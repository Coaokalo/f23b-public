# Install or remove the F-23B preview

Requires Windows, **DCS World 2.9.29.27468**, an installed and activated
**DCS: F/A-18C Hornet**, and **Python 3.11 or later** for the missile installer.
Other DCS versions are not qualified. The installer checks the actual native
weapon files and refuses unknown versions.

Installation has two required parts: **copy both aircraft folders**, then
**install and verify the missile patch**. The patch changes **AIM-120B and AIM-9X
globally**, including other aircraft, and may fail multiplayer integrity checks.
AIM-120C remains unchanged. Removal instructions are below.

This is an experimental preview for single-player use. See
[known limitations](https://github.com/Coaokalo/f23b-public/blob/main/KNOWN_ISSUES.md)
for flight, VR, multiplayer, and weapon limitations.

## Install

1. Download **F23B-preview-2026-09-13.zip** from
   [Releases](https://github.com/Coaokalo/f23b-public/releases) and extract it completely.
   GitHub's automatic “Source code” archives are not the aircraft download.
2. Close DCS, its updater and ModelViewer. Move any existing `F-23B` and
   `F-23B-Player` folders to a backup location outside `Mods/aircraft`.
   Copy both new folders into `%USERPROFILE%\Saved Games\DCS\Mods\aircraft`.
   Use your actual Saved Games profile if it is named `DCS.openbeta` or differs.
   Do not merge old files into the new folders. Keep your `Config/Input` mappings.
3. In the extracted download, open a terminal and run the following, replacing
   the DCS path with your installation directory:

   ```powershell
   python native_patch.py install --dcs-root "D:\Eagle Dynamics\DCS World"
   python native_patch.py verify --dcs-root "D:\Eagle Dynamics\DCS World"
   ```

   Both commands must report PASS. If Windows denies access to the DCS folder,
   run the terminal as administrator and repeat. Keep this extracted release
   for verification and rollback.
4. Start DCS normally. Select the F-23B and an included Quick Start mission,
   or use an F-23B mission with the MALICE/Block II payload. Existing Hornet
   controls apply. Selecting a missile leaves the bay closed; one trigger press
   opens the bay, sends the native release command and closes the bay.

DCS repair or updates may remove the missile patches; run verification again
afterward. The installer checks your local DCS files and refuses unknown versions.
No ED native source or binary is included: it uses your own installation.

## Remove or roll back

Close DCS and run this from the original extracted release:

```powershell
python native_patch.py restore --dcs-root "D:\Eagle Dynamics\DCS World"
```

Then remove the two F-23B module folders from Saved Games, or restore your prior
module backup and its matching native patch. Original native files and checksums
are retained in `F23B-native-backup` inside the DCS installation. The script
refuses to overwrite files changed by an update or another mod. If DCS already
restored the stock files, restore is harmless. Keep backups until rollback is
complete; a different F-23B weapon revision requires restoring the old release first.

## Troubleshooting

- Aircraft absent: check that both folders sit directly inside `Mods/aircraft`,
  with `entry.lua` immediately inside each; check Hornet installation/activation.
- Aircraft present but missiles wrong: run native patch verification and choose
  a matching F-23B payload. Installing Saved Games folders alone is insufficient.
- Unsupported native file: restore other missile modifications or use DCS repair,
  then check whether your DCS version is supported. Do not bypass the checksum.
- [Bug reports](https://github.com/Coaokalo/f23b-public/issues/new?template=bug_report.yml):
  include the build ID from `release.json`, DCS version, mission,
  steps to reproduce and the relevant `Saved Games/DCS/Logs/dcs.log` excerpt.
  Remove personal paths or account details before posting.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
