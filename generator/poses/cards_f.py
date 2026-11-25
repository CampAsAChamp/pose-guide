"""Batch 3, part 1: solo standing, leaning, close-ups, action."""
from .helpers import *


@card("Both pockets", "S St F Str f", "Weight on one hip, both hands at the pockets, shoulders dropped, head tilted a touch.",
      "Full length against a plain wall. Leave space above the head and keep the camera at waist height.")
def f01():
    cam = Cam(**FULL)
    return sc_wall(cam, col="#9FBDB8", dado="#8EADA8", zw=-2.6, plant=4.6) + figs(
        cam, [P(LS_R, x=-0.3, yaw=-8, sh=3, tilt=-5, turn=6, la=POCKET(1), ra=POCKET(-1))], zclip=-2.5)


@card("Hands behind back", "S St F Par f", "Clasp both hands behind the back, one toe resting behind the other foot, head tilted.",
      "Shoot from slightly to one side so the arm line shows. Full length with soft background.")
def f02():
    cam = Cam(**FULL)
    return sc_park(cam) + figs(cam, [P(LTOE, yaw=14, sh=-3, tilt=8, turn=-10, la=BACKH(1), ra=BACKH(-1))])


@card("Clasped hands", "S St T Stu f", "Stand tall, hands loosely clasped low in front, shoulders angled slightly off-square.",
      "Crop at mid-thigh. A calm, formal look that works for team and profile photos.")
def f03():
    cam = cam_tq()
    return bg_plain("#DCE2E6", "#E8ECEF") + figs(cam, [P(yaw=-14, turn=10, tilt=2, la=CLASP(1), ra=CLASP(-1))], shadow=False)


@card("Shade the eyes", "S St W Bea s", "Stand side-on, one hand up shading the eyes, the other at the pocket, looking out to sea.",
      "Go wide, keep the figure small on a third line and facing into the open part of the frame.")
def f04():
    cam = Cam(**WIDE)
    return sc_beach(cam) + figs(cam, [P(LSTEP, x=-2.2, yaw=82, ra=SHADE(-1), la=POCKET(1), nod=-4)])


@card("Phone scroll", "S St T Str f", "Hold the phone at chest height and look down at it, other hand at the pocket, weight on one hip.",
      "Crop at mid-thigh and shoot it as a candid. Ask them to really read something.")
def f05():
    cam = cam_tq()
    J = solve(P(LS_L, yaw=10, nod=22, turn=-6, ra=PHONE(-1), la=POCKET(1)))
    return sc_street(cam, stripes=False) + figs(cam, [J], extra=[phone(cam, J)], shadow=False)


@card("Wave hello", "S Wa F Par f", "Walk toward the camera and raise one hand in a relaxed wave at shoulder height.",
      "Centre the path, shoot a burst and pick the frame where the hand is clear of the face.")
def f06():
    cam = Cam(**FULL)
    return sc_path(cam) + figs(cam, [walk(-1, yaw=-4, la=WAVE, tilt=4)])


@card("Arms wide", "S St F Fie f", "Feet apart, both arms stretched straight out to the sides, chest open and chin lifted.",
      "Step back so the fingertips have room on both sides. Shoot toward open sky.")
def f07():
    cam = Cam(s=60, D=16, hc=4.4, feet_y=712)
    return sc_field(cam) + figs(cam, [P(LW, bend=-6, nod=-14, la=OUTW, ra=OUTW)])


@card("Profile stand", "S St F Wat s", "Stand in full profile, hands at the pockets, one foot a little ahead, eyes on the horizon.",
      "Shoot exactly side-on and leave more space in front of the face than behind.")
def f08():
    cam = Cam(**FULL)
    return sc_water(cam, rx=1.6) + figs(cam, [P(LSTEP, x=-0.9, yaw=88, la=POCKET(1), ra=POCKET(-1))])


@card("Back pockets", "S St T Fie b", "Back to the camera, both hands in the back pockets, weight on one leg, head turned to profile.",
      "Crop at mid-thigh. Works best with low sun in front of the subject.")
def f09():
    cam = cam_tq()
    return sc_field(cam) + figs(cam, [P(LS_R, yaw=172, turn=34, la=BPOCKET(1), ra=BPOCKET(-1))], shadow=False)


@card("Wall prop", "S Le F Str f", "Plant one straight arm on the wall at shoulder height, lean into it and cross the ankles. Other hand on the hip.",
      "Include enough wall to show what they lean on. Keep the camera level so the wall edge stays vertical.")
