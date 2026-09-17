# SPDX-License-Identifier: MIT
"""Bundle a committed preview ZIP and Python/Tk into a single Windows setup EXE."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--aircraft-zip', type=Path, required=True)
    args = parser.parse_args()
    if os.name != 'nt':
        parser.error('Build the Windows installer on Windows')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT).strip():
        parser.error('Commit source changes before building')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    archive = args.aircraft_zip.resolve(strict=True)
    with zipfile.ZipFile(archive) as z:
        release = json.loads(z.read('release.json'))
    if release['corresponding_source_commit'] != commit:
        parser.error('Repackage the aircraft from the current source commit first')
    work = ROOT / 'build/setup' / commit[:12]
    work.mkdir(parents=True, exist_ok=True)
    shutil.copy2(archive, work / 'payload.zip')
    notices = work / 'runtime-notices'
    notices.mkdir(exist_ok=True)
    shutil.copy2(Path(sys.base_prefix) / 'LICENSE.txt', notices / 'Python-LICENSE.txt')
    shutil.copy2(Path(sys.base_prefix) / 'tcl/tk8.6/license.terms', notices / 'Tk-LICENSE.txt')
    distribution = importlib.metadata.distribution('PyInstaller')
    license_file = next(p for p in distribution.files if str(p).endswith('COPYING.txt'))
    shutil.copy2(distribution.locate_file(license_file), notices / 'PyInstaller-COPYING.txt')
    name = archive.stem + '-Setup'
    subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
                    '--onefile', '--windowed', '--noupx',
                    '--name', name, '--paths', str(ROOT),
                    '--distpath', str(archive.parent), '--workpath', str(work / 'objects'),
                    '--specpath', str(work), '--add-data', str(work / 'payload.zip') + ':.',
                    '--add-data', str(notices) + ':runtime-notices',
                    str(ROOT / 'setup_f23b.py')], cwd=ROOT, check=True)
    exe = archive.parent / (name + '.exe')
    digest = hashlib.sha256(exe.read_bytes()).hexdigest()
    checksums = archive.parent / 'SHA256SUMS.txt'
    lines = [line for line in checksums.read_text().splitlines() if not line.endswith('  ' + exe.name)]
    checksums.write_text('\n'.join(lines + [digest + '  ' + exe.name]) + '\n', encoding='utf-8')
    print(exe)
    print(digest)


if __name__ == '__main__':
    main()
