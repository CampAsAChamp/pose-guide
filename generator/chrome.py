"""Find and run a headless Chrome. Shared by smoke_test.py and preview.py.

Set CHROME=/path/to/chrome to choose the binary, and CHROME_FLAGS to add
switches (CI sets CHROME_FLAGS=--no-sandbox, which Linux runners need).
"""
from __future__ import annotations

import os
import shlex
import shutil
import sys

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]


def find_chrome() -> str:
    """Return a path to a Chrome/Chromium binary, honouring $CHROME.

    Outputs: the binary path. Side effects: exits with status 1 if none is found.
    """
    override = os.environ.get("CHROME")
    for candidate in ([override] if override else []) + CHROME_CANDIDATES:
        path = candidate if os.path.isabs(candidate) else shutil.which(candidate)
        if path and os.path.exists(path):
            return path
    print("[*] FAILED: no Chrome found. Install Chrome or set CHROME=/path/to/chrome.", file=sys.stderr)
    sys.exit(1)


def headless_cmd(profile: str) -> list:
    """The start of a headless Chrome command line using a throwaway profile folder.

    Inputs: profile folder (a separate profile avoids clashing with a running Chrome).
    Outputs: argument list; callers append their own switches and the URL.
    """
    return [find_chrome(), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
            f"--user-data-dir={profile}"] + shlex.split(os.environ.get("CHROME_FLAGS", ""))
