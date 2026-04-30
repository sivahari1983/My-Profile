You are orchestrating a UI design and verification pipeline for a Flask portfolio site. Execute each phase in strict order.

The user story or feature request to design is:

---
$ARGUMENTS
---

---

## PHASE 0 — DESIGN SYSTEM CHECK

Before invoking the design agent, read the design system reference:

**File:** `.claude/skills/ui-designer/references/design-system.md`

Extract and hold in context:
- Color tokens (`--green`, `--fg`, `--fg2`, `--r2`, `--t`, etc.)
- Card pattern (background, border, hover lift amount)
- Typography scale (font families, clamp sizes, gradient text pattern)
- Existing section IDs and nav links (to avoid duplicates and choose correct anchor targets)
- Scroll reveal pattern (`.reveal-item` + `.revealed`)
- Responsive breakpoints

Pass this extracted context to the `ux-design-planner` agent in Phase 1. Do not skip this step — designs that ignore the design system will produce mismatched CSS.

---

## PHASE 1 — UX DESIGN (ux-design-planner agent)

Invoke the `ux-design-planner` sub-agent with the input above.

Hand it this exact brief:
> "Produce a full UI design specification for the following user story in the context of a Flask + Jinja2 portfolio site. Use only the design tokens and patterns from the design system below — do not invent new colors, border radii, or transition values. Design system summary: [paste the extracted context from Phase 0]. User story: [paste the input]"

Wait for the agent to return all four sections:
1. Written UI Layout
2. Component List
3. Interaction Flow
4. Coding Checklist

Print the full design spec to the conversation.

**Stop here.** Ask the user:
> "Design spec is ready. Shall I proceed with implementation?"

Do not continue until the user confirms.

---

## PHASE 2 — IMPLEMENTATION (coding)

Using the design spec and coding checklist from Phase 1, make the required code changes. Follow this order:

### 2a. Template changes (`templates/index.html`)
- Add new sections or components as specified in the checklist
- Follow existing Jinja2 patterns (`{% if %}`, `{% for %}`)
- Use existing section structure: `<section id="..." class="...">` with `.container` and `.section-header` inside

### 2b. Data changes (`app.py`)
- If the feature requires new portfolio data, add it to `DEFAULT_PORTFOLIO`
- Follow existing dict structure and naming conventions

### 2c. CSS changes (`static/css/style.css`)
- Add new styles at the end, under a clearly labelled comment block
- Follow the card pattern, typography scale, and color tokens from `.claude/skills/ui-designer/references/design-system.md` (§1 Colors, §4 Card Pattern, §2 Typography)
- Only use CSS custom properties — no hardcoded hex or rgba values for colors already in the design system
- Add `.reveal-item` to new cards (§5 Scroll Reveal)

### 2d. JS changes (`static/js/main.js`)
- Only add JS if the feature requires interactivity beyond existing handlers
- Wrap new JS in an IIFE: `(function() { ... })()`

### 2e. Regenerate static site
Run:
```
C:\Users\hnataraj\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe generate_static.py
```
Confirm output: `Static site generated successfully!`

Print a summary of all files changed before proceeding to Phase 3.

---

## PHASE 3 — UI VERIFICATION (Playwright MCP)

Invoke the `playwright-ui-tester` sub-agent to verify the implementation.

Hand it this brief:
> "Run the full UI verification suite. The feature just implemented is: [one-line summary of what was built]. Pay special attention to verifying the new [section/component name] is visible, correctly styled, and reachable via navigation. Save all screenshots to tests/screenshots/ with descriptive names prefixed with the feature name."

The agent will run these checks using the `mcp__playright__*` tools:

| Step | Tool | What it checks |
|---|---|---|
| 1 | `browser_navigate` → `http://localhost:5000` | Page loads (HTTP 200) |
| 2 | `browser_take_screenshot` | Visual baseline |
| 3 | `browser_snapshot` | DOM structure — nav links, new components |
| 4 | `browser_evaluate` | JS assertions — section IDs, href values, computed styles |
| 5 | `browser_click` + `browser_wait_for` | Smooth-scroll navigation per link |
| 6 | `browser_resize` → `375×812` | Mobile layout — hamburger, nav open/close |
| 7 | `browser_console_messages` | No unexpected JS errors |

Wait for the agent to return its full test report table (✅ PASS / ❌ FAIL per check).

**If any check fails:** fix the issue in Phase 2, re-run `generate_static.py`, then re-run Phase 3.

---

## PHASE 4 — WRAP UP

After all phases complete successfully:

1. Update `task.md` — add a new section for this user story with:
   - The user story text
   - Checklist of all Phase 1 coding checklist items, marked complete
   - Links to Phase 3 screenshots

2. Commit all changes:
   - Stage: `templates/index.html`, `static/css/style.css`, `static/js/main.js` (if changed), `app.py` (if changed), `docs/`, `task.md`, `tests/screenshots/`
   - Commit message format: `feat: <one-line description of what was implemented>`

3. Print a final summary:
   ```
   ## Implementation Complete

   User story: <the story>

   Changes made:
   - <file>: <what changed>

   Test result: ✅ ALL PASS / ❌ X FAILURES

   Screenshots: tests/screenshots/<feature>-*.png
   ```

Do not push or open a PR — leave that for the user to decide.