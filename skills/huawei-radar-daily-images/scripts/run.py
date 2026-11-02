"""Local receipts for an agent-operated Word -> image deck. Never calls a model."""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid
import zipfile
from xml.etree import ElementTree as ET

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
VENDOR = SKILL / 'vendor/upstream'


def install_pycache_prefix():
    adapter = json.loads((SKILL / 'references/project.json').read_text(encoding='utf-8-sig'))
    relative = adapter.get('bytecode_prefix') or 'tmp/pycache'
    prefix = (REPO / relative).resolve()
    repo = REPO.resolve()
    if prefix != repo and repo not in prefix.parents:
        raise ValueError('bytecode prefix escapes repository')
    if prefix == VENDOR.resolve() or VENDOR.resolve() in prefix.parents:
        raise ValueError('bytecode prefix must stay outside vendor/upstream')
    prefix.mkdir(parents=True, exist_ok=True)
    os.environ['PYTHONPYCACHEPREFIX'] = str(prefix)
    sys.pycache_prefix = str(prefix)
    return prefix


install_pycache_prefix()
W = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
DATE_PATTERN = r'(?<!\d)(20\d{2})[-/年](\d{1,2})[-/月](\d{1,2})'


def dates_in(text):
    return sorted({'%s-%02d-%02d' % (y, int(m), int(d)) for y, m, d in re.findall(DATE_PATTERN, text)})


def report_dates(text):
    """Only report headings/labels establish identity; source event dates do not."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    found = []
    heading = r'^(?:AI4M(?:BD|B)SE\s*[｜|]\s*)?(?:(?:前沿)?雷达日报|日报精读)'
    for i, line in enumerate(lines[:30]):
        if len(line) > 180:
            continue
        if re.match(heading, line) or re.match(r'^(?:报告日期|日报日期)\s*[:：]', line):
            found += dates_in(line)
            if not dates_in(line) and i + 1 < len(lines) and re.match(DATE_PATTERN, lines[i+1]):
                found += dates_in(lines[i+1])
        elif i == 0 and re.match(DATE_PATTERN, line):
            # A leading date heading is common for user supplied standalone Word.
            if not re.search(r'论文|发布于|发表于|提交于|来源|参考', line):
                found += dates_in(line)
    return sorted(set(found))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(Path(path).read_bytes())


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(encoded(data))
    os.replace(temp, path)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def inside(path, root):
    path, root = Path(path).resolve(), Path(root).resolve()
    require(path != root and path.is_relative_to(root), 'path escapes output boundary')
    return path


@contextlib.contextmanager
def locked(root):
    root.mkdir(parents=True, exist_ok=True)
    path = root / '.lock'
    with path.open('x', encoding='utf-8') as stream:
        stream.write(str(os.getpid()))
    try:
        yield
    finally:
        path.unlink()


def lock_pin_error(path, expected):
    """Pin is the SHA-256 of the lock file's stored bytes, not a newline-normalized copy."""
    raw = Path(path).read_bytes()
    actual = digest(raw)
    if actual == expected:
        return None
    if b'\r\n' in raw:
        alternate, stored, other = raw.replace(b'\r\n', b'\n'), 'CRLF', 'LF'
    else:
        alternate, stored, other = raw.replace(b'\n', b'\r\n'), 'LF', 'CRLF'
    if digest(alternate) == expected:
        return 'upstream lock changed: line ending mismatch; pin matches %s bytes %s, stored file is %s %s' % (other, expected, stored, actual)
    return 'upstream lock changed: expected %s actual %s' % (expected, actual)


def configuration():
    adapter = read(SKILL / 'references/project.json')
    mismatch = lock_pin_error(VENDOR / 'bundle.lock.json', adapter['upstream_lock_sha256'])
    require(mismatch is None, mismatch)
    defaults = read(VENDOR / 'references/defaults.json')
    defaults['workspace'] = 'repository'
    defaults['output_paths'] = {'role_a': 'role-a', 'role_c': 'role-c', 'delivery': 'delivery'}
    defaults['visual_contract'] = read(SKILL / 'references/visual-contract.json')
    defaults['reading_manifest'] = read(SKILL / 'references/reading-manifest.json')
    defaults['adapter'] = adapter
    return defaults


