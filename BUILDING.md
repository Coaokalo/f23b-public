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
with the committed source and updated release documentation. Its input hash is
pinned in `config/releases/preview-baseline.json`. It preserves all aircraft
module files and installer bytes, verifies the committed source snapshot, and
creates aircraft/source ZIPs and SHA-256 checksums in an ignored output folder.

```powershell
python -B tools/package_preview.py --runtime-input "PATH/TO/F23B-preview-4c254be08a8d.zip"
```

The runtime input is a private release input and is not downloaded by CI.
Packaging produces a draft candidate; it does not change GitHub visibility or
publish a release. A different compiler may produce a different DLL hash from
the retained preview binary even when building the corresponding source.
