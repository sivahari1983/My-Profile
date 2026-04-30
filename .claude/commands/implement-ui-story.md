You are orchestrating a three-phase UI implementation pipeline for a Flask portfolio site. Execute each phase in strict order — do not skip or combine phases.

The user story to implement is:

---
$ARGUMENTS
---

---

## PHASE 1 — UX DESIGN (ux-design-planner agent)

Invoke the `ux-design-planner` sub-agent with the user story above.

Hand it this exact brief:
> "Produce a full UI design specification for the following user story in the context of a Flask + Jinja2 portfolio site that uses CSS custom properties for theming (defined in `static/css/style.css` `:root` block) and a single-page layout with smooth-scroll anchor navigation. The design must align with the existing green-themed design system. User story: [paste the user story]"

Wait for the agent to return all four sections:
1. Written UI Layout
2. Component List
3. Interaction Flow
4. Coding Checklist

Do not proceed to Phase 2 until the full design spec is returned. Print the design spec to the conversation so the user can review it.

---

## PHASE 2 — IMPLEMENTATION (coding)

Using the design spec and coding checklist from Phase 1 as your implementation guide, make the required code changes to this project. Follow this order:

### 2a. Template changes (`templates/index.html`)
- Add any new sections, components, or structural HTML as specified in the checklist
- Follow the existing Jinja2 template patterns (conditional blocks with `{% if %}`, loops with `{% for %}`)
- Use existing section structure as a reference: `<section id="..." class="...">` with `.container` and `.section-header` inside

### 2b. Data changes (`app.py`)
- If the feature requires new portfolio data, add it to `DEFAULT_PORTFOLIO` in `app.py`
- Follow the existing dict structure and naming conventions

### 2c. CSS changes (`static/css/style.css`)
- Add new styles at the end of the file, grouped under a clearly labelled comment block
- Use existing CSS custom properties from `:root` (e.g. `var(--green)`, `var(--r2)`, `var(--t)`, `var(--fg)`, `var(--fg2)`)
- Match existing patterns: card styles use `backdrop-filter`, hover uses `transform: translateY(-4px)`
- Add `.reveal-item` class to new cards so the intersection observer animates them in

### 2d. JS changes (`static/js/main.js`)
- Only add JS if the feature requires interactivity beyond what existing handlers cover
- Wrap new JS in an IIFE: `(function() { ... })()`

### 2e. Regenerate static site
Run:
```
C:\Users\hnataraj\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe generate_static.py
```

Confirm output: `Static site generated successfully!`

Print a summary of all files changed before proceeding to Phase 3.

---

## PHASE 3 — UI VERIFICATION (playwright-ui-tester agent)

Invoke the `playwright-ui-tester` sub-agent to verify the implementation.

Hand it this brief:
> "Run the full UI verification suite. The feature just implemented is: [one-line summary of what was built]. Pay special attention to verifying the new [section/component name] is visible, correctly styled, and reachable via navigation. Save all screenshots to tests/screenshots/ with descriptive names prefixed with the feature name."

Wait for the agent to return its full test report table.

---

## PHASE 4 — WRAP UP

After all three phases complete:

1. Update `task.md` — add a new section for this user story with:
   - The user story text
   - A checklist of all items from the Phase 1 coding checklist, marked complete
   - Links to the Phase 3 screenshots

2. Commit all changes on the current branch:
   - Stage: `templates/index.html`, `static/css/style.css`, `static/js/main.js` (if changed), `app.py` (if changed), `docs/`, `task.md`, `tests/screenshots/`
   - Commit message format: `feat: <one-line description of what was implemented>`

3. Print a final summary:
   ```
   ## Implementation Complete

   User story: <the story>

   Changes made:
   - <file>: <what changed>
   - ...

   Test result: ✅ ALL PASS / ❌ X FAILURES

   Screenshots: tests/screenshots/<feature>-*.png
   ```

Do not push or open a PR — leave that for the user to review and decide.