def f10():
    cam = Cam(**FULL)
    o = sc_wall(cam, col="#D9CDBD", dado=None, zw=-3.0) + sidewall(cam, 1.95)
    pose = P(LX, x=-0.35, yaw=4, sh=-7, tilt=-4, la=("ik", "w", (1.78, 5.75, 0.1), (0.2, -1, 0)), ra=HIP(-1))
    return o + figs(cam, [pose], zclip=-2.9)


@card("Peekaboo", "S St T Par f", "Stand behind a tree, one hand on the trunk, and lean the head and shoulders out to one side.",
      "Crop at mid-thigh and keep the trunk on a third line. Playful, so ask for a real laugh.")
def f11():
    cam = cam_tq(top=150)
    pose = P(x=-0.85, z=-0.7, sh=11, tilt=-10, yaw=10, la=("ik", "w", (-0.05, 5.5, 0.6), (0.2, -1, 0.4)), ra=RELAX)
    return sc_park(cam) + figs(cam, [pose], extra=trunk(cam, -0.1, 1.2), shadow=False)


@card("Thumbs in belt", "S St T Fie f", "Feet apart, thumbs hooked at the belt, elbows out, chin level.",
      "Crop at mid-thigh from slightly below eye level for a confident look.")
def f12():
    cam = cam_tq()
    return sc_field(cam) + figs(cam, [P(LW, yaw=6, nod=-4, la=THUMB(1), ra=THUMB(-1))], shadow=False)


@card("Hand on head", "S St U Bea f", "One hand on top of the head as if holding a hat, the other on the hip, head tilted toward the raised arm.",
      "Crop at the waist and leave room for the raised elbow. Horizon kept behind the chest.")
def f13():
    cam = cam_waist(top=150, s=160)
    return sc_beach(cam) + figs(cam, [P(yaw=-15, tilt=6, sh=-2, la=ONHEAD(1), ra=HIP(-1))], shadow=False)


@card("Chin on fist", "S Se C Caf f", "Elbow on the table, chin resting on a loose fist, other forearm flat, eyes to the lens.",
      "Come in close and crop at the chest. Window light from the side shapes the face.")
def f14():
    cam = cam_tq(top=150, s=230, hc=4.9, D=7, headtop=5.6)
    J = solve(sit(bend=13, tilt=5, turn=-6, yaw=8,
                  ra=("ik", lambda J: J["head"] + J["Rh"] @ V(-0.1, -0.64, 0.3), lambda J: V(-0.75, 3.2, 0.9) - J["sr"]),
                  la=("ik", "c", (-0.2, 1.1, 0.95), (0.7, -0.6, 0.3))))
    J["nolegs"] = True
    ty = cam.gy(0.45, 3.15)
    return bg_cafe() + figs(cam, [J], extra=[Raw(0.42, R(0, ty, W, H - ty, "#B88A63") + R(0, ty, W, 10, "#C99C75"))], shadow=False)


@card("Hands frame face", "S St C Stu f", "Bring both hands up to the cheeks with elbows down and together, head tilted slightly.",
      "Tight crop at the chest. Keep the fingers relaxed and off the eyes.")
def f15():
    cam = cam_close(top=150)
    pose = P(tilt=5, la=("ik", lambda J: J["head"] + J["Rh"] @ V(0.42, -0.42, 0.22), (0.5, -1, 0.5)),
             ra=("ik", lambda J: J["head"] + J["Rh"] @ V(-0.42, -0.42, 0.22), (-0.5, -1, 0.5)))
    return bg_plain("#E3DDD3", "#EEE9E1") + figs(cam, [pose], shadow=False)


@card("Close profile", "S St C Hom s", "Turn fully side-on to the camera and look toward the window, chin level.",
      "Tight crop at the chest with space in front of the face. Expose for the lit edge of the profile.")
def f16():
    cam = cam_close()
    return bg_window() + figs(cam, [P(x=-0.35, yaw=80, turn=4, nod=-3)], shadow=False)


@card("Close over-shoulder", "S St C Str b", "Back to the camera, then turn the head to look over the shoulder at the lens.",
      "Tight crop at the shoulder blades. Focus on the visible eye.")
def f17():
    cam = cam_close()
    return sc_street(cam, stripes=False) + figs(cam, [P(yaw=150, twist=-16, turn=-70, tilt=-3)], shadow=False)


