# Photo pose guide generator

The Python that draws every pose in the photo pose guide and builds the single-file site (`index.html`). It needs only NumPy.

Put this folder inside the site's repository (for example as `generator/`), then:

```
pip install -r requirements.txt
python build.py            # rewrites ../index.html with all poses
python preview.py 201      # contact sheet of chosen poses in preview.html
```

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

Reusable pieces: leg sets (`LS_R`, `LS_L`, `LX`, `LW`, `LSTEP`) and arm targets (`HAIR`, `PHONE`, `SHADE`, `WAVE`, `CLASP`, `BACKH`) are in `poses/helpers.py`; `HIP`, `POCKET`, `CROSS_L`/`CROSS_R`, `walk()`, `sit()` and `stair_sitter()` are in `poses/scenes.py`; `kneel()` is in `cards_c.py`, and `run()` and `prone()` are in `cards_h.py`. `mirror(pose)` in `poses/mannequin.py` flips any pose left to right. A card module that starts with `from .helpers import *` gets everything except the last three.

## Adding a pose

Add a function with the `@card` decorator at the end of `poses/cards_i.py`, or in a new module that you import last in `poses/catalog.py`. Cards are numbered in the order they are registered, so always add new ones after the existing cards: inserting one earlier would shift every later number and break links such as `#pose-120`.

```python
@card("Window lean", "S Le T Hom s",
      "Lean a shoulder on the window frame, arms folded, eyes on the view.",
      "Shoot side-on from inside the room and expose for the window light.")
def my_window_lean():
    cam = cam_tq()
    pose = P(LX, yaw=80, la=CROSS_L, ra=CROSS_R, turn=-10)
    return bg_window() + figs(cam, [pose], shadow=False)
```

The tag string uses one short code per group, in order: People (`S P G`), Pose (`St Le Wa Se Cr Ly Ac Mx`), Shot (`W F T U C`), Setting (`Str Par Bea Fie Vie Wat Ste Caf Hom Stu`) and Angle (`f s b`). The full table is `TAGS` in `poses/helpers.py`.

Then run `python preview.py <number>` to check it and `python build.py` to rebuild the site.

## Files

- `build.py`: renders every card, inlines `styles.css` and `app.js` into `template.html`, and writes `index.html`.
- `template.html`: the site's HTML, with `__CSS__`, `__JS__`, `__COUNT__` and `__DATA__` swapped in at build time.
- `styles.css`: the site's CSS.
- `app.js`: the site's JavaScript (filters, viewer, saving).
- `preview.py`: contact sheet of chosen cards.
- `poses/mannequin.py`: the 3D skeleton, IK, perspective camera, shading and cast shadows.
- `poses/samples.py`: the first six sample scenes and small SVG helpers.
- `poses/scenes.py`: backdrops, props and common pose snippets.
- `poses/helpers.py`: the `@card` registry, tag codes and extra snippets.
- `poses/cards_b.py` to `cards_i.py`: the poses themselves.
- `poses/catalog.py`: the full ordered list, with tips for cards 1 to 64.
