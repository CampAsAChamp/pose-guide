# Photo Pose Guide

A single self-contained static page, `index.html` (about 4 MB), with 200 illustrated photo poses for solo, partner and group shots. Each pose has a posing tip and a framing tip. It is published with GitHub Pages from the root of `main`.

There is no framework or runtime dependency. The only external resources are two Google Fonts (Bricolage Grotesque for headings, Instrument Sans for body text), with system-font fallbacks. Keep it a single file that works when opened directly from disk.

## index.html is a build output

Do not hand-edit the pose data in `index.html`. It is generated from `generator/`:

- Edit the Python in `generator/poses/`, or the page itself: `generator/template.html` (HTML), `generator/styles.css` (CSS) and `generator/app.js` (JS). `build.py` inlines the CSS and JS, so the output stays one file.
- Check poses with `python preview.py <numbers> --png` (run from `generator/`). It screenshots with the same Chrome as the smoke test.
- Run `python build.py` to regenerate `../index.html`. It first runs the data checks in `generator/checks.py` and writes nothing if any fail.
- Run `python smoke_test.py` (from `generator/`) after building. It loads the page twice in headless Chrome, checks filters, search, the viewer and saving, confirms state survives a reload, and fails on any console error. It needs only an installed Chrome (or `CHROME=/path/to/chrome`).
- Read `generator/README.md` first. It documents the camera, scene, pose-dictionary and `@card` APIs.
- Setup: `pip install -r generator/requirements.txt` (NumPy only). `generator/.venv` is git-ignored.
- CI (`.github/workflows/check.yml`) rebuilds on every push and fails if the result differs from the committed `index.html`, then runs the smoke test. Commit `index.html` with the generator change that produced it.

**Pose numbers are permanent.** Every card states its number in its decorator, `@card(201, "Title", ...)`. A new pose takes the next unused number (add it at the end of `poses/cards_i.py`, or in a new module added to the import line in `poses/catalog.py`). Then run `python build.py --lock` once to record the number and title in `generator/pose_numbers.json`. A normal build fails if a recorded number disappears or changes title, because `#pose-N` links would then point at a different pose. Run `--lock` again only for a deliberate rename.

## Data format

All pose data is one JSON object in `<script id="poses" type="application/json">` near the end of `index.html`. The JSON escapes `</` as `<\/`.

- `groups`: the filter groups, in order:
  - People: Solo, Partner, Group
  - Pose: Standing, Leaning, Walking, Seated, Crouching, Lying, Action, Mixed Levels
  - Shot: Wide, Full Length, Three-Quarter, Waist Up, Close-Up
  - Setting: Street, Park, Beach, Field, Viewpoint, Waterfront, Steps, Café, Home, Studio
  - Angle: Facing Camera, Side-On, Back to Camera
- `cards`: 200 objects, each with:
  - `n`: pose number (1 to 200)
  - `t`: title
  - `g`: tags, exactly one per group, in the order People, Pose, Shot, Setting, Angle
  - `p`: pose tip (one or two sentences)
  - `f`: framing tip (one or two sentences)
  - `a`: the illustration as inner SVG markup for a 600 x 800 viewBox (3:4 portrait)
  - `d` (optional): a description of the drawing for screen readers, used in the drawing's label. Only cards with a hand-written `alt=` have one (currently 1 to 64).

Use typographic apostrophes and quotes in visible text. The build turns `'` into `’` and rejects straight `"`.

## Page behaviour

- Filter chips show a count per tag. Tags within a group widen the match (OR). Tags across groups narrow it (AND). The search box matches title, tips and tags.
- Every filter group label has a small line icon. People, Shot and Angle chips also have icons (head counts, crop size, facing direction), set in `TAG_ICONS` in `generator/app.js`. Pose and Setting chips are text only on purpose: their icons would be vague at chip size.
- Thumbnails are drawn only near the viewport (IntersectionObserver), to keep 200 SVGs fast.
- Clicking a pose opens a `<dialog>` viewer with the large drawing, tags, both tips, a thirds-grid toggle, Save, and Previous/Next, which step through the current filter. Arrow keys and swipes also step.
- `#pose-N` opens a pose and `#all` closes the viewer.
- Each grid card shows its first three tags (People, Pose, Shot) as quiet, non-interactive pills. A "Tags" switch in the bar hides them.
- Saved poses and the grid and tag settings live in localStorage under `pose-saved`, `pose-thirds` and `pose-tags` (tags default to on), wrapped in try/catch. They are per browser and not shared.
- Motion: the filter panel folds open and shut (CSS grid rows; `hidden` is still the state), chips pop when selected, grid cards slide to their new place when the filters change (the 200 `<li>` nodes are built once and reused; filtered-out cards fade as `li.leaving` before removal), the viewer grows from and shrinks back to the pose's thumbnail, and Previous/Next slide the drawing. All of it is skipped under `prefers-reduced-motion`.
- There is one theme, dark, set by CSS custom properties on `:root`. There is no light mode, no `prefers-color-scheme` handling and no theme switch. The layout is responsive and has been checked at 390px and 1280px widths.

## Illustration style (match it for any new or edited art)

- A faceless, jointed 3D artist's mannequin drawn in perspective: capsule-shaped limbs, ball joints, an oval chest and pelvis with a faint centre line, and a head with a lighter face plate and two dot eyes when facing the camera.
- Each part has a dark outline (`#2F3033`), a shade colour and a lit colour offset toward the upper left. Standing figures cast a soft ground shadow (`#20242B` at 0.17 opacity).
- People in one picture use different tints: sand `#F7E9D2`, sky `#CDE5F7`, coral `#FAD4C8`, sage `#D9ECD1`, lilac `#E4DCF4`.
- Backdrops are flat, muted, simple shapes: street, park, beach, field, mountain viewpoint, waterfront railing or pier, steps, café, home interior, plain studio.
- Every frame is portrait 3:4.

## Known weak cards (for touch-ups when asked)

- Weak: 39 Jacket sling, 60 Hands-up line, 62 Café trio, 74 Wall prop, 128 Edge of the bed, 136 Tuck jump, 163 Run together, 179 Peek stack.
- Cluttered: 33 Two rows, 35 Group jump, 36 Sofa stack.

## How to work

- Before editing, summarise the file's structure back to the user in a few lines.
- After any change, check that the JSON still parses and that the page opens without console errors.
- Commit with clear messages. **Do not push until the user says so.**
- This is a personal repo: no Jira ticket, branch or worktree is needed. Commit straight to `main`.
