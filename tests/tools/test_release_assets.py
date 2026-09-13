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
from release_assets import fix_mission, MISSION_TEXT_OLD, MISSION_TEXT_NEW


class ContentTests(unittest.TestCase):
    def test_briefing_update_preserves_payload_triggers_and_other_members(self):
        original = ('mission = {descriptionText="' + MISSION_TEXT_OLD + '",'
                    'descriptionBlueTask="' + MISSION_TEXT_OLD + '",'
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
            self.assertEqual(corrected.replace(MISSION_TEXT_NEW.encode(), MISSION_TEXT_OLD.encode()), original)
            for n in members.keys() - {'mission'}:
                self.assertEqual(z.read(n), members[n])

    def test_changed_mission_format_is_not_silently_rewritten(self):
        source = io.BytesIO()
        with zipfile.ZipFile(source, 'w') as z:
            z.writestr('mission', 'mission = {descriptionText="different revision"}')
        with self.assertRaises(ValueError):
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
