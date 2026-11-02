"""Verify a portable package. No model calls and no image-quality certification."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'package-manifest.json').read_text(encoding='utf-8'))
errors = []
for name, expected in manifest['files'].items():
    path = (root / name).resolve()
    if root not in path.parents or not path.is_file():
        errors.append('Missing or invalid path: ' + name)
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected['sha256']:
        errors.append('SHA256 mismatch: ' + name)
skill = root / 'skills/huawei-radar-daily-images'
reading = json.loads((skill / 'references/reading-manifest.json').read_text(encoding='utf-8-sig'))
for name in reading['required_rules'] + reading['required_images']:
    if not (skill / name).is_file():
        errors.append('Required reading asset missing: ' + name)
try:
    import PIL
    pillow = PIL.__version__
except ImportError:
    pillow = None
    errors.append('Pillow missing: use the host runtime or install requirements.txt')
result = subprocess.run([sys.executable, '-B', str(skill / 'scripts/run.py'), 'verify'], capture_output=True, text=True, encoding='utf-8')
if result.returncode:
    errors.append('Vendor verification failed: ' + result.stdout + result.stderr)
else:
    vendor = json.loads(result.stdout)
print(json.dumps({'status': 'FAIL' if errors else 'PASS', 'scope': 'package integrity and runtime dependencies only', 'files_checked': len(manifest['files']), 'reading_rules': len(reading['required_rules']), 'golden_images': len(reading['required_images']), 'vendor': vendor if not result.returncode else None, 'pillow': pillow, 'errors': errors}, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
