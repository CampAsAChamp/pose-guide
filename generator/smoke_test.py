"""Smoke test for the built pose guide page (../index.html).

Loads the page in headless Chrome twice with the same browser profile and checks
that it works end to end. Needs only the Python standard library and an
installed Chrome (set CHROME=/path/to/chrome to use a different binary).

Steps:
  1. Find a Chrome binary.
  2. Copy index.html into a temp folder with a probe script injected: an error
     hook at the top of <head> and a test script at the end of <body>.
  3. Run 1 (fresh profile): check rendering, filters, search, the viewer and
     the Saved filter, then turn grid lines off and save pose 5.
  4. Run 2 (same profile): check that the grid setting and saved pose survived
     the reload.
  5. Report every check and any console errors; exit 1 if anything failed.

Usage (from generator/):
  python build.py && python smoke_test.py
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.normpath(os.path.join(HERE, "..", "index.html"))
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

# Runs before the app script. Records uncaught errors, rejected promises and
# console.error calls so the probe can report them.
ERROR_HOOK = """<script>
window.__smokeErrors = [];
window.addEventListener('error', function(e){ window.__smokeErrors.push('error: ' + e.message); });
window.addEventListener('unhandledrejection', function(e){ window.__smokeErrors.push('rejection: ' + e.reason); });
(function(){ var orig = console.error; console.error = function(){
  window.__smokeErrors.push('console.error: ' + Array.prototype.join.call(arguments, ' ')); return orig.apply(console, arguments); }; })();
