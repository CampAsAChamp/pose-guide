"""Draw a contact sheet of selected poses so you can eyeball new or edited cards.

    python preview.py 12 45 199          # writes preview.html
    python preview.py 12 45 --png        # also screenshots it to preview.png (needs: pip install playwright && playwright install chromium)
    python preview.py --range 190 200
"""
import argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from poses.catalog import CARDS  # noqa: E402

GRID = ('<g stroke="#FFFFFF" stroke-width="1.5" opacity="0.7"><line x1="200" y1="0" x2="200" y2="800"/>'
        '<line x1="400" y1="0" x2="400" y2="800"/><line x1="0" y1="266.7" x2="600" y2="266.7"/>'
        '<line x1="0" y1="533.3" x2="600" y2="533.3"/></g>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nums", nargs="*", type=int)
    ap.add_argument("--range", nargs=2, type=int)
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args()
    want = set(a.nums)
    if a.range:
        want |= set(range(a.range[0], a.range[1] + 1))
    pick = [c for c in sorted(CARDS, key=lambda c: int(c[1])) if not want or int(c[1]) in want]
    cells = "".join(
        '<figure style="margin:0"><svg width="240" height="320" viewBox="0 0 600 800">%s%s</svg>'
        '<figcaption style="font:13px system-ui">%s %s</figcaption></figure>' % (c[4](), GRID, c[1], c[2]) for c in pick)
    html = '<body style="margin:0;padding:10px;background:#888;display:flex;flex-wrap:wrap;gap:10px">%s</body>' % cells
    out = os.path.join(HERE, "preview.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, "with", len(pick), "poses")
    if a.png:
        from playwright.sync_api import sync_playwright
        cols = min(6, len(pick)) or 1
        rows = (len(pick) + cols - 1) // cols
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={"width": 20 + cols * 250, "height": 20 + rows * 352})
            pg.goto("file://" + out)
            pg.screenshot(path=os.path.join(HERE, "preview.png"))
            b.close()
        print("wrote preview.png")


if __name__ == "__main__":
    main()
