# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run locally (Windows):**
```bash
setup.bat    # first-time: creates venv and installs dependencies
run.bat      # starts Flask dev server at http://localhost:5000
```

**Run locally (macOS/Linux):**
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Regenerate the static site** (must be done after any template, CSS, JS, or portfolio data change before committing):
```bash
python generate_static.py
```

**Manually trigger view count update:**
```bash
python update_view_count.py
```

**Run tests:**
```bash
py -m pip install -r requirements-dev.txt   # first time only
py -m pytest                                # run all 32 tests
py -m pytest tests/test_app.py             # routes + persistence only
py -m pytest tests/test_update_view_count.py  # update script only
```

## Architecture

This project has two runtime modes that share the same template and data:

### 1. Flask app (`app.py`)
Serves the portfolio dynamically. Portfolio content lives entirely in `DEFAULT_PORTFOLIO` (a large dict defined in `app.py`). Updating content means editing that dict, then regenerating the static site. The Flask app is not deployed publicly — it is only used for local development and as the import source for `generate_static.py`.

### 2. Static site (`docs/`)
The live site is served via **GitHub Pages** from the `docs/` folder on the `main` branch of `sivahari1983/My-Profile`. `generate_static.py` renders the Jinja2 template in a Flask app context, rewrites all `/static/` paths to relative `static/` paths, and copies `static/` assets into `docs/static/`. **Always run `generate_static.py` and commit `docs/` after any change to `templates/`, `static/`, or `DEFAULT_PORTFOLIO`.**

### 3. View count (`view_count.json`)
Persistent counter stored in `view_count.json`. GitHub Actions (`.github/workflows/update-view-count.yml`) runs hourly, increments the count, calls `generate_static.py`, and commits the result. The frontend JS reads the live count directly from the GitHub raw content URL:
```
https://raw.githubusercontent.com/sivahari1983/My-Profile/main/view_count.json
```
A `Math.max` guard in the JS ensures the displayed count never decreases even if the raw file lags the baked-in HTML value.

### Git remotes
| Remote | Repo | Purpose |
|---|---|---|
| `upstream` | `sivahari1983/My-Profile` | Live site (GitHub Pages) — push here to deploy |
| `origin` | `fit824/My-Profile` | Fork used for PRs |

Push to `upstream main` to deploy directly, or push to `origin main` and open a PR.

## Key Files

| File | Role |
|---|---|
| `app.py` | `DEFAULT_PORTFOLIO` dict + Flask routes + view count API |
| `generate_static.py` | Renders template → `docs/index.html`, copies assets |
| `update_view_count.py` | Increments `view_count.json`, calls `generate_static.py` |
| `templates/index.html` | Single Jinja2 template for the entire page |
| `static/css/style.css` | All styling via CSS custom properties (`:root` variables) |
| `static/js/main.js` | Interactivity + view count fetch from GitHub raw URL |
| `docs/` | Generated output — do not edit manually |
| `view_count.json` | Live view counter database |

## Theming

All colours are CSS custom properties in the `:root` block at the top of `static/css/style.css`. Change colours there and the hardcoded `rgba(...)` values below them in the same file — then run `generate_static.py` to sync to `docs/`.

## Playwright UI Testing

After any change to `templates/`, `static/css/style.css`, or `static/js/main.js`, verify the UI using the Playwright MCP tools (`mcp__playright__*`) before committing. The Flask server must be running first.

**Start the server (Windows):**
```bash
C:\Users\hnataraj\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe app.py
```

**Standard verification flow:**
1. `mcp__playright__browser_navigate` → `http://localhost:5000`
2. `mcp__playright__browser_take_screenshot` — confirm page loads
3. `mcp__playright__browser_snapshot` — inspect element roles and links
4. `mcp__playright__browser_evaluate` — run JS assertions (scroll position, href values, DOM structure)
5. `mcp__playright__browser_wait_for` — wait for smooth-scroll animations (`time: 1.5`)
6. `mcp__playright__browser_resize` → `{ width: 375, height: 812 }` — test mobile layout
7. `mcp__playright__browser_console_messages` — check for JS errors

**Screenshots:**
Save verification screenshots to `tests/screenshots/` (tracked in git). Root-level `*.png` files are gitignored. Embed screenshots in `task.md` as test evidence after each feature change.

**Notes:**
- Flask in non-debug mode caches templates per process. If the served HTML does not reflect template edits, kill all Python processes and restart the server fresh via PowerShell: `Get-Process python* | Stop-Process -Force`
- Smooth-scroll uses `e.preventDefault()` so `window.location.hash` is not updated — use `window.scrollY` to assert navigation worked
- Playwright screenshots and `.playwright-mcp/` temp folder are gitignored at the root level

## Deployment Flow

```
Edit DEFAULT_PORTFOLIO or templates/static
        ↓
python generate_static.py
        ↓
git add . && git commit && git push upstream main
        ↓
GitHub Pages serves docs/ immediately
GitHub Actions runs hourly to update view_count.json
```