</script>"""

# Runs after the app script. Drives the page like a user and writes results
# into a JSON <script> element, which --dump-dom prints back unescaped.
PROBE = r"""<script>
(async function(){
  var results = [], $ = function(id){ return document.getElementById(id); };
  var sleep = function(ms){ return new Promise(function(r){ setTimeout(r, ms); }); };
  // Headless virtual time skips ahead without painting frames, so CSS transitions never advance on their own.
  // Jump every running animation to its end state before checking a result that depends on one.
  function settle(){ document.getAnimations().forEach(function(a){ try { a.finish(); } catch (e) {} }); }
  function check(name, ok, detail){ results.push({ name: name, ok: !!ok, detail: detail === undefined ? '' : String(detail) }); }
  // cards fading out after a filter change stay in the DOM briefly as li.leaving, so they are not counted
  function poses(){ return document.querySelectorAll('#grid > li:not(.leaving) .pose').length; }
  function finish(){
    var out = document.createElement('script'); out.type = 'application/json'; out.id = 'smoke-result';
    out.textContent = JSON.stringify({ results: results, errors: window.__smokeErrors });
    document.body.appendChild(out);
  }
  try {
    await sleep(200);
    var secondRun = localStorage.getItem('smoke-run') === '1';
    if (!secondRun) {
      localStorage.setItem('smoke-run', '1');
      check('renders 200 poses', poses() === 200, poses());
      check('count text', $('count').textContent === '200 poses', $('count').textContent);
      check('filter panel starts closed', $('filterPanel').hidden && $('filterBtn').getAttribute('aria-expanded') === 'false');
      $('filterBtn').click();
      check('filter button opens panel', !$('filterPanel').hidden && $('filterBtn').getAttribute('aria-expanded') === 'true');

      var chip = document.querySelector('.chip[data-tag="Solo"]');
      check('Solo chip exists', chip);
      chip.click(); await sleep(50);
      var solo = poses();
      check('Solo chip narrows list', solo > 0 && solo < 200, solo);
      check('Clear Filters shown', !$('clear').hidden);
      $('clear').click(); await sleep(50);
      check('Clear Filters restores all', poses() === 200, poses());

      $('q').value = 'bench'; $('q').dispatchEvent(new Event('input')); await sleep(50);
      var bench = poses();
      check('search narrows list', bench > 0 && bench < 200, bench);
      $('clear').click(); await sleep(50);

      // Home resets filters, search and the open filter panel
      $('filterBtn').click(); if ($('filterPanel').hidden) $('filterBtn').click();
      document.querySelector('.chip[data-tag="Solo"]').click(); await sleep(50);
      $('homeBar').click(); await sleep(500); // Clear Filters shrinks away before it is hidden
      check('Home resets filters and closes panel', poses() === 200 && $('filterPanel').hidden && $('clear').hidden, poses());

      location.hash = '#pose-5'; await sleep(200);
      check('#pose-5 opens viewer', $('viewer').open && $('vTitle').textContent.length > 0, $('vTitle').textContent);
      $('vSave').click();
      check('Save pose toggles on', $('vSave').getAttribute('aria-pressed') === 'true' && $('vSaveLabel').textContent === 'Saved', $('vSaveLabel').textContent);
      check('Save pose keeps heart icon', $('vSave').querySelector('svg'));
      $('vNext').click(); await sleep(600);
      check('Next steps to pose 6', location.hash === '#pose-6' && $('vPos').textContent.indexOf('Pose 6') === 0 && !document.querySelector('.art-ghost'), location.hash);
      $('vPrev').click(); await sleep(600);
      check('Previous steps back to pose 5', location.hash === '#pose-5' && $('vSave').getAttribute('aria-pressed') === 'true', location.hash);
      // closing is animated, so allow it time to finish
      location.hash = '#all'; await sleep(600);
      check('#all closes viewer', !$('viewer').open);

      var before = $('gridToggle').getAttribute('aria-checked');
      $('gridToggle').click();
      check('grid toggle flips', $('gridToggle').getAttribute('aria-checked') !== before, before + ' -> ' + $('gridToggle').getAttribute('aria-checked'));
      if ($('gridToggle').getAttribute('aria-checked') === 'true') $('gridToggle').click(); // leave grid lines off for run 2

      check('tag pills on by default', $('tagToggle').getAttribute('aria-checked') === 'true' && document.querySelectorAll('.pose .mp').length === 600, document.querySelectorAll('.pose .mp').length);
      $('tagToggle').click();
      // the pills fold away rather than disappearing at once
      getComputedStyle(document.querySelector('.meta')).maxHeight; settle();
      var firstMeta = document.querySelector('.meta');
      check('tags toggle hides pills', document.body.classList.contains('notags') && firstMeta.offsetHeight === 0 && getComputedStyle(firstMeta).visibility === 'hidden', firstMeta.offsetHeight);
      $('tagToggle').click(); // leave tags on for run 2

      $('savedOnly').click(); await sleep(50);
      check('Saved filter shows saved pose only', poses() === 1, poses());
      $('savedOnly').click(); await sleep(50);
      check('Saved filter off restores all', poses() === 200, poses());
      await sleep(600);
      check('no leftover fading cards', document.querySelectorAll('.leaving').length === 0 && document.querySelectorAll('.pose').length === 200, document.querySelectorAll('.leaving').length);
    } else {
      check('grid setting persisted (off)', $('gridToggle').getAttribute('aria-checked') === 'false', $('gridToggle').getAttribute('aria-checked'));
      check('saved pose persisted', JSON.stringify(JSON.parse(localStorage.getItem('pose-saved') || '[]')) === '[5]', localStorage.getItem('pose-saved'));
      $('savedOnly').click(); await sleep(50);
      check('Saved filter after reload', poses() === 1, poses());
      var card = document.querySelector('#grid > li:not(.leaving) .pose');
      check('saved card shows heart mark', card && card.querySelector('.saved-mark svg'));
    }
  } catch (e) {
    check('probe ran without throwing', false, e && e.stack || e);
  }
  finish();
})();
</script>"""


def log_step(message: str) -> None:
    """Print a progress line to stderr. Inputs: message. Side effects: writes to stderr."""
    print(f"[*] {message}", file=sys.stderr)


def find_chrome() -> str:
    """Return a path to a Chrome/Chromium binary, honouring $CHROME.

    Outputs: the binary path. Side effects: exits with status 1 if none is found.
    """
    override = os.environ.get("CHROME")
    for candidate in ([override] if override else []) + CHROME_CANDIDATES:
        path = candidate if os.path.isabs(candidate) else shutil.which(candidate)
        if path and os.path.exists(path):
            return path
    log_step("FAILED: no Chrome found. Install Chrome or set CHROME=/path/to/chrome.")
    sys.exit(1)


def write_probe_page(workdir: str) -> str:
    """Copy index.html into workdir with the error hook and probe injected.

    Inputs: a temp folder. Outputs: the probe page path. Side effects: writes one file.
    """
    if not os.path.exists(PAGE):
        log_step(f"FAILED: {PAGE} not found. Run python build.py first.")
        sys.exit(1)
    with open(PAGE, encoding="utf-8") as fh:
        page = fh.read()
    # The hook must run before any app code, so it goes right after <head>.
    page = page.replace("<head>", "<head>" + ERROR_HOOK, 1)
    # rpartition targets the page's own closing tag, not any "</body>" text inside the pose data.
    head, sep, tail = page.rpartition("</body>")
    if not sep:
        log_step("FAILED: index.html has no </body> tag.")
        sys.exit(1)
    path = os.path.join(workdir, "smoke.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + PROBE + sep + tail)
    return path


def run_page(chrome: str, profile: str, page: str) -> dict:
    """Load the probe page once in headless Chrome and return its results.

    Inputs: Chrome path, profile folder (shared between runs so localStorage
    carries over), probe page path. Outputs: {"results": [...], "errors": [...]}.
    """
    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
        f"--user-data-dir={profile}",
        # Virtual time lets the probe's timers and hash changes finish without real waiting.
        "--virtual-time-budget=10000",
        "--dump-dom", "file://" + page,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    match = re.search(r'<script type="application/json" id="smoke-result">(.*?)</script>', proc.stdout, re.S)
    if not match:
        return {"results": [{"name": "probe finished", "ok": False, "detail": "no result in page output"}], "errors": []}
    # --dump-dom prints <script> text raw, so the JSON needs no unescaping.
    return json.loads(match.group(1))


def report(label: str, outcome: dict) -> int:
    """Print one run's checks and errors. Inputs: run label, run outcome. Outputs: failure count."""
    failures = 0
    for r in outcome["results"]:
        mark = "PASS" if r["ok"] else "FAIL"
        failures += 0 if r["ok"] else 1
        detail = f"  ({r['detail']})" if r["detail"] and not r["ok"] else ""
        print(f"  {mark}  {label}: {r['name']}{detail}")
    for e in outcome["errors"]:
        failures += 1
        print(f"  FAIL  {label}: {e}")
    return failures


def main() -> None:
    # Step 1: find Chrome.
    log_step("Step 1/4: finding Chrome")
    chrome = find_chrome()

    with tempfile.TemporaryDirectory(prefix="pose-smoke-") as workdir:
        profile = os.path.join(workdir, "profile")

        # Step 2: write the instrumented copy of the page.
        log_step("Step 2/4: preparing probe page")
        page = write_probe_page(workdir)

        # Step 3: first load, fresh profile.
        log_step("Step 3/4: run 1 (fresh profile)")
        first = run_page(chrome, profile, page)

        # Step 4: second load with the same profile to check persistence.
        log_step("Step 4/4: run 2 (after reload)")
        second = run_page(chrome, profile, page)

    failures = report("run 1", first) + report("run 2", second)
    total = len(first["results"]) + len(second["results"])
    if failures:
        log_step(f"FAILED: {failures} problem(s) across {total} checks")
        sys.exit(1)
    log_step(f"Done: all {total} checks passed, no console errors")


if __name__ == "__main__":
    main()
