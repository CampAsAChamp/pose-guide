# Photo pose guide generator

The Python that draws every pose in the photo pose guide and builds the single-file site (`../index.html`). It needs NumPy, plus an installed Chrome for the smoke test and screenshots.

```
pip install -r requirements.txt
python build.py            # checks the pose data, then rewrites ../index.html
python smoke_test.py       # headless-Chrome check of the built page
python preview.py 12 45    # contact sheet of chosen poses in preview.html (add --png for preview.png)
```

GitHub Actions (`.github/workflows/check.yml`) rebuilds the page on every push, fails if it differs from the committed `index.html`, and runs the smoke test. Always commit `index.html` together with the generator change that produced it.

## How a pose is made

Every pose is a small Python function that returns SVG for a 600 x 800 portrait frame. It does three things:

1. **Sets a camera.** `Cam(s, D, hc, feet_y)` is a level perspective camera: `s` is pixels per head-height at the subject, `D` the camera distance, `hc` the camera height (in head-heights) and `feet_y` where the ground at the subject lands on screen. `Cam(**FULL)` is the standard full-length framing; `cam_tq()`, `cam_waist()` and `cam_close()` crop at the thigh, waist and chest.
2. **Draws a backdrop.** Scene functions in `poses/scenes.py` return flat SVG: `sc_wall`, `sc_street`, `sc_beach`, `sc_park`, `sc_field`, `sc_view`, `sc_path`, `sc_home`, `sc_studio`, `sc_water`, `sc_water_x`, `sc_pier`, `sc_stairs`, `bg_cafe`, `bg_window`, `bg_plain`. Props such as `bench`, `box`, `lowwall`, `chair_front` and `sofa_front` sit among the figures by depth.
3. **Poses one or more mannequins** and renders them with `figs(cam, [pose, ...], extra=props)`.

### Units and directions

World units are head-heights. X points to screen right, Y up and Z toward the camera. A figure with `yaw=0` faces the camera, and its left side is screen right. `yaw=90` faces screen right, `yaw=180` faces away.

### A pose dictionary

```python
dict(
    x=0, z=0,                # position on the ground
    yaw=15,                  # whole-body turn
    hip=-5, sh=3,            # hip and shoulder tilt (contrapposto)
    bend=10, twist=0,        # torso lean forward/back and twist
    turn=-20, tilt=4, nod=0, # head turn, tilt and nod
    la=..., ra=...,          # left and right arm
    ll=..., rl=...,          # left and right leg
    lf=(toe_out, pitch), rf=...,
    who="b", size=0.93,      # tint (a b c d e) and scale
    py=None,                 # pelvis height for seated or airborne poses; None plants the lowest foot on the ground
)
```

A limb is either four angles, `(upper_out, upper_forward, lower_out, lower_forward)` in degrees, or a reach target solved with IK: `("ik", frame, (x, y, z), pole)`. The frame is `"w"` world, `"p"` pelvis, `"c"` chest, `"r"` body root or `"g"` ground under the pelvis, or a function `lambda J: point` for targets on another joint or person. The pole picks which way the elbow or knee bends.

Reusable pieces: leg sets (`LS_R`, `LS_L`, `LX`, `LW`, `LSTEP`), arm targets (`HAIR`, `PHONE`, `SHADE`, `WAVE`, `CLASP`, `BACKH`) and whole-pose snippets (`kneel()`, `run()`, `prone()`, `floor_knees()`, `sofa_front()`) are in `poses/helpers.py`; `HIP`, `POCKET`, `CROSS_L`/`CROSS_R`, `walk()`, `sit()` and `stair_sitter()` are in `poses/scenes.py`. `mirror(pose)` in `poses/mannequin.py` flips any pose left to right. Every card module starts with `from .helpers import *`, which brings in all of these; card modules never import from each other. Put anything a second module needs into `helpers.py`.

## Adding a pose

Add a function with the `@card` decorator at the end of `poses/cards_i.py`, or in a new module added to the import line in `poses/catalog.py`. The first argument is the pose number. Give a new pose the next unused number (201, 202, ...). A number is a public link (`#pose-120`), so never reuse or change one.

```python
@card(201, "Window lean", "S Le T Hom s",
      "Lean a shoulder on the window frame, arms folded, eyes on the view.",
      "Shoot side-on from inside the room and expose for the window light.",
      alt="Mannequin leaning a shoulder on a window frame with arms folded.")  # optional screen-reader description
def my_window_lean():
    cam = cam_tq()
    pose = P(LX, yaw=80, la=CROSS_L, ra=CROSS_R, turn=-10)
    return bg_window() + figs(cam, [pose], shadow=False)
```

The tag string uses one short code per group, in order: People (`S P G`), Pose (`St Le Wa Se Cr Ly Ac Mx`), Shot (`W F T U C`), Setting (`Str Par Bea Fie Vie Wat Ste Caf Hom Stu`) and Angle (`f s b`). The full table is `TAGS` in `poses/registry.py`.

Then run `python preview.py <number>` to check it, and `python build.py --lock` once to record the new number and title in `pose_numbers.json`. After that, plain `python build.py` refuses to build if a recorded number disappears or its title changes. For a deliberate rename, edit the title and run `--lock` again.

### What the build checks

`build.py` runs `checks.py` before writing anything and lists every problem it finds: numbers must run 1 to N without gaps, recorded numbers keep their titles, titles are unique, each card has one tag per group in order, tips are one or two sentences, visible text uses typographic quotes rather than `"`, and every drawing parses as SVG. Straight apostrophes are fine; the build turns them into `’`.

## Files

- `build.py`: renders every card, runs the checks, inlines `styles.css` and `app.js` into `template.html`, and writes `index.html`.
- `checks.py`: the data checks listed above.
- `pose_numbers.json`: every published pose number and its title. Written only by `build.py --lock`.
- `chrome.py`: finds and starts headless Chrome for the smoke test and screenshots. Set `CHROME` to pick the binary and `CHROME_FLAGS` to add switches.
- `template.html`: the site's HTML, with `__CSS__`, `__JS__`, `__COUNT__` and `__DATA__` swapped in at build time.
- `styles.css`: the site's CSS.
- `app.js`: the site's JavaScript (filters, viewer, saving).
- `smoke_test.py`: loads the built page twice in headless Chrome and checks it works, including that saved poses and the grid setting survive a reload. Standard library only, plus an installed Chrome.
- `preview.py`: contact sheet of chosen cards; `--png` screenshots it with Chrome.
- `poses/mannequin.py`: the 3D skeleton, IK, perspective camera, shading and cast shadows.
- `poses/registry.py`: the `@card` decorator, the `Card` record, tag codes and filter groups. It imports nothing else from the package, so any module can use it.
- `poses/samples.py`: small SVG helpers and the first six poses.
- `poses/scenes.py`: backdrops, props and common pose snippets.
- `poses/helpers.py`: everything a card module imports: scenes, props and shared pose snippets, plus `@card`.
- `poses/cards_b.py` to `cards_i.py`: the poses themselves.
- `poses/catalog.py`: imports every card module and sorts the cards by number.
