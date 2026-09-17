# SPDX-License-Identifier: MIT
"""Self-contained F-23B setup; uses the existing native missile installer."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile
import zipfile

import native_patch

MODULES = ('F-23B', 'F-23B-Player')
STATE = '.f23b-install'


def unpack(archive, destination):
    with zipfile.ZipFile(archive) as source:
        names = source.namelist()
        if len(names) != len(set(n.lower() for n in names)):
            raise ValueError('Duplicate package entries')
        for name in names:
            parts = PurePosixPath(name).parts
            if not parts or name.startswith('/') or '\\' in name or ':' in name or '..' in parts:
                raise ValueError('Invalid package path')
        source.extractall(destination)
    release = json.loads((destination / 'release.json').read_text(encoding='utf-8'))
    for name, expected in release['files'].items():
        path = destination / name
        if not path.resolve().is_relative_to(destination.resolve()):
            raise ValueError('Invalid manifest path')
        if native_patch.sha(path.read_bytes()) != expected:
            raise ValueError('Damaged download: ' + name)
    actual = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
    if actual != set(release['files']) | {'release.json'}:
        raise ValueError('Package inventory mismatch')
    for module in MODULES:
        if not (destination / module / 'entry.lua').is_file():
            raise ValueError('Incomplete aircraft download')
    return release


def regular_tree(path, recursive=True):
    if path.is_symlink() or path.resolve() != path.absolute():
        raise ValueError('Setup will not replace linked folders: ' + str(path))
    if path.exists() and recursive:
        for child in path.rglob('*'):
            if child.is_symlink() or child.resolve() != child.absolute():
                raise ValueError('Setup will not replace linked files: ' + str(child))


def perform(action, dcs, profile, archive):
    native_patch.ensure_closed()
    dcs, profile = dcs.resolve(strict=True), profile.resolve(strict=True)
    if dcs == profile or profile.is_relative_to(dcs) or dcs.is_relative_to(profile):
        raise ValueError('Choose the DCS game folder and a separate Saved Games DCS profile')
    if not (profile / 'Config').is_dir() and not (profile / 'Logs').is_dir():
        raise ValueError('Choose your Saved Games DCS profile (the folder containing Config or Logs)')
    aircraft = profile / 'Mods/aircraft'
    state = profile / STATE
    regular_tree(aircraft, recursive=False)
    regular_tree(state)
    receipt_path = state / 'receipt.json'
    receipt = json.loads(receipt_path.read_text()) if receipt_path.is_file() else None
    if state.exists() and not receipt:
        raise ValueError('An incomplete installation record exists at ' + str(state))
    if receipt and (receipt['dcs_root'] != str(dcs) or receipt['profile'] != str(profile)):
        raise ValueError('This installation belongs to a different DCS folder or profile')
    if action == 'remove' and not receipt:
        raise ValueError('No installation managed by this setup was found in that profile')
    for module in MODULES:
        target = aircraft / module
        regular_tree(target)
        if target.exists() and not receipt:
            raise ValueError('Move the existing ' + module + ' folder to a backup location first. Setup will not overwrite an unmanaged installation.')
        if target.exists():
            for path in target.rglob('*'):
                if path.is_file():
                    name = module + '/' + path.relative_to(target).as_posix()
                    if name not in receipt['files']:
                        raise ValueError('Preserve this added file outside the module before continuing: ' + str(path))
                    if action == 'remove' and native_patch.sha(path.read_bytes()) != receipt['files'][name]:
                        raise ValueError('Preserve this changed file before removing the module: ' + str(path))
    work = Path(tempfile.mkdtemp(prefix='.f23b-setup-', dir=profile))
    moved, installed = [], []
    cleanup = True
    try:
        package = work / 'package'
        package.mkdir()
        release = unpack(archive, package)
        if receipt and receipt['source_commit'] != release['corresponding_source_commit']:
            raise ValueError('Remove the previous release with its original installer before changing releases')
        if action == 'install':
            staged_state = work / STATE
            staged_state.mkdir()
            record = dict(dcs_root=str(dcs), profile=str(profile),
                          source_commit=release['corresponding_source_commit'],
                          files={n: h for n, h in release['files'].items()
                                 if n.split('/')[0] in MODULES})
            (staged_state / 'receipt.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
            # Keep the release identity and install instructions available after setup.
            for name in ('release.json', 'INSTALL.md', 'NOTICES.md', 'SOURCE.md',
                         'COPYING', 'LICENSE', 'LICENSE-ASSETS.md', 'THIRD_PARTY_NOTICES.md'):
                if (package / name).is_file():
                    shutil.copy2(package / name, staged_state / name)
            if (package / 'LICENSES').is_dir():
                shutil.copytree(package / 'LICENSES', staged_state / 'LICENSES')
            runtime_notices = Path(__file__).resolve().parent / 'runtime-notices'
            if runtime_notices.is_dir():
                shutil.copytree(runtime_notices, staged_state / 'runtime-notices')
        aircraft.mkdir(parents=True, exist_ok=True)
        # Retain the existing installation until BOTH native files pass preflight.
        # If the patcher refuses or a move fails, put every old folder back.
        try:
            for target in [aircraft / n for n in MODULES] + [state]:
                if target.exists():
                    backup = work / ('previous-' + target.name)
                    target.rename(backup)
                    moved.append((backup, target))
            if action == 'install':
                for module in MODULES:
                    target = aircraft / module
                    (package / module).rename(target)
                    installed.append(target)
                staged_state.rename(state)
                installed.append(state)
                # Weapon definitions are now in their installed location.
                patch_package = work / 'patch'
                (patch_package / 'F-23B/Weapons').mkdir(parents=True)
                shutil.copy2(package / 'release.json', patch_package / 'release.json')
                for _, project, *_ in native_patch.SPECS.values():
                    shutil.copy2(aircraft / 'F-23B/Weapons' / project,
                                 patch_package / 'F-23B/Weapons' / project)
                native_patch.run('install', dcs, patch_package)
            else:
                native_patch.run('restore', dcs, package)
        except Exception:
            # A failed rollback must leave the retained folders available to recover.
            cleanup = False
            for target in reversed(installed):
                target.rename(work / ('failed-' + target.name))
            for backup, target in reversed(moved):
                backup.rename(target)
            cleanup = True
            raise
    finally:
        if cleanup:
            shutil.rmtree(work, ignore_errors=True)
    if action == 'remove':
        return 'F-23B removed and original missile files restored. Your controls and missions were kept.'
    return 'F-23B installed, including custom weapons. Start DCS and select an F-23B Quick Start mission.'


def defaults():
    profile = Path.home() / 'Saved Games/DCS'
    dcs = ''
    if os.name == 'nt':
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders') as key:
                saved = Path(os.path.expandvars(winreg.QueryValueEx(key, '{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}')[0]))
                profiles = [saved / n for n in ('DCS', 'DCS.openbeta') if (saved / n).is_dir()]
                profile = profiles[0] if profiles else saved / 'DCS'
        except OSError:
            pass
        for key_name in (r'Software\Eagle Dynamics\DCS World', r'Software\Eagle Dynamics\DCS World OpenBeta'):
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name) as key:
                    dcs = winreg.QueryValueEx(key, 'Path')[0]
                    break
            except OSError:
                pass
    return dcs, str(profile)


def gui(archive):
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    import threading
    import queue

    root = tk.Tk()
    root.title('F-23B Setup')
    root.resizable(False, False)
    frame = ttk.Frame(root, padding=24)
    frame.grid()
    ttk.Label(frame, text='F-23B Black Widow II', font=('Segoe UI', 18, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w')
    ttk.Label(frame, text='Experimental preview • Aircraft and custom weapons', padding=(0, 6, 0, 14)).grid(row=1, column=0, columnspan=2, sticky='w')
    entries = []
    for row, (label, value) in enumerate(zip(('DCS game folder', 'Saved Games DCS profile'), defaults())):
        ttk.Label(frame, text=label).grid(row=2 + row * 2, column=0, sticky='w')
        entry = ttk.Entry(frame, width=65)
        entry.insert(0, value)
        entry.grid(row=3 + row * 2, column=0, pady=(4, 12))
        def browse(field=entry):
            folder = filedialog.askdirectory(parent=root, title='Select folder')
            if folder:
                field.delete(0, tk.END)
                field.insert(0, folder)
        ttk.Button(frame, text='Browse…', command=browse).grid(row=3 + row * 2, column=1, padx=(10, 0), pady=(4, 12))
        entries.append(entry)
    ttk.Label(frame, wraplength=550, text='Requires DCS 2.9.29.27468 and an installed, activated F/A-18C Hornet. Close DCS before continuing.\n\nInstalls custom missiles by changing AIM-120B and AIM-9X for all aircraft. Original files are backed up. This can affect multiplayer integrity checks.').grid(row=6, column=0, columnspan=2, sticky='w', pady=(0, 18))
    status = tk.StringVar(value='Ready. No separate Python installation is needed.')
    ttk.Label(frame, textvariable=status, wraplength=550).grid(row=8, column=0, columnspan=2, sticky='w', pady=(16, 0))
    results = queue.Queue()
    busy = False
    def finish():
        nonlocal busy
        try:
            ok, text = results.get_nowait()
        except queue.Empty:
            root.after(100, finish)
            return
        busy = False
        install.config(state='normal')
        remove.config(state='normal')
        status.set(text if ok else 'Setup did not complete. See the message for details.')
        (messagebox.showinfo if ok else messagebox.showerror)('F-23B Setup', text, parent=root)
    def start(action):
        nonlocal busy
        paths = [e.get().strip() for e in entries]
        if not all(paths):
            messagebox.showerror('F-23B Setup', 'Select both folders first.', parent=root)
            return
        if action == 'remove' and not messagebox.askyesno('Remove F-23B', 'Remove both aircraft folders and restore the original missile files?', parent=root):
            return
        busy = True
        install.config(state='disabled')
        remove.config(state='disabled')
        status.set('Installing aircraft and weapons…' if action == 'install' else 'Removing aircraft and restoring weapons…')
        def worker():
            try:
                results.put((True, perform(action, Path(paths[0]), Path(paths[1]), archive)))
            except Exception as exc:
                results.put((False, str(exc)))
        threading.Thread(target=worker, daemon=True).start()
        root.after(100, finish)
    install = ttk.Button(frame, text='Install / Repair', command=lambda: start('install'))
    install.grid(row=7, column=0, sticky='w')
    remove = ttk.Button(frame, text='Remove', command=lambda: start('remove'))
    remove.grid(row=7, column=1, sticky='e')
    root.protocol('WM_DELETE_WINDOW', lambda: None if busy else root.destroy())
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--action', choices=('install', 'remove'))
    parser.add_argument('--dcs-root', type=Path)
    parser.add_argument('--profile', type=Path)
    parser.add_argument('--result', type=Path)
    args = parser.parse_args()
    archive = Path(__file__).resolve().parent / 'payload.zip'
    if not args.action:
        # Elevate the interactive installer; automated fixture runs need no admin.
        if os.name == 'nt' and getattr(sys, 'frozen', False):
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                result = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, None, None, 1)
                if result <= 32:
                    ctypes.windll.user32.MessageBoxW(None, 'Setup needs administrator permission to update the DCS weapon files. Run setup again to continue.', 'F-23B Setup', 0x10)
                return
        gui(archive)
        return
    if not args.dcs_root or not args.profile or not args.result:
        parser.error('Automated setup requires --dcs-root, --profile and --result')
    try:
        message = perform(args.action, args.dcs_root, args.profile, archive)
        result = dict(ok=True, message=message)
    except Exception as exc:
        result = dict(ok=False, message=str(exc))
    args.result.write_text(json.dumps(result, indent=2), encoding='utf-8')
    sys.exit(0 if result['ok'] else 1)


if __name__ == '__main__':
    main()
