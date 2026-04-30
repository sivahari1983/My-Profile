---
name: Button shadow effects feature
description: Shadow hover/active states added to .btn-primary, .btn-secondary, .nav-toggle, #back-top — verified clean 2026-04-30
type: project
---

All four button/interactive elements now have layered box-shadow states:

- `.btn-primary` — base `0px 4px 20px rgba(22,163,74,0.3)`, hover `0px 8px 30px rgba(22,163,74,0.4)`, active `0px 12px 36px rgba(22,163,74,0.55)`
- `.btn-secondary` — no base shadow, hover `0px 4px 16px rgba(22,163,74,0.15)`, active `0px 6px 22px rgba(22,163,74,0.28)`
- `.nav-toggle` — hover `0px 2px 10px rgba(22,163,74,0.18)`, active `0px 4px 16px rgba(22,163,74,0.35)` + `translateY(1px)`
- `#back-top` — base `0px 4px 20px rgba(34,197,94,0.3)`, hover `0px 8px 30px rgba(34,197,94,0.5)`, active `0px 14px 40px rgba(34,197,94,0.65)`

**Why:** Improve interactive affordance — buttons should feel tactile with depth changes on state transitions.

**How to apply:** When testing button interactions, verify computed box-shadow deepens progressively from base -> hover -> active. Use CSSOM (iterate sheet.cssRules) for pseudo-class state verification since Playwright's getComputedStyle loses hover state between hover() and evaluate() calls.
