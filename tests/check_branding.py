# SPDX-License-Identifier: MIT
"""Validate generated graphics against the game's existing skin inventory."""
import io
import json
from pathlib import Path
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from release_assets import branding

baseline = json.loads((ROOT / 'config/releases/preview-baseline.json').read_text())
expected = {n for n in baseline['files'] if n.endswith('.png') and
            ('/Theme/' in n or '/Encyclopedia/' in n)}
graphics = branding()
assert set(graphics) == expected
for name, data in graphics.items():
    image = Image.open(io.BytesIO(data))
    image.verify()
    image = Image.open(io.BytesIO(data))
    if '/ME/' in name:
        assert image.size == (1920, 1080)
    elif '/Encyclopedia/' in name:
        assert image.size == (1280, 720)
    else:
        size = 76 if '76x76' in name else 38 if '38x38' in name else 256
        assert image.size == (size, size)
print('PASS: eleven original graphics match the shipped skin inventory and dimensions')
