# SPDX-License-Identifier: MIT
"""Deterministic preview content fixes and original menu graphics."""
import io
import zipfile

F35_TEXTURE_PREFIX = 'F-23B/Textures/F23A_V11_'
MISSION_TEXT_OLD = 'Coffin load: 2x AIM-9X, 3x AIM-120C'
MISSION_TEXT_NEW = 'Bay load: 2x AIM-9X Block II, 3x AIM-424 MALICE'
MISSION_MODULES_OLD = '["requiredModules"] = { ["F-23B"] = "F-23B" }'
MISSION_MODULES_NEW = ('["requiredModules"] = { ["F-23B Core"] = "F-23B Core", '
                       '["F-23B Player"] = "F-23B Player" }')


def fix_mission(data):
    """Correct briefing and plugin requirements; preserve other mission content."""
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(data)) as source:
        text = source.read('mission').decode('utf-8')
        if text.count(MISSION_TEXT_OLD) != 2:
            raise ValueError('Unexpected Quick Start briefing; refusing a broad replacement')
        if text.count(MISSION_MODULES_OLD) != 1:
            raise ValueError('Unexpected Quick Start module requirements')
        text = text.replace(MISSION_TEXT_OLD, MISSION_TEXT_NEW)
        text = text.replace(MISSION_MODULES_OLD, MISSION_MODULES_NEW)
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as target:
            for item in source.infolist():
                target.writestr(item, text.encode('utf-8') if item.filename == 'mission'
                               else source.read(item.filename))
    return output.getvalue()


def branding():
    """Draw original UI graphics; no photographs, vendor art, or font files copied."""
    from PIL import Image, ImageDraw, ImageFont

    def make(width, height, icon=False):
        image = Image.new('RGB', (width, height), '#0b1520')
        draw = ImageDraw.Draw(image)
        gold = '#d5b577'
        if icon:
            margin = max(2, width // 16)
            draw.rounded_rectangle((margin, margin, width-margin-1, height-margin-1),
                                   radius=width//7, outline=gold, width=max(1, width//64))
            font = ImageFont.load_default(size=max(10, int(width*.37)))
            draw.text((width/2, height/2), '23', font=font, fill=gold, anchor='mm')
        else:
            # Original geometric mark, drawn in normalized coordinates.
            silhouette = [(0,-1),(.09,-.22),(.72,.55),(.33,.42),(.21,.76),
                          (.10,.58),(0,.68),(-.10,.58),(-.21,.76),(-.33,.42),
                          (-.72,.55),(-.09,-.22)]
            scale = height*.30
            points = [(width*.72+x*scale,height*.44+y*scale) for x,y in silhouette]
            draw.polygon(points, fill='#192d3c')
            draw.line(points+[points[0]], fill='#34505f', width=max(1,width//900))
            left = int(width*.085)
            draw.line((left,height*.26,left+width*.055,height*.26), fill=gold,
                      width=max(2,height//230))
            draw.text((left,height*.34), 'F-23B',
                      font=ImageFont.load_default(size=int(height*.12)), fill=gold)
            draw.text((left,height*.50), 'BLACK WIDOW II',
                      font=ImageFont.load_default(size=int(height*.040)), fill='#e7edf0')
            draw.text((left,height*.80), 'EXPERIMENTAL COMMUNITY AIRCRAFT',
                      font=ImageFont.load_default(size=int(height*.019)), fill='#91a3ad')
            draw.text((left,height*.84), 'DCS WORLD / F/A-18C REQUIRED',
                      font=ImageFont.load_default(size=int(height*.016)), fill='#91a3ad')
        stream = io.BytesIO()
        image.save(stream, format='PNG', optimize=False)
        return stream.getvalue()

    files = {}
    background = make(1920, 1080)
    for name in ['BackGround-F-23B.png', 'MainMenulogo.png', 'base-menu-window.png',
                 'briefing-map-default.png', 'loading-window.png']:
        files['F-23B/Theme/ME/'+name] = background
    for name, size in [('icon 76x76.png',76), ('icon-38x38.png',38), ('icon.png',256),
                       ('icon_active.png',256), ('icon_select.png',256)]:
        files['F-23B/Theme/'+name] = make(size, size, icon=True)
    files['F-23B/Encyclopedia/Plane/F-23B/F-23B.png'] = make(1280, 720)
    return files