def verify_vendor():
    result = subprocess.run([sys.executable, '-B', str(VENDOR / 'scripts/verify_bundle.py'), '--root', str(VENDOR)], capture_output=True, text=True, encoding='utf-8')
    require(result.returncode == 0, 'vendor verification failed: ' + result.stdout + result.stderr)
    return result.stdout


def extract(path):
    with zipfile.ZipFile(path) as archive:
        require(archive.getinfo('word/document.xml').file_size < 20_000_000, 'DOCX too large')
        root = ET.fromstring(archive.read('word/document.xml'))
        paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', W)) for p in root.findall('.//w:p', W)]
        text = '\n'.join(p for p in paragraphs if p.strip())
        links = re.findall(r'https?://[^\s<>]+', text)
        rel = 'word/_rels/document.xml.rels'
        if rel in archive.namelist():
            for entry in ET.fromstring(archive.read(rel)):
                if entry.get('Type', '').endswith('/hyperlink'):
                    links.append(entry.get('Target', ''))
        require(text.strip(), 'empty Word is not a zero-signal result')
        return {'text': text, 'links': sorted(set(links)), 'body_dates': dates_in(text), 'report_dates': report_dates(text)}


def handoff_input(path, word=None, date=None):
    data = read(path) if path else {}
    key = data.get('key') or data.get('date')
    require(not (date and key and date != key), 'handoff date conflict')
    word = word or data.get('narrative_docx') or data.get('word_path')
    require(word and (date or key), 'word and date required')
    if path and not Path(word).is_absolute():
        word = str(Path(path).resolve().parent / word)
    return word, date or key, data.get('narrative_docx_sha256') or data.get('word_sha256'), data.get('sources')