@card("Hand on neck", "S St U Stu f", "One hand to the back of the neck with the elbow out, other arm across the waist, eyes down.",
      "Crop at the waist. A relaxed, thoughtful look, so keep the shoulders soft.")
def f18():
    cam = cam_waist(top=120, s=170)
    pose = P(yaw=-10, nod=10, tilt=6, la=NECK(1), ra=("ik", "c", (0.38, 0.95, 0.5), (-0.8, -0.6, 0.2)))
    return bg_plain("#D9DFE3", "#E7EBEE") + figs(cam, [pose], shadow=False)


@card("Morning stretch", "S St U Hom f", "Reach both arms overhead with hands joined, lengthen the body and tip the head back a little.",
      "Leave plenty of room above for the hands. Crop at the waist beside a bright window.")
def f19():
    cam = cam_waist(top=300, s=140)
    pose = P(x=-0.5, nod=-8, bend=-4, la=("ik", "c", (0.08, 4.3, 0.0), (1, 0.3, -0.2)), ra=("ik", "c", (-0.08, 4.3, 0.0), (-1, 0.3, -0.2)))
    return bg_window() + figs(cam, [pose], shadow=False)


@card("Lapels", "S St U Stu f", "Both hands at the chest as if straightening a jacket, elbows down, chin lifted.",
      "Crop at the waist from eye level. Good in-between moment for formal portraits.")
def f20():
    cam = cam_waist(top=120, s=170)
    pose = P(yaw=8, nod=-4, la=("ik", "c", (0.3, 1.72, 0.56), (1, -0.7, 0.2)), ra=("ik", "c", (-0.3, 1.72, 0.56), (-1, -0.7, 0.2)))
    return bg_plain("#DCE2E6", "#E8ECEF") + figs(cam, [pose], shadow=False)


@card("Table lean-in", "S Se U Caf f", "Fold both forearms on the table and lean toward the camera, shoulders forward, head tilted.",
      "Shoot from across the table at eye level and crop at the table edge.")
def f21():
    cam = Cam(s=150, D=9, hc=4.75, feet_y=372 + 4.75 * 150)
    J = solve(sit(bend=17, tilt=-5, yaw=-4, la=("ik", "c", (-0.42, 1.08, 0.95), (0.8, -0.5, 0.3)),
                  ra=("ik", "c", (0.42, 1.14, 1.02), (-0.8, -0.5, 0.3))))
    J["nolegs"] = True
    ty = cam.gy(0.42, 3.15)
    return bg_cafe() + figs(cam, [J], extra=[Raw(0.40, R(0, ty, W, H - ty, "#B88A63") + R(0, ty, W, 10, "#C99C75"))], shadow=False)


@card("Phone call", "S St T Str f", "Phone to one ear, free hand at the pocket, weight on one leg, eyes off to the side.",
      "Crop at mid-thigh and shoot while they talk. Leave space on the side they look toward.")
def f22():
    cam = cam_tq()
    J = solve(P(LS_R, yaw=-10, turn=18, tilt=-4, ra=EAR(-1), la=POCKET(1)))
    return sc_street(cam, stripes=False) + figs(cam, [J], shadow=False)


@card("Look up", "S St F Str f", "Hands at the pockets, one foot forward, head tipped back to look up at the buildings.",
      "Crouch and shoot from knee height so the figure and the skyline both stretch upward.")
def f23():
    cam = Cam(**LOW)
    return sc_street(cam, stripes=False) + figs(cam, [P(LSTEP, yaw=10, nod=-24, la=POCKET(1), ra=POCKET(-1))])


@card("Pier end", "S St W Wat b", "Stand at the end of the pier with feet together and hands clasped behind the back.",
      "Go wide and centre the pier so its lines lead to the figure. Keep the horizon level.")
def f24():
    cam = Cam(s=50, D=20, hc=4.2, feet_y=646)
    return sc_pier(cam, zend=-2.0) + figs(cam, [P(z=-1.2, yaw=180, ll=(1, 0, 0, 0), rl=(1, 0, 0, 0), la=BACKH(1), ra=BACKH(-1))])


@card("Strap hold", "S St F Str f", "One hand up holding a bag strap at the shoulder, other arm loose, ankles crossed.",
      "Full length with the strap side toward the camera. Let them shift weight between frames.")
def f25():
    cam = Cam(**FULL)
    pose = P(LX, yaw=-12, turn=10, ra=("ik", "c", (-0.62, 1.85, 0.42), (-1, -0.6, 0.3)), la=RELAX)
    return sc_wall(cam, col="#E3C98A", dado="#D3B979", zw=-2.6, door=1.4) + figs(cam, [pose], zclip=-2.5)


