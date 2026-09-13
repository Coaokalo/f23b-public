# SPDX-License-Identifier: MIT
"""Prepare a private preview from pinned runtime bytes and committed source."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

from verify_source import verify

ROOT = Path(__file__).resolve().parents[1]
NAME = 'F23B-preview-2026-09-13'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def zip_bytes(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 9, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-input', type=Path, required=True)
    args = parser.parse_args()
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT).strip():
        raise SystemExit('Commit the source changes before packaging')
    verify()
    baseline = json.loads((ROOT / 'config/releases/preview-baseline.json').read_text())
    raw = args.runtime_input.read_bytes()
    if sha(raw) != baseline['input_archive_sha256']:
        raise SystemExit('Runtime input does not match the pinned archive')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if len(z.namelist()) != len(set(z.namelist())):
            raise SystemExit('Duplicate runtime archive entries')
        files = {n: z.read(n) for n in z.namelist()}
    if set(files) != set(baseline['files']) | {'release.json'}:
        raise SystemExit('Runtime inventory differs from the pinned baseline')
    for name, expected in baseline['files'].items():
        if sha(files[name]) != expected:
            raise SystemExit(f'Runtime hash mismatch: {name}')
    module_files = {n: b for n, b in files.items() if n.startswith(('F-23B/', 'F-23B-Player/'))}
    if len(module_files) != 62:
        raise SystemExit('Expected 62 aircraft module files')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    source = subprocess.check_output(['git', 'archive', '--format=zip', 'HEAD'], cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(source)) as z:
        source_files = {n: z.read(n) for n in z.namelist() if not n.endswith('/')}
    for name, data in module_files.items():
        source_name = 'Mods/aircraft/' + name
        if source_name in source_files and source_files[source_name] != data:
            raise SystemExit(f'Corresponding Lua/config differs: {name}')
    if files['native_patch.py'] != source_files['native_patch.py']:
        raise SystemExit('Installer source mismatch')
    for name in ['COPYING', 'LICENSE', 'LICENSE-ASSETS.md', 'THIRD_PARTY_NOTICES.md',
                 'INSTALL.md', 'LICENSES/MIT.txt', 'config/licensing/third-party-code-reuse.json',
                 'experiments/flight-feel/docs/provenance/GRINNELLI_V2_1_PERFORMANCE_REFERENCE.md']:
        files[name] = source_files[name]
    files['NOTICES.md'] = (
        '# F-23B experimental preview\n\n'
        'THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.\n\n'
        'Requires an installed, activated DCS: F/A-18C Hornet. Read INSTALL.md.\n'
        'Software: GPL-3.0-or-later with retained file-level MIT grants.\n'
        'Visual derivatives: SytaPastel YF-23 and nobatgeldi F-35 Cockpit, CGTrader.\n'
        'See THIRD_PARTY_NOTICES.md and LICENSE-ASSETS.md for attribution and terms.\n'
        'Private draft: distribution review and final installation checks are pending.\n'
    ).encode()
    files['SOURCE.md'] = (
        '# Corresponding software source\n\n'
        f'Companion archive: `{NAME}-source.zip`.\n\n'
        f'Repository: https://github.com/Coaokalo/f23b-public/tree/{commit}\n\n'
        'The companion contains source, build scripts, tests, license notices, and\n'
        'BUILDING.md. SDK headers and licensed visual sources are external inputs.\n'
        f'Source archive SHA-256: `{sha(source)}`.\n'
    ).encode()
    manifest = {k: v for k, v in baseline.items() if k not in {'files', 'input_archive_sha256'}}
    manifest.update(kind='PRIVATE_DRAFT_PREVIEW', publication_status='PRIVATE_DRAFT',
                    source_repository='https://github.com/Coaokalo/f23b-public',
                    corresponding_source_commit=commit, release_tooling_source=commit,
                    corresponding_source_archive=NAME + '-source.zip',
                    corresponding_source_sha256=sha(source),
                    files={n: sha(b) for n, b in sorted(files.items()) if n != 'release.json'})
    files['release.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    assert all(files[n] == data for n, data in module_files.items())
    output = ROOT / 'dist' / NAME / commit[:12]
    output.mkdir(parents=True, exist_ok=True)
    aircraft = zip_bytes(files)
    assets = {NAME + '.zip': aircraft, NAME + '-source.zip': source}
    for name, data in assets.items():
        path = output / name
        if path.exists() and path.read_bytes() != data:
            raise SystemExit(f'Output already exists with different bytes: {path.name}')
        path.write_bytes(data)
    checksums = ''.join(f'{sha(data)}  {name}\n' for name, data in sorted(assets.items()))
    (output / 'SHA256SUMS.txt').write_text(checksums, encoding='utf-8')
    (output / 'RELEASE_NOTES.md').write_bytes(source_files['docs/RELEASE_NOTES.md'])
    print(f'PASS: 62 unchanged aircraft files; source commit {commit}')
    print(output)
    print(checksums)


if __name__ == '__main__':
    main()
