# Build and test

The aircraft runtime targets Windows x64. Install Visual Studio 2022 with its
C++ build tools, CMake 3.25+, Python 3.11+, and DCS with the activated F/A-18C
Hornet. Use the headers in your own DCS installation; they are not bundled here.

## Flight bridge

From the repository root, replacing the DCS path with your installation:

```powershell
cmake -S experiments/native-force-bridge -B build/native -A x64 -DDCS_ROOT="D:/Eagle Dynamics/DCS World"
cmake --build build/native --config Release
ctest --test-dir build/native -C Release --output-on-failure
```

The library is `build/native/Release/F23B_ForceBridge.dll`. It uses the installed
Hornet's native system callbacks. Building this DLL does not create the complete
aircraft download: licensed visual assets are separate inputs.

## Tests without DCS

The flight-model tests use a project-authored interface stub when DCS headers are
unavailable. The stub tests calculations and integration code, not the real SDK
ABI or flight inside DCS.

```powershell
cmake -S experiments/flight-feel -B build/flight
cmake --build build/flight --config Release
ctest --test-dir build/flight -C Release --output-on-failure
python -B -m unittest discover -s tests/tools -v
python -B tools/verify_source.py
lua tests/lua/radar_upgrade_spec.lua
lua tests/lua/exterior_visual_adapter_spec.lua
lua tests/lua/input_bridge_profile_spec.lua
lua tests/lua/engine_visual_registration_spec.lua
lua tests/lua/malice_blockii_hornet_spec.lua
```

The installer tests use temporary fixtures. They do not patch an installed game.
Hosted CI runs these checks on Windows and Linux. The full native bridge and
real SDK checks require a local Windows installation.

## Native radar helper

`F23B_Radar.dll` connects the project weapons, radar support and SA scale in
memory while an F-23B is flown. It checks the exact DCS binaries in
`config/releases/dcs-requirements.json` before it changes anything, and it
restores the original bytes when the session closes. It needs MinGW-w64 `g++`:

```powershell
./experiments/native-radar/build.ps1
```

The script runs the native test groups and writes the DLL to `build/native-radar`.

## Release packaging

`tools/package_release.py` packages the aircraft module files of the flown
build. `config/releases/release-2026-09-29.json` pins every flown file by
SHA-256 and lists the unused files that the release removes, with reasons.
Every shipped script and configuration file must equal the committed source.
Pillow renders the original menu graphics from code; no old artwork is used.
Quick Start mission corrections update the briefing and required Core/Player
plugin identities while preserving the payloads, triggers and other mission data.

```powershell
python -m pip install -r requirements-release.txt
python -B tools/package_release.py --runtime-dir "PATH/TO/FLOWN/Mods/aircraft"
```

The flown module folders are a private release input and are not downloaded by CI.
They contain the licensed visual derivatives. The Blender source for these
derivatives remains private; it is not corresponding software source.
Both DLLs build from this source to identical code sections. Other sections
contain build paths and timestamps, so whole-file hashes can differ.
Packaging produces a draft candidate; it does not change GitHub visibility or
publish a release.

## Windows setup executable

After committing the source and packaging the aircraft as above:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-setup.txt
.venv/Scripts/python.exe tools/build_setup.py --aircraft-zip "PATH/TO/F23B-2026-09-29.zip"
```

The build uses [PyInstaller](https://pyinstaller.org/en/stable/usage.html) to bundle
Python, Tk, setup and the exact aircraft ZIP into one setup EXE.
Only builders install these dependencies. The EXE and its checksum are placed
beside the aircraft/source archives. The payload must match the committed source.
The GUI requests administrator access so that it can restore game files that
earlier releases changed. Command-line fixture runs can operate without
elevation in temporary folders. Setup never downloads code at runtime.
The executable is unsigned unless a release maintainer signs it separately.

Setup installs only into the Saved Games profile. It adds nothing to the DCS
game folder. It removes the September 18 cockpit connection and restores the
September 17 missile files when they are present.
