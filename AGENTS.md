# Photo pose guide

A single self-contained static page, `index.html` (about 4 MB), with 200 illustrated photo poses for solo, partner and group shots. Each pose has a posing tip and a framing tip. It is published with GitHub Pages from the root of `main`.

There is no framework or runtime dependency. The only external resources are two Google Fonts (Bricolage Grotesque for headings, Instrument Sans for body text), with system-font fallbacks. Keep it a single file that works when opened directly from disk.

## index.html is a build output

Do not hand-edit the pose data in `index.html`. It is generated from `generator/`:

- Edit the Python in `generator/poses/` (or `generator/template.html` for the page's HTML, CSS and JS).
- Check poses with `python preview.py <numbers> --png` (run from `generator/`).
- Run `python build.py` to regenerate `../index.html`.
- Read `generator/README.md` first. It documents the camera, scene, pose-dictionary and `@card` APIs.
- Setup: `pip install -r generator/requirements.txt` (NumPy only). `generator/.venv` is git-ignored.

**Always add new poses after the existing ones** (end of `poses/cards_i.py`, or a new module imported last in `poses/catalog.py`). Cards are numbered by registration order, so inserting one earlier breaks `#pose-N` links.

## Data format

All pose data is one JSON object in `<script id="poses" type="application/json">` near the end of `index.html`. The JSON escapes `</` as `<\/`.

- `groups`: the filter groups, in order:
  - People: Solo, Partner, Group
  - Pose: Standing, Leaning, Walking, Seated, Crouching, Lying, Action, Mixed levels
  - Shot: Wide, Full length, Three-quarter, Waist up, Close-up
  - Setting: Street, Park, Beach, Field, Viewpoint, Waterfront, Steps, Café, Home, Studio
  - Angle: Facing camera, Side-on, Back to camera
- `cards`: 200 objects, each with:
  - `n`: pose number (1 to 200)
  - `t`: title
  - `g`: tags, exactly one per group, in the order People, Pose, Shot, Setting, Angle
  - `p`: pose tip (one or two sentences)
  - `f`: framing tip (one or two sentences)
  - `a`: the illustration as inner SVG markup for a 600 x 800 viewBox (3:4 portrait)

Use typographic apostrophes in visible text.

## Page behaviour

- Filter chips show a count per tag. Tags within a group widen the match (OR). Tags across groups narrow it (AND). The search box matches title, tips and tags.
- Thumbnails are drawn only near the viewport (IntersectionObserver), to keep 200 SVGs fast.
- Clicking a pose opens a `<dialog>` viewer with the large drawing, tags, both tips, a thirds-grid toggle, Save, and Previous/Next, which step through the current filter. Arrow keys and swipes also step.
- `#pose-N` opens a pose and `#all` closes the viewer.
- Saved poses and the grid setting live in localStorage under `pose-saved` and `pose-thirds`, wrapped in try/catch. They are per browser and not shared.
- Light and dark themes come from CSS custom properties on `:root`. The layout is responsive and has been checked at 390px and 1280px widths.

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
