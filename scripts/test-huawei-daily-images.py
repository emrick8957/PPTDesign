"""Offline receipts tests. Fixture bitmaps never count as real imagegen acceptance."""
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
import tempfile
import unittest
import zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('daily_images',ROOT/'skills/huawei-radar-daily-images/scripts/run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def docx(path,text='2026-09-26 信号：测试材料', link=True):
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('word/document.xml',f'<w:document xmlns:w="{m.W["w"]}"><w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p><w:tbl><w:tr><w:tc><w:p><w:r><w:t>表格内容</w:t></w:r></w:p></w:tc></w:tr></w:tbl></w:body></w:document>' if text else f'<w:document xmlns:w="{m.W["w"]}"/>')
        if link:z.writestr('word/_rels/document.xml.rels','<Relationships><Relationship Type="x/hyperlink" Target="https://example.org/source"/></Relationships>')


class Receipts(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.word=self.base/'中文 路径.docx';docx(self.word)
        self.r=m.Runner(self.base/'runs',{'adapter':{'version':'fixture'}})
        self.run=self.r.prepare(self.word,'2026-09-26','creator')
        self.prompt=self.base/'prompt.txt';self.prompt.write_text('This is a fixture prompt, not a real image generation.',encoding='utf-8')
        self.image=self.base/'fixture.png';Image.new('RGB',(1920,1080),'white').save(self.image)

    def reading_receipt(self):
        manifest=m.read(m.SKILL/'references/reading-manifest.json')
        report={'word_hash':m.sha(self.word),'date':'2026-09-26','full_word_read':True,'golden_viewed':list(range(1,11)),
                'source_notes':'Synthetic offline fixture; no real reading claimed.', 'blockers':[],
                'capabilities':{k:True for k in ['imagegen','view_image','independent_review']},
                'rule_files':manifest['required_rules'],
                'assets':[{'path':name,'sha256':m.sha(m.SKILL/name),'status':'READ','evidence':'fixture-only'} for name in manifest['required_rules']+manifest['required_images']],
                'signals':[{'id':'S1','word_locator':'paragraph 1','claims':['fixture only'],'source_status':'WORD_SUFFICIENT','reason':'synthetic fixture'}]}
        path=self.base/'reading.json';m.write(path,report);return path

    def ready_start(self):
        result=self.r.ready(self.run,self.reading_receipt())
        path=self.base/'start.json';m.write(path,{'authority':'user','stage':'step2','quote':'fixture start','message_ref':'fixture-only','readiness_token':result['readiness_token']})
        self.r.start(self.run,path)

    def ready_design(self):
        self.ready_start()
        # Fixture setup deliberately bypasses real design; TC-08 owns live validation.
        state=m.read(self.run/'state.json');(self.run/'fixture-design.txt').write_text('fixture')
        state['design']={'fixture-design.txt':m.sha(self.run/'fixture-design.txt')};state['status']='DESIGNED';m.write(self.run/'state.json',state)

    def ten(self):
        self.ready_design()
        for page in range(1,11):
            for phase in ['C2','C2.6']:
                Image.new('RGB',(1920,1080),'white' if phase=='C2' else '#eeeeee').save(self.image)
                token=self.r.reserve(self.run,page,phase,self.prompt)
                self.r.record(self.run,token,self.image,'fixture-only')

    def review(self):
        binding=self.r.binding(self.run)
        m.write(self.run/'role-c/self-check.json',{'binding':binding,'pages':[{'page':i,'score':92,'hard_failures':[]} for i in range(1,11)]})
        for name in ['refinement-report.md','cross-page-review.md']:(self.run/'role-c'/name).write_text('fixture evidence only')
        report={'binding':binding,'reviewer':'independent','reviewer_task':'fixture-task','verdict':'PASS','sources_checked':['https://example.org/source?temporary=hidden#section'],'pages':[{'page':i,'viewed':True,'verdict':'PASS','notes':'fixture, not actual visual review','hard_failures':[],'checks':{k:{'verdict':'PASS','evidence':'fixture, not real visual verification'} for k in m.read(m.SKILL/'references/visual-contract.json')['review_checks']}} for i in range(1,11)]}
        path=self.base/'review.json';m.write(path,report);return path

    def test_step1_stops_and_requires_step2(self):
        self.assertEqual(self.r.load(self.run)[1]['status'],'READING')
        with self.assertRaisesRegex(ValueError,'Step2'):self.r.design(self.run)
        result=self.r.ready(self.run,self.reading_receipt())
        state=self.r.load(self.run)[1]
        self.assertEqual(state['status'],'READY_FOR_DESIGN');self.assertEqual(state['attempts'],[])
        self.assertFalse((self.run/'role-a').exists());self.assertFalse((self.run/'native').exists())
        with self.assertRaisesRegex(ValueError,'Step2'):self.r.design(self.run)
        path=self.base/'start.json';m.write(path,{'authority':'user','stage':'step2','quote':'fixture','message_ref':'fixture','readiness_token':'stale'})
        with self.assertRaisesRegex(ValueError,'stale'):self.r.start(self.run,path)
        d=m.read(path);d['readiness_token']=result['readiness_token'];m.write(path,d)
        self.r.start(self.run,path);self.assertEqual(self.r.load(self.run)[1]['status'],'DESIGN_AUTHORIZED')

    def test_missing_reading_and_golden_block(self):
        for field in ['assets','golden_viewed','capabilities']:
            path=self.reading_receipt();d=m.read(path);d[field]=[] if field!='capabilities' else {};m.write(path,d)
            with self.assertRaises(ValueError):self.r.ready(self.run,path)
            self.assertEqual(m.read(self.run/'state.json')['status'],'PREPARATION_BLOCKED')
        self.r.ready(self.run,self.reading_receipt())

    def test_preparation_invalidates_on_word_and_source_change(self):
        path=self.reading_receipt();d=m.read(path)
        source=self.run/'input/source.txt';source.write_text('fixture source')
        d['signals'][0].update(source_status='READ',url='https://example.org',sections=['1'],read_at='2026-09-30',snapshot='input/source.txt',sha256=m.sha(source))
        m.write(path,d);self.r.ready(self.run,path)
        source.write_text('changed')
        with self.assertRaisesRegex(ValueError,'preparation evidence changed'):self.r.load(self.run)
        source.write_text('fixture source');docx(self.word,'2026-09-26 changed')
        with self.assertRaisesRegex(ValueError,'original Word changed'):self.r.load(self.run)

    def test_readiness_receipt_and_rule_tamper(self):
        self.r.ready(self.run,self.reading_receipt())
        state=m.read(self.run/'state.json');name=next(iter(state['readiness']['rules']))
        state['readiness']['rules'][name]='changed';m.write(self.run/'state.json',state)
        with self.assertRaisesRegex(ValueError,'reading resource changed'):self.r.load(self.run)

    def test_unread_vendor_tool_change_blocks_resume(self):
        from unittest.mock import patch
        self.r.ready(self.run,self.reading_receipt())
        tool=m.VENDOR/'bundle/skills0818-20260912/huawei_ppt_builder/tools/render_contract_builder.py'
        original=m.sha
        def changed(path):
            return 'changed-tool' if Path(path).resolve()==tool.resolve() else original(path)
        with patch.object(m,'sha',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'reading resource changed'):self.r.load(self.run)
        self.assertEqual(self.r.load(self.run)[1]['status'],'READY_FOR_DESIGN')

    def test_design_requires_complete_audit(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        self.ready_start()
        a=self.run/'role-a'
        m.write(a/'deck_spec.json',{'slides':[{'slide_no':i} for i in range(1,11)]})
        audit={'visual_contract':m.read(m.SKILL/'references/visual-contract.json'),
               'pages':[{'page':i,'layout_mapping':'fixture','selection_reason':'fixture','evidence_locations':'fixture',
                         'supporting_increment':'not applicable: fixture','relationship_check':'fixture','hard_failures':[]} for i in range(1,11)]}
        audit['pages'][0]['relationship_check']='';m.write(a/'design-audit.json',audit)
        with self.assertRaisesRegex(ValueError,'relationship audit'):self.r.design(self.run)
        audit['pages'][0]['relationship_check']='fixture relationship reviewed';m.write(a/'design-audit.json',audit)
        # Only adapter state transition is tested; upstream compiler has separate validation.
        with patch.object(m.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout='',stderr='')):
            self.r.design(self.run)
        self.assertEqual(self.r.load(self.run)[1]['status'],'DESIGNED')
        audit['pages'][0]['selection_reason']='changed';m.write(a/'design-audit.json',audit)
        with self.assertRaisesRegex(ValueError,'design changed'):self.r.load(self.run)

    def test_visual_and_relation_failures_block_approval(self):
        self.ten()
        for key in ['public_layout','relationship_paths']:
            path=self.review();d=m.read(path);d['pages'][0]['checks'][key]['verdict']='FAIL';m.write(path,d)
            with self.assertRaisesRegex(ValueError,'explicit visual'):self.r.approve(self.run,path)
        path=self.review();d=m.read(path);d['pages'][0]['hard_failures']=['header above title'];m.write(path,d)
        with self.assertRaisesRegex(ValueError,'hard failure'):self.r.approve(self.run,path)

    def test_input_identity_and_revisions(self):
        content=m.extract(self.word);self.assertIn('表格内容',content['text']);self.assertIn('https://example.org/source',content['links'])
        self.assertEqual(self.run,self.r.prepare(self.word,'2026-09-26','other'))
        self.assertNotEqual(self.run,self.r.prepare(self.word,'2026-09-26','creator',revision='corrected-source'))
        before=m.sha(self.word)
        with self.assertRaisesRegex(ValueError,'hash mismatch'):self.r.prepare(self.word,'2026-09-26','x','f'*64)
        with self.assertRaisesRegex(ValueError,'date conflicts'):self.r.prepare(self.word,'2026-09-27','x')
        self.assertEqual(before,m.sha(self.word))
        docx(self.word,'2026-09-26 changed');self.assertNotEqual(self.run,self.r.prepare(self.word,'2026-09-26','x'))

    def test_invalid_empty_and_tamper(self):
        docx(self.word,'')
        with self.assertRaisesRegex(ValueError,'empty Word'):self.r.prepare(self.word,'2026-09-26','x')
        self.word.write_text('invalid')
        with self.assertRaises(zipfile.BadZipFile):self.r.prepare(self.word,'2026-09-26','x')
        (self.run/'input/source.docx').write_text('tamper')
        with self.assertRaisesRegex(ValueError,'snapshot changed'):self.r.load(self.run)

    def test_pending_lock_and_paths(self):
        with self.assertRaisesRegex(ValueError,'design gate'):self.r.reserve(self.run,1,'C2',self.prompt)
        self.ready_design();token=self.r.reserve(self.run,1,'C2',self.prompt)
        with self.assertRaisesRegex(ValueError,'pending'):self.r.reserve(self.run,1,'C2',self.prompt)
        self.r.abandon(self.run,token,'Checked the tool output: no recoverable result exists.')
        self.r.reserve(self.run,1,'C2',self.prompt)
        with self.assertRaises(FileExistsError):
            with m.locked(self.run):self.r.reserve(self.run,2,'C2',self.prompt)
        with self.assertRaisesRegex(ValueError,'boundary'):self.r.load(self.base)
        with self.assertRaisesRegex(ValueError,'ten final'):self.r.binding(self.run)

    def test_wrong_phase_and_bitmap(self):
        self.ready_design()
        with self.assertRaisesRegex(ValueError,'C2 required'):self.r.reserve(self.run,1,'C2.6',self.prompt)
        token=self.r.reserve(self.run,1,'C2',self.prompt)
        Image.new('RGB',(100,100),'white').save(self.image)
        with self.assertRaisesRegex(ValueError,'aspect invalid'):self.r.record(self.run,token,self.image,'fixture')
        self.image.write_text('not png')
        with self.assertRaises(OSError):self.r.record(self.run,token,self.image,'fixture')

    def test_approval_rework_and_delivery(self):
        self.ten()
        with self.assertRaisesRegex(ValueError,'approval required'):self.r.finalize(self.run)
        path=self.review();report=m.read(path);report['reviewer']='creator';m.write(path,report)
        with self.assertRaisesRegex(ValueError,'independent reviewer'):self.r.approve(self.run,path)
        path=self.review();report=m.read(path);report['binding']['pages']['1']='stale';m.write(path,report)
        with self.assertRaisesRegex(ValueError,'stale'):self.r.approve(self.run,path)
        path=self.review();self.r.approve(self.run,path);self.r.finalize(self.run)
        archive=self.run/'delivery/deck.zip'
        with zipfile.ZipFile(archive) as z:
            self.assertEqual(len(z.namelist()),13)
            self.assertFalse(any(n.endswith(('.docx','.pptx')) or '..' in n for n in z.namelist()))
            self.assertNotIn(str(self.base),z.read('manifest.json').decode())
            self.assertEqual(json.loads(z.read('manifest.json'))['source_urls'],['https://example.org/source#section'])
        archive.unlink();self.r.finalize(self.run);self.assertTrue(archive.exists())
        token=self.r.reserve(self.run,1,'C4',self.prompt)
        with self.assertRaisesRegex(ValueError,'approval required'):self.r.finalize(self.run)
        with self.assertRaisesRegex(ValueError,'copy previous'):self.r.record(self.run,token,self.image,'fixture-repair')
        Image.new('RGB',(1920,1080),'#dddddd').save(self.image)
        self.r.record(self.run,token,self.image,'fixture-repair')
        self.assertIsNone(self.r.load(self.run)[1]['review'])

    def test_zero_signals(self):
        proof=self.base/'zero.json';m.write(proof,{'date':'2026-09-26','valid_signal_count':0,'authority':'upstream','reference':'fixture'})
        run=Path(self.r.skip('2026-09-26',proof,'Confirmed zero valid signals'))
        self.assertEqual(m.read(run/'skip.json')['image_calls'],0)
        m.write(proof,{'date':'2026-09-26','valid_signal_count':1})
        with self.assertRaisesRegex(ValueError,'zero-signal'):self.r.skip('2026-09-26',proof,'not empty')

    def test_upstream_lock_pin_matches_stored_bytes(self):
        config = m.configuration()
        raw = (m.VENDOR / 'bundle.lock.json').read_bytes()
        self.assertNotIn(b'\r\n', raw)
        self.assertEqual(config['adapter']['upstream_lock_sha256'], m.digest(raw))
        self.assertNotEqual(m.digest(raw.replace(b'\n', b'\r\n')), config['adapter']['upstream_lock_sha256'])
        self.assertIsNone(m.lock_pin_error(m.VENDOR / 'bundle.lock.json', m.digest(raw)))

    def test_lock_line_ending_mismatch_is_explicit(self):
        raw = (m.VENDOR / 'bundle.lock.json').read_bytes()
        pinned_as_crlf = m.digest(raw.replace(b'\n', b'\r\n'))
        message = m.lock_pin_error(m.VENDOR / 'bundle.lock.json', pinned_as_crlf)
        self.assertIn('line ending mismatch', message)
        self.assertIn('stored file is LF', message)
        content = m.lock_pin_error(m.VENDOR / 'bundle.lock.json', '0' * 64)
        self.assertIn('expected ' + '0' * 64, content)
        self.assertNotIn('line ending', content)

    def test_discovery_and_vendor(self):
        alias=ROOT/'.agents/skills/radar-daily-images'
        self.assertEqual((alias/'../../../skills/huawei-radar-daily-images/SKILL.md').resolve(),m.SKILL/'SKILL.md')
        self.assertIn('"errors": []',m.verify_vendor())
        vendor=self.base/'vendor';shutil.copytree(m.VENDOR,vendor)
        (vendor/'SKILL.md').write_text('tampered copy',encoding='utf-8')
        check=subprocess.run([__import__('sys').executable,'-B',str(vendor/'scripts/verify_bundle.py'),'--root',str(vendor)],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(check.returncode,0);self.assertIn('hash mismatch: SKILL.md',check.stdout)

    def test_handoff_without_cover_and_config(self):
        handoff=self.base/'handoff.json'
        m.write(handoff,{'key':'2026-09-26','narrative_docx':self.word.name,'narrative_docx_sha256':m.sha(self.word)})
        word,date,expected,sources=m.handoff_input(handoff)
        self.assertEqual(self.run,self.r.prepare(word,date,'upstream',expected,sources))
        with self.assertRaisesRegex(ValueError,'date conflict'):m.handoff_input(handoff,date='2026-09-27')
        m.write(handoff,{'date':'2026-09-26','word_path':str(self.word),'word_sha256':'0'*64})
        word,date,expected,sources=m.handoff_input(handoff)
        with self.assertRaisesRegex(ValueError,'hash mismatch'):self.r.prepare(word,date,'upstream',expected,sources)
        other=m.Runner(self.r.root,{'adapter':{'version':'changed'}})
        self.assertNotEqual(self.run,other.prepare(self.word,'2026-09-26','creator'))
        with self.assertRaisesRegex(ValueError,'configuration changed'):other.load(self.run)
        m.write(self.run/'effective-config.json',{'tampered':True})
        with self.assertRaisesRegex(ValueError,'snapshot changed'):self.r.load(self.run)

    def test_missing_page_normalization_and_evidence_tamper(self):
        self.ten();state=m.read(self.run/'state.json');chosen=state['pages'].pop('10');m.write(self.run/'state.json',state)
        with self.assertRaisesRegex(ValueError,'ten final'):self.r.binding(self.run)
        with self.assertRaisesRegex(ValueError,'approval required'):self.r.finalize(self.run)
        state['pages']['10']=chosen;m.write(self.run/'state.json',state)
        # Real normalization implementation is exercised, never counted as model output.
        token=self.r.reserve(self.run,1,'C4',self.prompt)
        Image.new('RGB',(1536,864),'#ababab').save(self.image);native=m.sha(self.image)
        self.r.record(self.run,token,self.image,'fixture normalization')
        item=next(x for x in self.r.load(self.run)[1]['attempts'] if x['id']==token)
        self.assertEqual(m.sha(self.run/item['native']),native)
        with Image.open(self.run/item['final']) as im:self.assertEqual(im.size,(1920,1080))
        self.r.approve(self.run,self.review())
        (self.run/'role-c/cross-page-review.md').write_text('changed evidence')
        with self.assertRaisesRegex(ValueError,'evidence changed'):self.r.finalize(self.run)
        self.r.approve(self.run,self.review())
        Image.new('RGB',(640,360),'white').save(self.run/item['final'])
        with self.assertRaisesRegex(ValueError,'registered image changed'):self.r.finalize(self.run)

    def test_git_output_boundary(self):
        output='reports/daily-images/2099-01-01/fixture/delivery/P01.png'
        result=subprocess.run(['git','check-ignore',output],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0)
        files=[str(p.relative_to(ROOT)).replace('\\','/') for p in m.VENDOR.rglob('*') if p.is_file()]
        result=subprocess.run(['git','check-ignore','--stdin'],cwd=ROOT,input='\n'.join(files)+'\n',capture_output=True,text=True)
        self.assertEqual(result.stdout,'');self.assertEqual(result.returncode,1)

    def test_report_date_vs_source_dates_and_clarification(self):
        docx(self.word,'2026-09-26 前沿雷达日报\n论文发表于2026-09-25，另一个实验开始于2026-09-20')
        run=self.r.prepare(self.word,'2026-09-26','creator')
        handoff=self.base/'dated-handoff.json';m.write(handoff,{'date':'2026-09-26','word_path':str(self.word)})
        word,date,expected,sources=m.handoff_input(handoff)
        self.assertEqual(run,self.r.prepare(word,date,'upstream',expected,sources))
        self.assertEqual(m.read(run/'input/date-resolution.json')['candidates'],['2026-09-26'])
        with self.assertRaisesRegex(ValueError,'report date conflicts'):self.r.prepare(self.word,'2026-09-25','creator')
        docx(self.word,'发布信息\nAI4MBDSE｜雷达日报2026-09-26 | 主题\nAI4MBDSE｜前沿雷达日报\n2026-09-26｜AI × MBSE\n论文发表于2026-09-25')
        self.r.prepare(self.word,'2026-09-26','creator')
        docx(self.word,'2026/09/26 前沿雷达日报\n论文发表于2026年9月25日')
        self.r.prepare(self.word,'2026-09-26','creator')
        docx(self.word,'前沿雷达日报\n2026-09-26｜主题\n报告日期：2026-09-25')
        before=m.sha(self.word)
        with self.assertRaisesRegex(ValueError,'ambiguous'):self.r.prepare(self.word,'2026-09-26','creator')
        proof=self.base/'date-proof.json';m.write(proof,{'date':'2026-09-26','authority':'user','quote':'2026-09-26｜主题','reason':'用户确认应以正式正文标题下方的日期为准。'})
        run=self.r.prepare(self.word,'2026-09-26','creator',date_evidence=proof)
        self.assertIn('date_resolution_hash',self.r.load(run)[1])
        self.assertEqual(before,m.sha(self.word))
        m.write(proof,{'date':'2026-09-26','authority':'user','quote':'不存在的日期2026-09-26','reason':'用户确认应以正式正文标题下方的日期为准。'})
        with self.assertRaisesRegex(ValueError,'quote must locate'):self.r.prepare(self.word,'2026-09-26','creator',date_evidence=proof)
        m.write(run/'input/date-resolution.json',{'changed':True})
        with self.assertRaisesRegex(ValueError,'date resolution changed'):self.r.load(run)
        # Body event dates are not report metadata; an unambiguous filename is fallback.
        other=self.base/'radar-2026-09-26.docx';docx(other,'研究观察\n论文发表于2026-09-25')
        self.r.prepare(other,'2026-09-26','creator')
        with self.assertRaisesRegex(ValueError,'report date conflicts'):self.r.prepare(other,'2026-09-25','creator')


if __name__=='__main__':unittest.main(verbosity=2)
