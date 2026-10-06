# SPDX-License-Identifier: MIT
"""Compare a release ZIP with a clean setup fixture, by complete file set and SHA-256."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def inventory(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file()}


def compare(archive, profile):
    with zipfile.ZipFile(archive) as source:
        expected = {n: hashlib.sha256(source.read(n)).hexdigest()
                    for n in source.namelist() if not n.endswith('/')}
    actual = inventory(profile)
    difference = {
        'missing': sorted(expected.keys() - actual.keys()),
        'extra': sorted(actual.keys() - expected.keys()),
        'changed': sorted(n for n in actual.keys() & expected.keys() if actual[n] != expected[n]),
    }
    if any(difference.values()):
        raise ValueError(json.dumps(difference, indent=2))
    return {'result': 'PASS', 'files': len(expected), 'sha256': expected}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--aircraft-zip', type=Path, required=True)
    parser.add_argument('--profile', type=Path, required=True,
                        help='A clean fixture, with no unrelated user files')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = compare(args.aircraft_zip, args.profile)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: all {result["files"]} installed files equal the ZIP by path and SHA-256')
