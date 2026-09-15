# SPDX-License-Identifier: MIT
import io
import json
from pathlib import Path
import re
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from release_assets import (fix_mission, MISSION_TEXT_OLD, MISSION_TEXT_NEW,
                            MISSION_MODULES_OLD, MISSION_MODULES_NEW)


class ContentTests(unittest.TestCase):
    def test_mission_requirements_match_plugins_and_other_content_is_preserved(self):
        original = ('mission = {descriptionText="' + MISSION_TEXT_OLD + '",'
                    'descriptionBlueTask="' + MISSION_TEXT_OLD + '",'
                    + MISSION_MODULES_OLD + ','
                    'payload="{F23B-AIM424-MALICE}",triggers={1,2,3}}').encode()
        members = {'mission': original, 'options': b'options = {}',
                   'l10n/DEFAULT/mapResource': b'mapResource = {}'}
        source = io.BytesIO()
        with zipfile.ZipFile(source, 'w') as z:
            for n, data in members.items():
                z.writestr(n, data)
        with zipfile.ZipFile(io.BytesIO(fix_mission(source.getvalue()))) as z:
            self.assertEqual(set(z.namelist()), set(members))
            corrected = z.read('mission')
            plugin_ids = set()
            for module in ('F-23B', 'F-23B-Player'):
                entry = (ROOT / 'Mods/aircraft' / module / 'entry.lua').read_text()
                plugin_ids.add(re.search(r'local self_ID = "([^"]+)"', entry).group(1))
            requirements = re.search(rb'\["requiredModules"\]\s*=\s*\{([^}]+)\}', corrected).group(1)
            self.assertEqual(set(re.findall(r'=\s*"([^"]+)"', requirements.decode())), plugin_ids)
            restored = corrected.replace(MISSION_TEXT_NEW.encode(), MISSION_TEXT_OLD.encode())
            restored = restored.replace(MISSION_MODULES_NEW.encode(), MISSION_MODULES_OLD.encode())
            self.assertEqual(restored, original)
            for n in members.keys() - {'mission'}:
                self.assertEqual(z.read(n), members[n])

    def test_changed_mission_format_is_not_silently_rewritten(self):
        source = io.BytesIO()
        with zipfile.ZipFile(source, 'w') as z:
            z.writestr('mission', 'mission = {descriptionText="different revision"}')
        with self.assertRaises(ValueError):
            fix_mission(source.getvalue())

    def test_unexpected_module_requirements_are_rejected(self):
        source = io.BytesIO()
        with zipfile.ZipFile(source, 'w') as z:
            z.writestr('mission', 'mission = {descriptionText="' + MISSION_TEXT_OLD
                       + '",descriptionBlueTask="' + MISSION_TEXT_OLD
                       + '",["requiredModules"] = { ["different"] = "different" }}')
        with self.assertRaisesRegex(ValueError, 'module requirements'):
            fix_mission(source.getvalue())

    def test_every_distance_model_is_pinned_and_distances_increase(self):
        text = (ROOT / 'Mods/aircraft/F-23B/Shapes/F-23B.lods').read_text()
        entries = re.findall(r'\{"([^"]+\.edm)",\s*([\d.]+)\}', text)
        models = json.loads((ROOT / 'config/releases/asset-fixes.json').read_text())['visual_models']
        self.assertEqual({'F-23B/Shapes/'+name for name, _ in entries}, set(models))
        distances = [float(distance) for _, distance in entries]
        self.assertEqual(distances, sorted(set(distances)))
        self.assertGreaterEqual(len(entries), 3)


if __name__ == '__main__':
    unittest.main()
