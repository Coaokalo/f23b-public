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
```

The installer tests use temporary fixtures. They do not patch an installed game.
Hosted CI runs these checks on Windows and Linux. The full native bridge and
real SDK checks require a local Windows installation.

## Private preview packaging

`tools/package_preview.py` combines an exact previously prepared runtime ZIP
with the committed source, content corrections and a private visual-model
overlay. The input is the September 15 accepted aircraft archive, pinned in
`config/releases/preview-baseline.json`;
the three revised models are pinned in `config/releases/asset-fixes.json`.
It preserves the flight code and installer bytes, verifies the committed source,
and creates aircraft/source ZIPs and SHA-256 checksums in an ignored output folder.
Pillow renders the original menu graphics from code; no old artwork is used.
Quick Start mission corrections update the briefing and required Core/Player
plugin identities while preserving the payloads, triggers and other mission data.

```powershell
python -m pip install -r requirements-release.txt
python -B tools/package_preview.py --runtime-input "PATH/TO/F23B-Burner-Assemblies-0eab91677b32.zip" --asset-overlay "PATH/TO/YF23-HORNET-VISUAL-OUTPUT"
```

Only the two aircraft folders are read from the private runtime archive; private
source archives and development receipts are excluded from the public download.
The runtime input and revised visual models are private release inputs and are
not downloaded by CI. The Blender source for these licensed derivatives remains
private; it is not corresponding software source for the flight bridge.
Packaging produces a draft candidate; it does not change GitHub visibility or
publish a release. A different compiler may produce a different DLL hash from
the retained preview binary even when building the corresponding source.

## Windows setup executable

After committing the source and packaging the aircraft as above:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-setup.txt
.venv/Scripts/python.exe tools/build_setup.py --aircraft-zip "PATH/TO/F23B-preview-2026-09-17.zip"
```

The build uses [PyInstaller](https://pyinstaller.org/en/stable/usage.html) to bundle
Python, Tk, the existing patcher and the exact aircraft ZIP into one setup EXE.
Only builders install these dependencies. The EXE and its checksum are placed
beside the aircraft/source archives. The payload must match the committed source.
The GUI requests administrator access; command-line fixture runs can operate
without elevation in temporary folders. Setup never downloads code at runtime.
The executable is unsigned unless a release maintainer signs it separately.