class Runner:
    def __init__(self, root=None, config=None):
        self.config = config if config is not None else configuration()
        self.root = Path(root).resolve() if root else inside(REPO / self.config['adapter']['output_root'], REPO)

    def run_path(self, value):
        path = inside(value, self.root)
        require(path.parent.parent == self.root, 'run must be date/identity under output root')
        return path

    def load(self, value):
        run = self.run_path(value)
        state = read(run / 'state.json')
        require(state['config_hash'] == digest(encoded(self.config)), 'configuration changed; prepare a new run')
        require(read(run / 'effective-config.json') == self.config, 'configuration snapshot changed')
        for name in ['input', 'prompts', 'native', 'versions', 'role-a', 'role-c', 'reviews', 'delivery']:
            inside(run / name, run)
        require(sha(run / 'input/source.docx') == state['word_hash'], 'input snapshot changed')
        require(sha(run / 'input/extracted.json') == state['extracted_hash'], 'extracted Word changed')
        if state.get('date_resolution_file_hash'):
            require(sha(run / 'input/date-resolution.json') == state['date_resolution_file_hash'], 'date resolution changed')
        for item in state['attempts']:
            require(sha(inside(run / item['prompt'], run)) == item['prompt_hash'], 'prompt changed')
            if item['status'] == 'recorded':
                for kind in ['native', 'final']:
                    require(sha(inside(run / item[kind], run)) == item[kind + '_hash'], 'registered image changed')
        if state.get('readiness'):
            self.check_readiness(run, state)
        if state.get('start'):
            require(sha(run / 'input/start.json') == state['start'], 'start receipt changed')
        if state.get('design'):
            for name, expected in state['design'].items():
                require(sha(inside(run / name, run)) == expected, 'design changed; prepare a new revision')
        return run, state

    def prepare(self, word, date, actor, expected=None, sources=None, revision='initial', date_evidence=None):
        from datetime import date as Date
        Date.fromisoformat(date)
        word = Path(word).resolve()
        require(word.suffix.lower() == '.docx', 'DOCX required')
        blob = word.read_bytes()
        word_hash = digest(blob)
        require(not expected or expected.lower() == word_hash, 'Word hash mismatch')
        content = extract(word)
        candidates = content['report_dates']
        basis = 'report-heading' if candidates else 'filename-or-explicit-caller-date'
        if not candidates:
            candidates = dates_in(word.name)
        resolution = None
        if date_evidence:
            resolution = read(date_evidence)
            quote = resolution.get('quote', '')
            require(resolution.get('date') == date and resolution.get('authority') == 'user' and len(resolution.get('reason','').strip()) >= 10, 'explicit user date clarification required')
            require(quote and quote in content['text'] and dates_in(quote) == [date], 'date clarification quote must locate the selected date in Word')
            require(not candidates or date in candidates, 'clarified date conflicts with report date')
            basis = 'user-clarified-report-date'
        require(not candidates or candidates == [date] or (len(candidates) > 1 and resolution), 'report date conflicts/ambiguous; clarify before prepare')
        identity = {'word_hash': word_hash, 'date': date, 'config_hash': digest(encoded(self.config)), 'revision': revision}
        if resolution:
            identity['date_resolution_hash'] = digest(encoded(resolution))
        key = digest(encoded(identity))
        self.root.mkdir(parents=True, exist_ok=True)
        run = inside(self.root / date / key[:20], self.root)
        with locked(self.root):
            if (run / 'state.json').exists():
                self.load(run)
                return run
            require(not run.exists(), 'partial prepare exists; preserve and inspect before recovery')
            (run / 'input').mkdir(parents=True)
            (run / 'input/source.docx').write_bytes(blob)
            write(run / 'input/extracted.json', content)
            write(run / 'input/sources.json', sources or [])
            write(run / 'effective-config.json', self.config)
            write(run / 'input/date-resolution.json', {'basis': basis, 'candidates': candidates, 'selected': date, 'clarification': resolution})
            write(run / 'state.json', {**identity, 'identity': key, 'schema': 'daily-images-run-v1', 'actor': actor, 'status': 'READING', 'source_path': str(word), 'attempts': [], 'pages': {}, 'review': None, 'design': {}, 'extracted_hash': sha(run / 'input/extracted.json'), 'date_resolution_file_hash': sha(run / 'input/date-resolution.json')})
        return run

    def check_readiness(self, run, state):
        ready = state.get('readiness')
        require(ready, 'reading gate not passed')
        require(sha(state['source_path']) == state['word_hash'], 'original Word changed; prepare a new run')
        for name, expected in ready['files'].items():
            require(sha(inside(run / name, run)) == expected, 'preparation evidence changed; prepare a new revision')
        for name, expected in ready['rules'].items():
            require(sha(inside(SKILL / name, SKILL)) == expected, 'reading resource changed; prepare a new revision')
        return ready

    def ready(self, value, receipt):
        run = self.run_path(value)
        with locked(run):
            run, state = self.load(run)
            require(not state.get('start') and not state['design'] and not state['attempts'], 'preparation is frozen after Step2 starts')
            try:
                report = read(receipt)
                require(report.get('word_hash') == state['word_hash'] and report.get('date') == state['date'], 'reading receipt identity mismatch')
                require(report.get('full_word_read') is True and report.get('golden_viewed') == list(range(1,11)), 'full Word/Golden reading missing')
                require(report.get('blockers') == [] and report.get('source_notes'), 'unresolved reading blockers/source notes')
                require(all(report.get('capabilities', {}).get(k) is True for k in ['imagegen','view_image','independent_review']), 'required host capability missing')
                manifest = read(SKILL / 'references/reading-manifest.json')
                assets = report.get('assets', [])
                require(len({x['path'] for x in assets}) == len(assets), 'duplicate reading asset')
                indexed = {x['path']:x for x in assets}
                rules = {}
                for name in manifest['required_rules'] + manifest['required_images']:
                    item = indexed.get(name, {})
                    require(item.get('status') == 'READ' and item.get('evidence'), 'required reading missing: ' + name)
                    actual = sha(inside(SKILL / name, SKILL))
                    require(item.get('sha256') == actual, 'reading asset changed: ' + name)
                    rules[name] = actual
                lock = VENDOR / 'bundle.lock.json'
                adapter = read(SKILL / 'references/project.json')
                require(sha(lock) == adapter['upstream_lock_sha256'], 'upstream lock changed')
                rules['references/project.json'] = sha(SKILL / 'references/project.json')
                rules['vendor/upstream/bundle.lock.json'] = sha(lock)
                for relative, expected in read(lock)['files'].items():
                    require(sha(inside(VENDOR / relative, VENDOR)) == expected, 'fixed resource changed: ' + relative)
                    rules['vendor/upstream/' + relative] = expected
                rules['references/reading-manifest.json'] = sha(SKILL / 'references/reading-manifest.json')
                require(report.get('rule_files') == manifest['required_rules'], 'rule_files must match reading manifest')
                sources = report.get('signals', [])
                require(sources and len({x['id'] for x in sources}) == len(sources), 'signal evidence inventory required')
                files = {}
                for item in sources:
                    require(item.get('word_locator') and item.get('claims') and item.get('source_status') in ['READ','WORD_SUFFICIENT','UNAVAILABLE'], 'incomplete signal evidence')
                    if item['source_status'] == 'READ':
                        require(item.get('url') and item.get('sections') and item.get('read_at'), 'source locator required')
                        name = item.get('snapshot', '')
                        require(name.startswith('input/'), 'source snapshot must be under input')
                        actual = sha(inside(run / name, run))
                        require(item.get('sha256') == actual, 'source snapshot changed')
                        files[name] = actual
                    else:
                        require(item.get('reason'), 'source reading reason required')
                        if item['source_status'] == 'UNAVAILABLE':
                            require(item.get('excluded_claims'), 'unavailable source must exclude unsupported claims')
                require(sha(state['source_path']) == state['word_hash'], 'original Word changed; prepare a new run')
                target = run / 'input/reading-receipt.json'
                write(target, report)
                files['input/reading-receipt.json'] = sha(target)
                state['readiness'] = {'files':files, 'rules':rules}
                state['readiness']['token'] = digest(encoded({'identity':state['identity'], 'files':files, 'rules':rules}))
                state['status'] = 'READY_FOR_DESIGN'
                state.pop('preparation_error', None)
            except (ValueError, OSError, KeyError, TypeError) as exc:
                state['status'] = 'PREPARATION_BLOCKED'
                state['preparation_error'] = str(exc)
                write(run / 'state.json', state)
                raise
            write(run / 'state.json', state)
            return {'status':state['status'], 'readiness_token':state['readiness']['token'], 'message':'Skill 全链路读取完成，可以启动任务。当前停留在准备阶段。'}

    def start(self, value, authorization):
        run = self.run_path(value)
        with locked(run):
            run, state = self.load(run)
            ready = self.check_readiness(run, state)
            require(state['status'] == 'READY_FOR_DESIGN' and not state.get('start'), 'Step2 already started or preparation not ready')
            report = read(authorization)
            require(report.get('authority') == 'user' and report.get('stage') == 'step2' and report.get('quote') and report.get('message_ref'), 'explicit Step2 user instruction required')
            require(report.get('readiness_token') == ready['token'], 'stale Step2 authorization')
            write(run / 'input/start.json', report)
            state['start'] = sha(run / 'input/start.json')
            state['status'] = 'DESIGN_AUTHORIZED'
            write(run / 'state.json', state)
            return state['status']

    def skip(self, date, evidence, reason):
        from datetime import date as Date
        Date.fromisoformat(date)
        proof = read(evidence)
        require(proof.get('date') == date and proof.get('valid_signal_count') == 0 and proof.get('authority') in ['user', 'upstream'] and proof.get('reference'), 'explicit zero-signal evidence required')
        require(reason and len(reason.strip()) >= 5, 'skip reason required')
        run = self.root / date / ('skip-' + digest(encoded(proof))[:15])
        with locked(self.root):
            run = self.run_path(run)
            write(run / 'skip.json', {'status':'SKIPPED', 'date':date, 'reason':reason, 'evidence':proof, 'image_calls':0})
        return str(run)

    def design(self, value):
        run = self.run_path(value)
        with locked(run):
            run, state = self.load(run)
            require(state.get('start'), 'Step2 authorization required before design')
            self.check_readiness(run, state)
            require(not state['attempts'], 'design frozen after first generation attempt')
            a = run / 'role-a'
            report = read(run / 'input/reading-receipt.json')
            require(report['word_hash'] == state['word_hash'] and report['date'] == state['date'], 'reading receipt identity mismatch')
            require(report.get('full_word_read') is True and report.get('golden_viewed') == list(range(1, 11)), 'full Word/Golden reading missing')
            require(report.get('source_notes') and report.get('rule_files'), 'reading/source evidence missing')
            spec = read(a / 'deck_spec.json')
            require([s['slide_no'] for s in spec['slides']] == list(range(1, 11)), 'exactly ten ordered slides required')
            audit = read(a / 'design-audit.json')
            require(audit.get('visual_contract') == read(SKILL / 'references/visual-contract.json'), 'public visual contract missing or changed')
            require([p['page'] for p in audit.get('pages', [])] == list(range(1,11)), 'ten design audit pages required')
            for page in audit['pages']:
                require(all(page.get(k) for k in ['layout_mapping','selection_reason','evidence_locations','supporting_increment','relationship_check']), 'page design evidence/relationship audit missing')
                require(page.get('hard_failures') == [], 'design hard failure')
            tools = VENDOR / 'bundle/skills0818-20260912/huawei_ppt_builder/tools'
            for script, args in [('validate_inputs.py', [a]), ('render_contract_builder.py', [a, run / 'role-c'])]:
                result = subprocess.run([sys.executable, '-B', str(tools / script), *map(str, args)], capture_output=True, text=True, encoding='utf-8')
                (run / (script + '.log')).write_text(result.stdout + result.stderr, encoding='utf-8')
                require(result.returncode == 0, script + ' failed; inspect run log')
            state['design'] = {p.relative_to(run).as_posix(): sha(p) for p in a.rglob('*') if p.is_file()}
            state['status'] = 'DESIGNED'
            write(run / 'state.json', state)

    def reserve(self, value, page, phase, prompt):
        run = self.run_path(value)
        with locked(run):
            run, state = self.load(run)
            require(bool(state['design']), 'design gate not passed')
            require(state.get('start'), 'Step2 authorization required before generation')
            self.check_readiness(run, state)
            require(1 <= page <= 10 and phase in ['C2', 'C2.6', 'C4'], 'invalid page/phase')
            require(not any(x['status'] == 'pending' and x['page'] == page for x in state['attempts']), 'pending generation: inspect tool result; do not duplicate')
            done = [x for x in state['attempts'] if x['page'] == page and x['status'] == 'recorded']
            require(phase == 'C2' or any(x['phase'] == 'C2' for x in done), 'C2 required before redraw')
            require(phase != 'C4' or any(x['phase'] == 'C2.6' for x in done), 'C2.6 required before repair')
            token = uuid.uuid4().hex
            target = run / 'prompts' / (token + '.txt')
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(Path(prompt).read_bytes())
            require(target.stat().st_size > 20, 'prompt empty')
            state['attempts'].append({'id': token, 'page': page, 'phase': phase, 'status': 'pending', 'prompt': target.relative_to(run).as_posix(), 'prompt_hash': sha(target)})
            state['review'] = None
            state['status'] = 'GENERATING'
            write(run / 'state.json', state)
            return token

    def abandon(self, value, token, reason):
        run = self.run_path(value)
        with locked(run):
            run, state = self.load(run)
            require(len(reason.strip()) >= 10, 'explain inspection and why no result is recoverable')
            item = next(x for x in state['attempts'] if x['id'] == token)
            require(item['status'] == 'pending', 'only pending attempts may be abandoned')
            item.update(status='abandoned', reason=reason)
            write(run / 'state.json', state)

    def record(self, value, token, image, tool_receipt):
        from PIL import Image
        run = self.run_path(value)
        with locked(run):
            run, state = self.load(run)
            item = next(x for x in state['attempts'] if x['id'] == token)
            require(item['status'] == 'pending', 'attempt already resolved')
            require(tool_receipt.strip(), 'tool receipt required')
            blob = Path(image).read_bytes()
            prior = [x for x in state['attempts'] if x['page'] == item['page'] and x['status'] == 'recorded']
            require(not prior or digest(blob) != prior[-1]['native_hash'], 'redraw must not copy previous image')
            with Image.open(image) as im:
                im.load()
                require(im.format == 'PNG', 'PNG required')
                width, height = im.size
                require(width >= 1024 and height >= 576 and abs(width / height - 16 / 9) < .04, 'image resolution/aspect invalid; redraw')
                native = run / 'native' / (token + '.png')
                final = run / 'versions' / (token + '.png')
                native.parent.mkdir(exist_ok=True); final.parent.mkdir(exist_ok=True)
                native.write_bytes(blob)
                if im.size == (1920, 1080):
                    final.write_bytes(blob)
                else:
                    # User permits size normalization only. No content editing/cropping.
                    from PIL import ImageOps
                    ImageOps.pad(im.convert('RGB'), (1920, 1080), method=Image.Resampling.LANCZOS, color='white').save(final)
            item.update(status='recorded', native=native.relative_to(run).as_posix(), final=final.relative_to(run).as_posix(), native_hash=sha(native), final_hash=sha(final), native_size=[width, height], final_size=[1920,1080], normalization='none' if [width,height]==[1920,1080] else 'contain-pad-lanczos', tool_receipt=tool_receipt)
            if item['phase'] != 'C2':
                state['pages'][str(item['page'])] = token
            state['review'] = None
            state['status'] = 'REVIEW_PENDING' if len(state['pages']) == 10 else 'GENERATING'
            write(run / 'state.json', state)

    def binding(self, value):
        run, state = self.load(value)
        require(len(state['pages']) == 10, 'ten final pages required')
        require(not any(x['status']=='pending' for x in state['attempts']), 'pending generation unresolved')
        chosen = {str(x['page']): x for x in state['attempts'] if state['pages'].get(str(x['page'])) == x['id']}
        return {'identity': state['identity'], 'word_hash': state['word_hash'], 'config_hash': state['config_hash'], 'pages': {n:chosen[n]['final_hash'] for n in map(str,range(1,11))}}

    def preview(self, value):
        from PIL import Image, ImageDraw
        run, state = self.load(value)
        self.binding(run)
        sheet = Image.new('RGB', (960,1450), 'white')
        draw = ImageDraw.Draw(sheet)
        for item in state['attempts']:
            page = item['page']
            if state['pages'].get(str(page)) != item['id']:continue
            with Image.open(run/item['final']) as im:
                im.load();thumb=im.copy();thumb.thumbnail((470,265))
                sheet.paste(thumb,(((page-1)%2)*480,((page-1)//2)*290))
            draw.text((((page-1)%2)*480+5,((page-1)//2)*290+265),f'P{page:02}',fill='black')
        target=run/'role-c/contact-sheet.png';target.parent.mkdir(exist_ok=True);sheet.save(target)
        return str(target)

    def approve(self, value, review):
        run = self.run_path(value)
        with locked(run):
            run, state = self.load(run)
            report = read(review)
            require(report['binding'] == self.binding(run), 'stale review binding')
            require(report.get('reviewer') and report['reviewer'] != state['actor'], 'independent reviewer required')
            require(report.get('reviewer_task') and report.get('verdict') == 'PASS', 'independent task PASS required')
            require([p['page'] for p in report['pages']] == list(range(1,11)), 'page review incomplete')
            require(all(p.get('viewed') is True and p.get('verdict')=='PASS' and p.get('notes') for p in report['pages']), 'page review failed')
            checks = read(SKILL / 'references/visual-contract.json')['review_checks']
            for page in report['pages']:
                require(page.get('hard_failures') == [], 'visual hard failure blocks approval')
                require(all(page.get('checks', {}).get(k, {}).get('verdict') == 'PASS' and page['checks'][k].get('evidence') for k in checks), 'explicit visual/relationship checks required')
            for name in ['self-check.json', 'refinement-report.md', 'cross-page-review.md']:
                require((run/'role-c'/name).is_file(), 'missing C stage evidence: '+name)
            self_check = read(run/'role-c/self-check.json')
            require(self_check['binding'] == report['binding'], 'stale self check')
            require([p['page'] for p in self_check['pages']] == list(range(1,11)) and all(p['score'] >= 92 and p['hard_failures']==[] for p in self_check['pages']), 'self check failed')
            write(run/'reviews/approved.json', report)
            state['review'] = {'path':'reviews/approved.json','sha256':sha(run/'reviews/approved.json'), 'evidence':{name:sha(run/'role-c'/name) for name in ['self-check.json','refinement-report.md','cross-page-review.md']}}
            state['status']='APPROVED'
            write(run/'state.json',state)

    def finalize(self, value):
        from PIL import Image, ImageDraw
        from datetime import datetime, timezone
        run = self.run_path(value)
        with locked(run):
            run,state=self.load(run)
            require(state['review'], 'independent approval required')
            approved=run/state['review']['path']
            require(sha(approved)==state['review']['sha256'], 'review changed')
            review=read(approved)
            require(review['binding']==self.binding(run), 'review invalidated')
            for name,expected in state['review']['evidence'].items():
                require(sha(run/'role-c'/name)==expected,'C stage evidence changed')
            out=inside(run/'delivery',run);out.mkdir(exist_ok=True)
            chosen={str(x['page']):x for x in state['attempts'] if state['pages'].get(str(x['page']))==x['id']}
            sheet=Image.new('RGB',(960,1450),'white');draw=ImageDraw.Draw(sheet)
            pages=[]
            for i in range(1,11):
                item=chosen[str(i)];name=f'P{i:02}.png';source=inside(run/item['final'],run)
                with Image.open(source) as im:
                    im.load();require(im.size==(1920,1080),'wrong final size')
                    thumb=im.copy();thumb.thumbnail((470,265));sheet.paste(thumb,(((i-1)%2)*480,((i-1)//2)*290))
                    draw.text((((i-1)%2)*480+5,((i-1)//2)*290+265),f'P{i:02}',fill='black')
                (out/name).write_bytes(source.read_bytes())
                pages.append({'page':i,'file':name,'sha256':sha(out/name),'native_size':item['native_size'],'final_size':item['final_size'],'normalization':item['normalization']})
            sheet.save(out/'contact-sheet.png')
            spec=read(run/'role-a/deck_spec.json') if (run/'role-a/deck_spec.json').exists() else {}
            from urllib.parse import urlsplit, urlunsplit
            source_urls=[]
            for value in review.get('sources_checked',[]):
                part=urlsplit(value)
                require(part.scheme in ['https','http'] and part.hostname and not part.username and not part.password, 'invalid public source URL')
                source_urls.append(urlunsplit((part.scheme,part.netloc,part.path,'',part.fragment)))
            public={'schema':'daily-images-delivery-v1','date':state['date'],'project_name':spec.get('deck_title','Radar daily images'), 'delivery_mode':'page_images','page_range':[1,10],'image_resolution':[1920,1080], 'source_files':[{'type':'docx','sha256':state['word_hash']}], 'generated_files':[p['file'] for p in pages]+['contact-sheet.png','manifest.json','review-summary.md'], 'self_check_summary':'10 pages passed; independent review bound to final hashes', 'known_limitations':['Image slides, no editable PPTX','Native size and any normalization disclosed per page','Engineering examples are not business validation results'], 'created_at':datetime.now(timezone.utc).isoformat(),'word_sha256':state['word_hash'],'pages':pages,'review':'PASS','scope':'local artifacts; no publication','contact_sheet_sha256':sha(out/'contact-sheet.png')}
            public['source_urls']=sorted(set(source_urls))
            write(out/'manifest.json',public)
            titles={str(s['slide_no']):s['title'] for s in spec.get('slides',[])}
            summary=['# Independent review','10 pages reviewed: PASS. The review is bound to the hashes in manifest.json.','Native resolution and normalization are recorded per page.','## Pages']
            summary += [f"- P{i:02} {titles.get(str(i),'')} — PASS" for i in range(1,11)]
            summary += ['## Limits', *public['known_limitations']]
            (out/'review-summary.md').write_text('\n\n'.join(summary)+'\n',encoding='utf-8')
            names=[p['file'] for p in pages]+['contact-sheet.png','manifest.json','review-summary.md']
            temp=out/'deck.zip.tmp'
            with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
                for name in names:z.write(out/name,name)
            os.replace(temp,out/'deck.zip')
            state['status']='DELIVERED';state['delivery']={name:sha(out/name) for name in names+['deck.zip']}
            write(run/'state.json',state)
            return public


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['verify','prepare','ready','start','skip','status','design','reserve','abandon','record','binding','preview','approve','finalize'])
    for flag in ['word','handoff','date','date-evidence','actor','run','phase','prompt','attempt','image','tool-receipt','reason','review','zero-evidence','revision','receipt','authorization']:
        parser.add_argument('--'+flag)
    parser.add_argument('--page',type=int)
    a=parser.parse_args()
    if a.command=='verify':
        configuration()
        print(verify_vendor());return
    runner=Runner()
    if a.command=='prepare':
        verify_vendor()
        word,date,expected,sources=handoff_input(a.handoff,a.word,a.date)
        require(a.actor,'actor required')
        result=str(runner.prepare(word,date,a.actor,expected,sources,a.revision or 'initial',a.date_evidence))
    elif a.command=='ready':result=runner.ready(a.run,a.receipt)
    elif a.command=='start':result=runner.start(a.run,a.authorization)
    elif a.command=='skip':result=runner.skip(a.date,a.zero_evidence,a.reason)
    elif a.command=='status':
        run=runner.run_path(a.run)
        result=read(run/'skip.json') if (run/'skip.json').exists() else runner.load(run)[1]
    elif a.command=='design':result=runner.design(a.run)
    elif a.command=='reserve':result=runner.reserve(a.run,a.page,a.phase,a.prompt)
    elif a.command=='abandon':result=runner.abandon(a.run,a.attempt,a.reason)
    elif a.command=='record':result=runner.record(a.run,a.attempt,a.image,a.tool_receipt)
    elif a.command=='binding':result=runner.binding(a.run)
    elif a.command=='preview':result=runner.preview(a.run)
    elif a.command=='approve':result=runner.approve(a.run,a.review)
    else:result=runner.finalize(a.run)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,StopIteration,zipfile.BadZipFile,ET.ParseError) as exc:
        print(json.dumps({'ok':False,'error':str(exc)},ensure_ascii=False),file=sys.stderr);sys.exit(1)
