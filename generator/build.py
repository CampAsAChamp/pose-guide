"""Render every pose and write the single-file site.

    python build.py                 # writes ../index.html (the repo root, if this folder sits inside the repo)
    python build.py -o site.html    # write somewhere else
    python build.py --only 12 45    # rebuild but print just these cards' titles (quick sanity check)
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from poses.catalog import CARDS, GROUPS  # noqa: E402

SELF_CLOSING = re.compile(r"></(path|rect|circle|line|polygon|ellipse)>")


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def render(fn):
    return SELF_CLOSING.sub("/>", fn())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=os.path.join(HERE, "..", "index.html"))
    ap.add_argument("--only", nargs="*", type=int)
    args = ap.parse_args()

    tidy = lambda s: s.replace("'", "\u2019")
    cards = []
    for stem, num, title, tags, fn, pose, frame, alt in sorted(CARDS, key=lambda c: int(c[1])):
        cards.append({"n": int(num), "t": tidy(title), "g": tags, "p": tidy(pose), "f": tidy(frame), "a": render(fn)})
        if args.only and int(num) in args.only:
            print(num, title, tags)
    data = {"groups": [[g, ts] for g, ts in GROUPS], "cards": cards}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = read("template.html")
    # Inline the stylesheet and script so the page stays one self-contained file.
    page = page.replace("__CSS__", read("styles.css").rstrip("\n"))
    page = page.replace("__JS__", read("app.js").rstrip("\n"))
    page = page.replace("__COUNT__", str(len(cards))).replace("__DATA__", blob)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("wrote %s: %d poses, %.2f MB" % (os.path.normpath(args.out), len(cards), len(page.encode()) / 1e6))


if __name__ == "__main__":
    main()
