"""Read-only integrity check for the pinned daily-slide skill bundle."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile


def verify(root):
    root = root.resolve()
    manifest = json.loads((root / 'bundle.lock.json').read_text(encoding='utf-8'))
    errors = []
    for relative, expected in manifest['files'].items():
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            errors.append(f'out-of-root path: {relative}')
            continue
        if not path.is_file():
            errors.append(f'missing: {relative}')
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            errors.append(f'hash mismatch: {relative}')
        try:
            if path.suffix in ('.md', '.txt', '.py', '.yaml', '.json'):
                text = raw.decode('utf-8-sig')
                if path.suffix == '.json':
                    json.loads(text)
            elif path.suffix == '.zip':
                with ZipFile(path) as archive:
                    bad = archive.testzip()
                    if bad:
                        errors.append(f'ZIP CRC failure: {relative}:{bad}')
        except Exception as exc:
            errors.append(f'unreadable: {relative}: {exc}')
    for relative in manifest['required']:
        if relative not in manifest['files']:
            errors.append(f'unpinned required file: {relative}')
    config = json.loads((root / 'references/defaults.json').read_text(encoding='utf-8'))
    if config['page_count'] != 10 or config['output']['create_pptx']:
        errors.append('default page count/output mismatch')
    return {'bundle': manifest['bundle_id'], 'checked_files': len(manifest['files']), 'errors': errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    result = verify(parser.parse_args().root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if result['errors'] else 0)