@card("Wall perch", "S Le F Par f", "Half-sit on the edge of a wall, hands gripping the edge either side, legs straight out with ankles crossed.",
      "Full length from the front. Keep the feet in frame and the wall level.")
def f26():
    cam = Cam(**FULL)
    wall = lowwall(cam, h=3.0, zb=-1.3, zn=-0.25)
    pose = P(py=3.42, bend=6, tilt=4, ll=(2, 27, 1, 27), rl=(-7, 28, -7, 24), rf=(10, 20), lf=(12, -10),
             la=("ik", "p", (0.98, -0.36, -0.2), (1, 0.2, -0.6)), ra=("ik", "p", (-0.98, -0.36, -0.2), (-1, 0.2, -0.6)))
    return sc_park(cam) + figs(cam, [pose], extra=wall)


@card("Dance line", "S Ac F Stu f", "Balance on one leg with the other bent back, one arm reaching up and the other out to the side.",
      "Full length with space around every limb. Shoot a burst as they hit the shape.")
def f27():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    pose = P(yaw=-20, bend=-4, nod=-6, ll=(-3, 0, -2, 0), rl=(4, -20, 4, -84), rf=(10, 60), la=(160, 0, 170, 0), ra=(88, 0, 95, 0))
    return sc_studio(cam, "#E3DDD3", "#D6CFC4") + figs(cam, [pose])


@card("Tree pose", "S St F Bea f", "Stand on one leg, sole of the other foot on the inner thigh, palms together overhead.",
      "Shoot square-on at waist height with the horizon behind the hips.")
def f28():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    pose = P(ll=(-2, 0, -1, 0),
             rl=("ik", lambda J: J["hl"] * 0.45 + J["kl"] * 0.55 + V(-0.3, 0, 0.08), (-1, -0.15, 0.3)), rf=(0, 80),
             la=("ik", "c", (0.06, 4.3, 0.05), (1, 0.3, -0.2)), ra=("ik", "c", (-0.06, 4.3, 0.05), (-1, 0.3, -0.2)))
    return sc_beach(cam) + figs(cam, [pose])


@card("Warrior", "S Ac F Bea s", "Long lunge with the front knee bent and back leg straight, arms reaching forward and back in one line.",
      "Shoot side-on from hip height so the long line from hand to hand fills the width.")
def f29():
    cam = Cam(s=58, D=16, hc=3.6, feet_y=712)
    pose = P(yaw=88, rl=(0, 62, 0, -4), ll=(0, -48, 0, -48), lf=(0, 10), la=(0, -92, 0, -92), ra=(0, 92, 0, 92))
    return sc_beach(cam) + figs(cam, [pose])


@card("Split leap", "S Ac F Fie s", "Leap forward with the front leg kicked out and the back leg trailing, arms thrown up and back.",
      "Shoot side-on in burst mode from a low angle and leave space ahead of the jumper.")
def f30():
    cam = Cam(s=56, D=16, hc=3.4, feet_y=716)
    pose = P(py=5.0, yaw=84, bend=-5, nod=-8, rl=(0, 76, 0, 70), rf=(0, 30), ll=(0, -68, 0, -84), lf=(0, 60),
             la=(10, 140, 5, 150), ra=(10, -62, 5, -70))
    return sc_field(cam) + figs(cam, [pose])


@card("Skip", "S Ac F Par f", "Skip toward the camera with one knee high and the opposite arm swinging up.",
      "Centre the path, shoot a burst and keep the frame at the top of the hop.")
def f31():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    pose = P(py=4.3, rl=(4, 72, 2, -8), rf=(8, 30), ll=(2, -6, 1, -20), lf=(8, 30), la=(8, 40, -4, 112), ra=(8, -30, 2, 20), tilt=4)
    return sc_path(cam) + figs(cam, [pose])


@card("Side bend", "S St F Par f", "Feet apart, one hand on the hip, the other arm reaching up and over as the body bends to the side.",
      "Square-on and full length. Leave room on the side they bend toward.")
def f32():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    return sc_park(cam) + figs(cam, [P(LW, sh=18, tilt=-8, la=(152, 0, 166, 0), ra=HIP(-1))])


@card("Hands on knees", "S St F Str f", "Bend forward with hands on the knees, knees soft, and look up at the camera laughing.",
      "Drop the camera to their face height. Good for breaking up a stiff session.")
