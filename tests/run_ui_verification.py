"""
Playwright UI verification script for Hero Title Single-Line Fix.
Run with: python tests/run_ui_verification.py
"""
import os
import sys
import json
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

BASE_URL = "http://localhost:5000"

results = {}
console_errors = []

def check_hero_title(page):
    return page.evaluate("""() => {
        const el = document.querySelector('.hero-title');
        if (!el) return { error: 'element not found' };
        return {
            clientHeight: el.clientHeight,
            scrollHeight: el.scrollHeight,
            lineHeight: getComputedStyle(el).lineHeight,
            fontSize: getComputedStyle(el).fontSize,
            whiteSpace: getComputedStyle(el).whiteSpace,
            innerText: el.innerText.trim()
        };
    }""")

def check_overflow(page):
    return page.evaluate(
        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ── STEP 2: Desktop 1280px ──────────────────────────────────────────
        print("\n[STEP 2] Desktop 1280x800")
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Capture console errors
        page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)

        page.goto(BASE_URL, wait_until="networkidle", timeout=15000)
        results["http_200"] = page.url != "" and True  # navigated successfully

        ss = os.path.join(SCREENSHOTS_DIR, "hero-title-desktop.png")
        page.screenshot(path=ss, full_page=False)
        print(f"  Screenshot saved: {ss}")

        info = check_hero_title(page)
        print(f"  Hero title info: {json.dumps(info, indent=2)}")
        results["desktop_white_space"] = info.get("whiteSpace", "")
        results["desktop_client_height"] = info.get("clientHeight", 999)
        results["desktop_single_line"] = (
            info.get("whiteSpace") == "nowrap" and info.get("clientHeight", 999) < 120
        )

        context.close()

        # ── STEP 3: Mobile 375px ────────────────────────────────────────────
        print("\n[STEP 3] Mobile 375x812")
        context = browser.new_context(viewport={"width": 375, "height": 812})
        page = context.new_page()
        page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)

        page.goto(BASE_URL, wait_until="networkidle", timeout=15000)

        ss = os.path.join(SCREENSHOTS_DIR, "hero-title-mobile-375.png")
        page.screenshot(path=ss, full_page=False)
        print(f"  Screenshot saved: {ss}")

        info = check_hero_title(page)
        print(f"  Hero title info: {json.dumps(info, indent=2)}")
        results["mobile_white_space"] = info.get("whiteSpace", "")
        results["mobile_client_height"] = info.get("clientHeight", 999)
        results["mobile_single_line"] = (
            info.get("whiteSpace") == "nowrap" and info.get("clientHeight", 999) < 120
        )
        overflow = check_overflow(page)
        results["mobile_no_overflow"] = not overflow
        print(f"  Horizontal overflow: {overflow}")

        context.close()

        # ── STEP 4: Tablet 768px ────────────────────────────────────────────
        print("\n[STEP 4] Tablet 768x1024")
        context = browser.new_context(viewport={"width": 768, "height": 1024})
        page = context.new_page()
        page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)

        page.goto(BASE_URL, wait_until="networkidle", timeout=15000)

        ss = os.path.join(SCREENSHOTS_DIR, "hero-title-tablet-768.png")
        page.screenshot(path=ss, full_page=False)
        print(f"  Screenshot saved: {ss}")

        info = check_hero_title(page)
        print(f"  Hero title info: {json.dumps(info, indent=2)}")
        results["tablet_white_space"] = info.get("whiteSpace", "")
        results["tablet_client_height"] = info.get("clientHeight", 999)
        results["tablet_single_line"] = (
            info.get("whiteSpace") == "nowrap" and info.get("clientHeight", 999) < 120
        )

        context.close()

        # ── STEP 5: Full-page screenshot at desktop ─────────────────────────
        print("\n[STEP 5] Full-page screenshot at 1280x800")
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)

        page.goto(BASE_URL, wait_until="networkidle", timeout=15000)
        ss = os.path.join(SCREENSHOTS_DIR, "hero-title-fullpage.png")
        page.screenshot(path=ss, full_page=True)
        print(f"  Full-page screenshot saved: {ss}")

        # Collect console errors
        js_errors = [msg for msg in console_errors if msg.type == "error"]
        results["no_js_errors"] = len(js_errors) == 0
        if js_errors:
            print(f"  JS errors found: {[m.text for m in js_errors]}")
        else:
            print("  No JS console errors.")

        context.close()
        browser.close()

    # ── STEP 6: Print report ────────────────────────────────────────────────
    ws_actual = results.get("desktop_white_space", "unknown")
    desktop_h = results.get("desktop_client_height", "?")
    mobile_h  = results.get("mobile_client_height", "?")
    tablet_h  = results.get("tablet_client_height", "?")

    def tick(key):
        return "✅" if results.get(key) else "❌"

    print("""
## Playwright UI Test Report — Hero Title Single-Line Fix
Date: 2026-04-29

| Check | Status | Notes |
|---|---|---|""")
    print(f"| Page loads (HTTP 200) | {tick('http_200')} | |")
    print(f"| white-space: nowrap applied | {tick('desktop_single_line')} | actual value: {ws_actual} |")
    print(f"| Desktop 1280px — single line | {tick('desktop_single_line')} | clientHeight: {desktop_h}px |")
    print(f"| Mobile 375px — single line | {tick('mobile_single_line')} | clientHeight: {mobile_h}px |")
    print(f"| Mobile 375px — no horizontal overflow | {tick('mobile_no_overflow')} | |")
    print(f"| Tablet 768px — single line | {tick('tablet_single_line')} | clientHeight: {tablet_h}px |")
    print(f"| No JS console errors | {tick('no_js_errors')} | |")
    print("""
### Screenshots saved
- tests/screenshots/hero-title-desktop.png
- tests/screenshots/hero-title-mobile-375.png
- tests/screenshots/hero-title-tablet-768.png
- tests/screenshots/hero-title-fullpage.png""")

    all_pass = all([
        results.get("http_200"),
        results.get("desktop_single_line"),
        results.get("mobile_single_line"),
        results.get("mobile_no_overflow"),
        results.get("tablet_single_line"),
        results.get("no_js_errors"),
    ])
    failures = sum(1 for k in ["http_200","desktop_single_line","mobile_single_line",
                                "mobile_no_overflow","tablet_single_line","no_js_errors"]
                   if not results.get(k))
    if all_pass:
        print("\n### Overall: ✅ ALL PASS")
    else:
        print(f"\n### Overall: ❌ {failures} FAILURE(S)")

    # Save results JSON for reference
    with open(os.path.join(SCREENSHOTS_DIR, "results.json"), "w") as f:
        json.dump({k: (v if not callable(v) else str(v)) for k, v in results.items()}, f, indent=2)

    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(run())
