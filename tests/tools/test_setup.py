# SPDX-License-Identifier: MIT
"""Installation transactions use temporary game/profile fixtures only."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import setup_f23b as setup
import test_native_installer as native_tests
installer = native_tests.installer


class SetupTests(unittest.TestCase):
    def setUp(self):
        native_tests.NativeInstallerTests.setUp(self)
        self.profile = self.dcs.parent / 'Saved Games/DCS'
        (self.profile / 'Config').mkdir(parents=True)
        (self.profile / 'Config/controls.txt').write_bytes(b'preserved controls')
        (self.profile / 'Missions').mkdir()
        (self.profile / 'Missions/owner.miz').write_bytes(b'preserved mission')
        for module in setup.MODULES:
            entry = self.package / module / 'entry.lua'
            entry.parent.mkdir(parents=True, exist_ok=True)
            entry.write_bytes(b'fixture aircraft')
        self.cockpit = self.dcs / setup.COCKPIT_SCRIPT
        self.cockpit.parent.mkdir(parents=True, exist_ok=True)
        self.cockpit.write_bytes(b'fixture cockpit')
        (self.package / 'independent-weapons.json').write_text(json.dumps(dict(
            version='fixture', binaries={'Mods/aircraft/FA-18C/bin/FA18C.dll': installer.sha(b'fixture')},
            cockpit_script_sha256=installer.sha(b'fixture cockpit'))))
        files = {p.relative_to(self.package).as_posix(): installer.sha(p.read_bytes())
                 for p in self.package.rglob('*') if p.is_file() and p.name != 'release.json'}
        (self.package / 'release.json').write_text(json.dumps(dict(files=files, corresponding_source_commit='fixture')))
        self.archive = self.dcs.parent / 'payload.zip'
        with zipfile.ZipFile(self.archive, 'w') as z:
            for path in self.package.rglob('*'):
                if path.is_file():
                    z.write(path, path.relative_to(self.package).as_posix())
        for p in (patch.object(setup, 'native_patch', installer), patch.object(installer, 'ensure_closed')):
            p.start()
            self.addCleanup(p.stop)

    def setup_action(self, action):
        return setup.perform(action, self.dcs, self.profile, self.archive)

    def run_action(self, action):
        return installer.run(action, self.dcs, self.package)

    def test_complete_install_repair_remove_preserves_user_files(self):
        self.setup_action('install')
        target = self.profile / 'Mods/aircraft/F-23B/entry.lua'
        target.write_bytes(b'damaged')
        self.setup_action('install')
        self.assertEqual(target.read_bytes(), b'fixture aircraft')
        self.assertEqual(self.cockpit.read_bytes(), b'fixture cockpit' + setup.HOOK)
        for kind, path in self.targets.items():
            self.assertEqual(path.read_bytes(), self.bases[kind])
        self.setup_action('remove')
        for module in setup.MODULES:
            self.assertFalse((self.profile / 'Mods/aircraft' / module).exists())
        self.assertFalse((self.profile / setup.STATE).exists())
        self.assertEqual(self.cockpit.read_bytes(), b'fixture cockpit')
        for kind, path in self.targets.items():
            self.assertEqual(path.read_bytes(), self.bases[kind])
        self.assertEqual((self.profile / 'Config/controls.txt').read_bytes(), b'preserved controls')
        self.assertEqual((self.profile / 'Missions/owner.miz').read_bytes(), b'preserved mission')

    def test_unsupported_game_rolls_back_new_modules(self):
        self.targets['ir'].write_bytes(b'unsupported')
        with self.assertRaises(ValueError):
            self.setup_action('install')
        self.assertFalse((self.profile / 'Mods/aircraft/F-23B').exists())
        self.assertFalse((self.profile / setup.STATE).exists())
        self.assertEqual(self.targets['radar'].read_bytes(), self.bases['radar'])

    def test_failed_repair_preserves_existing_installation(self):
        self.setup_action('install')
        before = (self.profile / setup.STATE / 'receipt.json').read_bytes()
        self.targets['ir'].write_bytes(b'updated by DCS')
        with self.assertRaises(ValueError):
            self.setup_action('install')
        self.assertEqual((self.profile / setup.STATE / 'receipt.json').read_bytes(), before)
        self.assertTrue((self.profile / 'Mods/aircraft/F-23B/entry.lua').is_file())

    def test_remove_refusal_restores_module_folders(self):
        self.setup_action('install')
        self.cockpit.write_bytes(self.cockpit.read_bytes() + b'changed hook')
        with self.assertRaises(ValueError):
            self.setup_action('remove')
        self.assertTrue((self.profile / 'Mods/aircraft/F-23B/entry.lua').is_file())
        self.assertTrue((self.profile / setup.STATE / 'receipt.json').is_file())

    def test_unmanaged_install_and_added_files_are_preserved(self):
        folder = self.profile / 'Mods/aircraft/F-23B'
        folder.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'unmanaged'):
            self.setup_action('install')
        folder.rmdir()
        self.setup_action('install')
        added = folder / 'owner.txt'
        added.write_bytes(b'keep me')
        for action in ('install', 'remove'):
            with self.assertRaisesRegex(ValueError, 'added file'):
                self.setup_action(action)
        self.assertEqual(added.read_bytes(), b'keep me')

    def test_upgrade_restores_legacy_missiles_and_replaces_receipt(self):
        self.run_action('install')
        self.setup_action('install')
        record = self.profile / setup.STATE / 'receipt.json'
        receipt = json.loads(record.read_text())
        receipt['source_commit'] = setup.LEGACY_RELEASE
        record.write_text(json.dumps(receipt))
        self.run_action('install')
        self.setup_action('install')
        self.assertEqual(json.loads(record.read_text())['source_commit'], 'fixture')
        for kind, path in self.targets.items():
            self.assertEqual(path.read_bytes(), self.bases[kind])

    def test_cockpit_write_failure_rolls_back_legacy_restoration_and_modules(self):
        self.run_action('install')
        before = {kind: path.read_bytes() for kind, path in self.targets.items()}
        original = installer.atomic_write
        def fail_hook(path, data):
            if path == self.cockpit:
                raise OSError('simulated cockpit write failure')
            return original(path, data)
        with patch.object(installer, 'atomic_write', fail_hook):
            with self.assertRaisesRegex(OSError, 'simulated'):
                self.setup_action('install')
        for kind, path in self.targets.items():
            self.assertEqual(path.read_bytes(), before[kind])
        self.assertEqual(self.cockpit.read_bytes(), b'fixture cockpit')
        self.assertFalse((self.profile / setup.STATE).exists())
        self.assertFalse((self.profile / 'Mods/aircraft/F-23B').exists())

    def test_unsupported_binary_does_not_change_game_or_modules(self):
        (self.dcs / 'Mods/aircraft/FA-18C/bin/FA18C.dll').write_bytes(b'new version')
        with self.assertRaisesRegex(ValueError, 'requires DCS'):
            self.setup_action('install')
        self.assertEqual(self.cockpit.read_bytes(), b'fixture cockpit')
        self.assertFalse((self.profile / setup.STATE).exists())

    def test_remove_after_game_update_keeps_updated_native_files(self):
        self.setup_action('install')
        self.cockpit.write_bytes(b'new DCS cockpit')
        self.targets['ir'].write_bytes(b'new DCS missile')
        self.setup_action('remove')
        self.assertEqual(self.cockpit.read_bytes(), b'new DCS cockpit')
        self.assertEqual(self.targets['ir'].read_bytes(), b'new DCS missile')


if __name__ == '__main__':
    unittest.main()
