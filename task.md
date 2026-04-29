# Task Tracker

## Nav Link + Mobile Navigation Fix

- [x] Add `Certifications` link to top navbar (`templates/index.html`)
- [x] Fix mobile hamburger button — add JS click handler to toggle nav open/close (`static/js/main.js`)
- [x] Add `.nav-menu.open` CSS rule for mobile expanded state (`static/css/style.css`)
- [x] Regenerate static site (`python generate_static.py`)
- [x] Verify on desktop — Certifications link scrolls to section, active highlight works
- [x] Verify on mobile — hamburger opens/closes nav, links close menu on click
- [x] Commit and push to deploy

## Playwright MCP — UI Verification (Ongoing)

Use the `mcp__playright__*` tools to visually verify UI changes before committing. Run these checks after any change to `templates/`, `static/css/style.css`, or `static/js/main.js`.

### Checklist (run after each UI change)

- [ ] Start local Flask server (`python app.py` or `run.bat`)
- [ ] Navigate to `http://localhost:5000` via `mcp__playright__browser_navigate`
- [ ] Take a screenshot (`mcp__playright__browser_take_screenshot`) to confirm page loads correctly
- [ ] Check desktop nav — all links visible, active highlight on scroll (`mcp__playright__browser_snapshot`)
- [ ] Check mobile nav — resize to 375px (`mcp__playright__browser_resize`), open hamburger, verify menu opens/closes
- [ ] Click each nav link and verify it scrolls to the correct section
- [ ] Check Certifications section renders and is reachable via nav
- [ ] Review browser console for JS errors (`mcp__playright__browser_console_messages`)
- [ ] Capture network requests to confirm view count fetch succeeds (`mcp__playright__browser_network_requests`)
- [ ] Regenerate static site (`python generate_static.py`) and navigate to `docs/index.html` to verify parity
- [ ] Take final screenshot and compare with previous for regressions