def f33():
    cam = Cam(s=76, D=13, hc=3.4, feet_y=716)
    pose = P(bend=48, nod=-44, ll=(8, 14, 5, -12), rl=(8, 14, 5, -12),
             la=("ik", lambda J: J["kl"] + V(0, 0.28, 0.14), (1, 0.3, 0)), ra=("ik", lambda J: J["kr"] + V(0, 0.28, 0.14), (-1, 0.3, 0)))
    return sc_wall(cam, col="#B9C6D2", dado="#A9B7C4", zw=-2.6) + figs(cam, [pose], zclip=-2.5)


@card("Tie the lace", "S Cr F Par s", "Kneel on one knee with the other foot forward, lean over and bring both hands to the shoe.",
      "Shoot side-on from low down. A natural pause in a walking sequence.")
def f34():
    cam = Cam(s=92, D=12, hc=2.6, feet_y=700)
    pose = kneel(yaw=80, bend=40, nod=28, la=("ik", lambda J: J["ar"] + J["Rr"] @ V(0.15, 0.3, 0.3), (1, -0.3, 0)),
                 ra=("ik", lambda J: J["ar"] + J["Rr"] @ V(-0.15, 0.3, 0.3), (-1, -0.3, 0)))
    return sc_path(cam) + figs(cam, [pose])


@card("Sit on heels", "S Cr F Bea s", "Kneel on both knees and sit back on the heels, hands resting on the thighs, back straight.",
      "Shoot side-on at the sitter's eye level with the horizon behind the shoulders.")
