# CM Toolkit (merged app)

Merges three previously separate Kivy apps into one APK with a top nav bar:

- **CM/DX** (`cmdx_tab.py`) — condition monitoring diagnostics
- **Rotor Balance** (`rotor_tab.py`) — single-plane balancing calculator
- **Bearing Freq** (`bearing_tab.py` + `bearing_data.py`) — bearing defect frequency scope

`main.py` is the only new file with real logic — it's a thin launcher that
instantiates each original app's `App` subclass, grabs its `.build()` root
widget, and drops it into its own `Screen` inside one `ScreenManager`. None
of the three apps' internal code was rewritten; each keeps its own classes,
math, and UI logic completely separate in its own module.

## What changed vs. the original repos
- `rotor_tab.py`: removed one line — a module-level `Window.clearcolor = ...`
  that would have overridden the color of whichever tab loaded last. The
  merged app now sets the window background per-tab from `main.py` on switch.
- Everything else (bearing_tab.py, bearing_data.py, cmdx_tab.py) is byte-for-byte
  the original source, just renamed from `main.py` to `<name>_tab.py`.

## Setting this up as its own GitHub repo
1. Create a new repo (e.g. `CM-Toolkit`) on GitHub.
2. Upload every file in this folder, preserving the `.github/workflows/build.yml` path.
3. Push to `main` — the Action builds a debug APK and uploads it as an artifact
   named `cm-toolkit-apk` (Actions tab → latest run → Artifacts).

## Local sanity check (optional, no Android tooling needed)
```
python3 -c "import ast; [ast.parse(open(f).read()) for f in ['main.py','cmdx_tab.py','rotor_tab.py','bearing_tab.py','bearing_data.py']]"
python3 -c "import bearing_data; print(len(bearing_data.DATA['data']), 'brands loaded')"
```

## If a tab crashes on device
The launcher wraps each tab's build in a try/except, so one broken tab
shows a red error screen with the traceback instead of crashing the whole
app — screenshot that screen and it'll be easy to diagnose.

## Update 2: fault recommendations + editable library
- Added the gearbox recommendations to the **Gear mesh wear or misalignment**
  fault, and the base-rigidity recommendations to the **Structural / bolting
  looseness** fault, in `cmdx_tab.py`'s `BASE_FAULTS` list.
- The CM/DX Library tab now has:
  - **+ Add** button to create a brand-new fault entry (name, technique,
    causes, recommendations).
  - **Edit** button inside each fault's detail popup to change its name,
    causes, or recommendations.
  - Your edits and additions are saved to `cmdx_library_overrides.json` in
    the app's private data folder, so they survive app updates/restarts.
    `BASE_FAULTS` in the code stays untouched — edits are layered on top.
  - Note: newly-added faults are searchable in the Library but won't
    auto-match in the Wizard's spectrum-tag scoring (that requires wiring
    signature tags into the code) — editing an *existing* fault keeps its
    original tags, so its wizard matching still works.

## Update 3: app icon
- Replaced `icon.png` with the new "CM Toolkit" artwork (also used as
  `presplash.png`, shown while Android loads the app, with a matching white
  background via `android.presplash_color` in `buildozer.spec`).
- `main.py`'s `CMToolkitApp` now sets `icon = "icon.png"` so it's used
  consistently as the launcher icon, task icon, and window icon.