def f35():
    cam = Cam(s=110, D=10, hc=2.8, feet_y=700)
    pose = P(x=-0.5, py=0.78, yaw=76, turn=-20, ll=(3, 79, 0, -90), rl=(3, 79, 0, -90), lf=(180, 5), rf=(180, 5),
             la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")))
    return sc_beach(cam) + figs(cam, [pose])


@card("High kneel", "S Cr F Bea f", "Kneel upright on both knees, both hands lifted into the hair with elbows out, back slightly arched.",
      "Camera at the kneeler's chest height. Leave room for the elbows.")
def f36():
    cam = Cam(s=100, D=11, hc=3.2, feet_y=704)
    pose = P(py=2.33, yaw=-10, bend=-6, tilt=4, ll=(5, 0, 0, -88), rl=(5, 0, 0, -88), lf=(180, 8), rf=(180, 8), la=HAIR(1), ra=HAIR(-1))
    return sc_beach(cam) + figs(cam, [pose])


@card("Doorway silhouette", "S St F Hom b", "Stand in the open doorway facing out, both hands up on the frame, feet apart.",
      "Shoot from inside the darker room toward the light so the figure reads as a shape.")
def f37():
    cam = Cam(**FULL)
    zf_ = 0.35
    o = R(0, 0, W, H, "#D4E6EC")
    for x, y, r, c in ((120, cam.hy - 70, 120, "#8DB58D"), (330, cam.hy - 90, 140, "#7DAA80"), (520, cam.hy - 60, 110, "#8DB58D")):
        o += C(x, y, r, c)
    o += R(0, cam.hy + 10, W, H, "#A9CC9C") + R(0, cam.gy(-0.2), W, H, "#8F8E86")
    wall = zrect(cam, zf_, -30, 0, -2.3, 14, "#5A6468") + zrect(cam, zf_, 2.3, 0, 30, 14, "#5A6468") + zrect(cam, zf_, -2.3, 9.4, 2.3, 14, "#5A6468")
    wall += zrect(cam, zf_, -2.55, 0, -2.3, 9.65, "#6E7A7E") + zrect(cam, zf_, 2.3, 0, 2.55, 9.65, "#6E7A7E") + zrect(cam, zf_, -2.55, 9.4, 2.55, 9.65, "#6E7A7E")
    pose = P(LW, yaw=180, la=("ik", "w", (-2.2, 6.9, 0.1), (0.3, -1, -0.3)), ra=("ik", "w", (2.2, 6.9, 0.1), (-0.3, -1, -0.3)))
    return o + figs(cam, [pose], extra=[Raw(0.3, wall)], shadow=False)


@card("Summit", "S St W Vie f", "Stand on the high point facing the camera with both arms raised wide.",
      "Go wide, keep the figure small and central with mountains on both sides.")
def f38():
    cam = Cam(**WIDE)
    rock = box(cam, -1.6, 1.6, 0, 1.0, -1.0, 1.0, "#B7B2A8", "#9E998F")
    return sc_view(cam) + figs(cam, [P(LW, gy=1.0, la=(128, -4, 142, -8), ra=(128, -4, 142, -8), nod=-6)], extra=rock, gy=1.0)


@card("Fence lean", "S Le T Fie f", "Lean on a fence with forearms folded along the top rail and chin close to the arms.",
      "Shoot from the other side of the fence at their eye level and crop below the rail.")
def f39():
    cam = cam_tq(top=190, s=118)
    zr = 0.55
    fence = zrect(cam, zr, -30, 4.75, 30, 5.0, "#A9825F") + zrect(cam, zr, -30, 2.9, 30, 3.12, "#A9825F")
    for x in (-3.3, 0.9, 5.1):
        fence += zrect(cam, zr, x, 0, x + 0.3, 5.25, "#8C6A4C")
    pose = P(bend=24, nod=-16, tilt=5, la=("ik", "w", (-0.45, 5.14, 0.6), lambda J: V(0.95, 5.1, zr) - J["sl"]),
             ra=("ik", "w", (0.5, 5.2, 0.68), lambda J: V(-0.95, 5.1, zr) - J["sr"]))
    return sc_field(cam) + figs(cam, [pose], extra=[Raw(zr - 0.1, fence)], shadow=False)


@card("Counter lean", "S Le T Caf s", "Stand side-on at the counter, one elbow on it holding a cup, other hand at the pocket, ankles crossed.",
      "Shoot along the counter and crop at mid-thigh, with space in front of the face.")
def f40():
    cam = cam_tq(top=130, s=118)
    counter = box(cam, 0.75, 6, 0, 4.4, -1.2, 1.0, "#C99C75", "#A57750", "#96683F")
    J = solve(P(LX, x=-0.4, yaw=84, bend=10, turn=-24, ra=("ik", "w", (1.25, 4.72, 0.45), lambda J: V(0.85, 4.5, 0.75) - J["sr"]), la=POCKET(1)))
    return cafe_side(cam) + figs(cam, [J], extra=counter + [small_cup(cam, J["hdr"] + V(0.05, -0.05, 0), z=float(J["hdr"][2]) + 0.3)], shadow=False)


@card("Mirror selfie", "S St T Hom f", "Hold the phone at chest height facing the mirror, other hand at the pocket, weight on one hip.",
      "Stand square to the mirror, keep the phone below the chin and check the background behind you.")
def f41():
    cam = cam_tq()
    J = solve(P(LS_L, yaw=8, tilt=-4, ra=("ik", "c", (-0.2, 1.75, 0.8), (-0.7, -1, 0)), la=POCKET(1)))
    return bg_window() + figs(cam, [J], extra=[phone(cam, J)], shadow=False)


@card("Side squat", "S Cr F Str s", "Squat side-on with heels down, elbows on the knees and chin resting on both hands.",
      "Bring the camera down to their eye level and shoot against a plain wall.")
def f42():
    cam = Cam(s=100, D=11, hc=2.4, feet_y=700)
    pose = P(py=1.3, yaw=78, bend=30, nod=-20, turn=-30,
             ll=("ik", "g", (0.3, 0.17, 0.5), (0.2, 1, 0.9)), rl=("ik", "g", (-0.3, 0.17, 0.55), (-0.2, 1, 0.9)),
             la=("ik", lambda J: J["head"] + J["Rh"] @ V(0.15, -0.66, 0.3), lambda J: J["kl"] - J["sl"]),
             ra=("ik", lambda J: J["head"] + J["Rh"] @ V(-0.15, -0.66, 0.3), lambda J: J["kr"] - J["sr"]))
    return sc_wall(cam, col="#D8B49C", dado=None, zw=-1.6) + figs(cam, [pose], zclip=-1.5)


@card("Walk the line", "S Ac F Str s", "Walk along a low wall heel to toe with both arms out for balance, eyes down.",
      "Shoot side-on from below the wall height and leave space in the direction of travel.")
def f43():
    cam = Cam(s=62, D=15, hc=3.6, feet_y=720)
    wall = lowwall(cam, -9, 9, 1.4, -0.45, 0.45)
    pose = P(gy=1.4, yaw=86, nod=16, rl=(0, 18, 0, 4), ll=(0, -14, 0, -22), lf=(2, 25), rf=(2, 0), la=(84, 0, 88, 0), ra=(84, 0, 80, 0))
    return sc_street(cam, stripes=False) + figs(cam, [pose], extra=wall, shadow=False)
