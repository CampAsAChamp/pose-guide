"""Batch 3, part 3: partner poses."""
from .helpers import *

PORT = dict(top=130, s=150, hc=5.5, D=8)


def crosslegs(**kw):
    p = dict(py=0.5, bend=4, ll=("ik", "g", (-0.3, 0.2, 0.85), (1, 0.12, 0.5)), rl=("ik", "g", (0.3, 0.2, 0.7), (-1, 0.12, 0.5)),
             lf=(60, 0), rf=(60, 0),
             la=("ik", lambda J: J["kl"] + V(0, 0.34, 0), (1, -0.5, -0.3)), ra=("ik", lambda J: J["kr"] + V(0, 0.34, 0), (-1, -0.5, -0.3)))
    p.update(kw)
    return p


@card(141, "Hand in hand", "P St F Par f", "Stand side by side holding hands, each with weight on the outer leg, heads tipped slightly toward each other.",
      "Full length and square-on. Keep the joined hands on the centre line.")
def h01():
    cam = Cam(**FULL)
    a = P(LS_R, x=-1.2, who="a", tilt=5, la=("ik", "w", (-0.06, 3.75, 0.1), (0.3, 0, -1)), ra=POCKET(-1))
    b = P(LS_L, x=1.2, who="b", size=0.93, tilt=-6, ra=("ik", "w", (0.06, 3.75, 0.1), (-0.3, 0, -1)), la=RELAX)
    return sc_park(cam) + figs(cam, [a, b])


@card(142, "Side hug", "P St U Stu f", "Stand hip to hip, one arm around the shoulders and the other around the waist, heads leaning in.",
      "Crop at the waist against a plain background and keep both faces the same distance from the lens.")
def h02():
    cam = cam_tq(**PORT)
    a = dict(x=-0.72, yaw=14, who="a", sh=-4, tilt=9, la=("ik", "w", (1.5, 5.85, -0.3), (0, 0.3, -1)), ra=RELAX)
    b = dict(x=0.62, z=0.12, yaw=-14, who="c", size=0.95, sh=4, tilt=-9, ra=("ik", "w", (-1.3, 4.5, -0.35), (0, -0.3, -1)), la=POCKET(1))
    return bg_plain("#DCE2E6", "#E8ECEF") + figs(cam, [a, b], shadow=False)


@card(143, "Cheek kiss", "P St U Fie s", "One faces the camera, the other turns side-on and leans in to kiss the cheek, a hand on the far shoulder.",
      "Crop at the waist and keep the frame where the one being kissed reacts.")
def h03():
    cam = cam_tq(**PORT)
    b = dict(x=0.45, yaw=-8, who="b", size=0.93, tilt=-7, sh=3, la=RELAX, ra=RELAX)
    a = dict(x=-0.95, z=0.1, yaw=72, who="a", bend=9, nod=10, la=("ik", "w", (1.1, 5.9, -0.2), (0, 0.3, -1)), ra=("ik", "w", (0.1, 4.9, 0.6), (-1, -0.6, 0)))
    return sc_field(cam) + figs(cam, [a, b], shadow=False)


@card(144, "Lean back hold", "P St F Bea s", "Face each other, hold both hands and lean back with straight arms so each balances the other.",
      "Shoot side-on and full length with the joined hands in the centre of the frame.")
def h04():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=714)
    a = dict(x=-1.75, yaw=88, who="a", bend=-16, ll=(0, 16, 0, 16), rl=(0, 16, 0, 16),
             la=("ik", "w", (-0.08, 5.0, -0.25), (0, -1, 0)), ra=("ik", "w", (-0.08, 5.0, 0.25), (0, -1, 0)))
    b = dict(x=1.7, yaw=-88, who="b", size=0.93, bend=-16, ll=(0, 16, 0, 16), rl=(0, 16, 0, 16),
             la=("ik", "w", (0.08, 4.95, 0.25), (0, -1, 0)), ra=("ik", "w", (0.08, 4.95, -0.25), (0, -1, 0)))
    return sc_beach(cam) + figs(cam, [a, b])


@card(145, "Lift hug", "P Ac F Par s", "One wraps both arms round the other's waist and lifts them off the ground, knees bent back, arms round the neck.",
      "Shoot side-on in burst mode. Full length with a little space above the lifted head.")
def h05():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    a = dict(x=-0.5, yaw=85, who="a", bend=-8, nod=-14, ll=(0, 6, 0, 6), rl=(0, -6, 0, -6),
             la=("ik", "w", (0.85, 4.45, -0.5), (0.6, -0.6, 0)), ra=("ik", "w", (0.85, 4.4, 0.5), (-0.6, -0.6, 0)))
    b = dict(x=0.55, yaw=-85, who="b", size=0.9, py=4.95 / 0.9, bend=8, nod=12, ll=(0, -8, 0, -82), rl=(0, -14, 0, -70), lf=(0, 40), rf=(0, 40),
             la=("ik", "w", (-0.8, 6.55, 0.42), (0.5, -1, 0)), ra=("ik", "w", (-0.8, 6.55, -0.42), (-0.5, -1, 0)))
    return sc_path(cam) + figs(cam, [a, b])


@card(146, "Dip", "P Ac F Stu s", "One steps forward into a lunge and supports the other, who leans far back with one leg raised and an arm round the neck.",
      "Shoot side-on and full length. Rehearse it slowly first, then shoot a burst.")
def h06():
    cam = Cam(s=62, D=15, hc=4.2, feet_y=716)
    a = dict(x=-0.9, yaw=82, who="a", bend=28, nod=-8, rl=(0, 42, 0, -6), ll=(0, -32, 0, -32), lf=(0, 12),
             ra=("ik", "w", (1.75, 4.55, 0.35), (0, -1, 0)), la=("ik", "w", (1.45, 4.6, -0.3), (0, -1, 0)))
    b = dict(x=0.75, yaw=-88, who="b", size=0.93, bend=-50, nod=-10, ll=(0, 22, 0, 22), rl=(0, 66, 0, 12), rf=(0, 40),
             la=("ik", "w", (-0.2, 5.3, 0.4), (0, 1, 0)), ra=(70, -30, 80, -40))
    return sc_studio(cam, "#E3DDD3", "#D6CFC4") + figs(cam, [a, b])


@card(147, "Arm around stroll", "P Wa T Str f", "Walk toward the camera with arms around each other's waists, outer arms swinging, heads tilted in.",
      "Crop at mid-thigh and shoot a burst while walking backward ahead of them.")
def h07():
    cam = cam_tq(top=130, s=108)
    a = walk(1, x=-0.8, yaw=5, who="a", tilt=6, la=("ik", "w", (1.35, 4.4, -0.42), (0, -0.3, -1)))
    b = walk(-1, x=0.78, yaw=-5, who="b", size=0.93, tilt=-7, ra=("ik", "w", (-1.3, 4.6, -0.44), (0, -0.3, -1)))
    return sc_street(cam, stripes=False) + figs(cam, [a, b], shadow=False)


@card(148, "Sunset walk", "P Wa F Bea b", "Walk away along the shore, one arm over the other's shoulders and the other's arm round the waist.",
      "Shoot from behind at sunset and keep the pair on the centre line with the sun beside them.")
def h08():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=714)
    a = walk(1, x=-0.82, yaw=178, who="a", ra=("ik", "w", (1.5, 5.75, 0.52), (0, 0.2, -1)))
    b = walk(-1, x=0.78, yaw=182, who="b", size=0.93, sh=-5, tilt=8, la=("ik", "w", (-1.2, 4.5, 0.54), (0, -0.2, -1)))
    return sc_beach(cam, sunset=True) + figs(cam, [a, b])


@card(149, "Back to back sit", "P Se F Par s", "Sit on the grass back to back with knees up and arms round the shins, both faces turned to the camera.",
      "Shoot side-on from ground level and keep the two backs touching on the centre line.")
def h09():
    cam = Cam(s=96, D=11, hc=2.8, feet_y=694)
    a = floor_knees(x=-0.6, yaw=-88, who="a", bend=6, turn=44)
    b = floor_knees(x=0.6, yaw=88, who="b", size=0.95, bend=6, turn=-44)
    return sc_park(cam) + figs(cam, [a, b])


@card(150, "Wall for two", "P Se F Vie f", "Sit side by side on the wall with legs hanging. One leans in, the other puts an arm around.",
      "Full length from the front with the view behind and the wall level.")
def h10():
    cam = Cam(s=74, D=14, hc=4.4, feet_y=712)
    a = sit(x=-0.85, z=0.05, who="a", tilt=5, la=("ik", "w", (1.6, 4.05, -0.3), (0, 0.3, -1)), ra=("ik", on_thigh("r")))
    b = sit(x=0.78, z=0.05, size=0.93, who="b", sh=9, tilt=-13, la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")), ll=(4, 89, 6, -4), rl=(4, 89, -6, 8))
    return sc_view(cam) + figs(cam, [a, b], extra=lowwall(cam))


@card(151, "Pier for two", "P Se W Wat b", "Sit together at the end of the pier, legs over the edge, one head resting on the other's shoulder.",
      "Go wide from behind and centre the pier so its lines lead to the pair.")
def h11():
    cam = Cam(s=58, D=18, hc=3.4, feet_y=640)
    zend = -1.6
    a = dict(x=-0.75, z=zend + 0.45, py=0.5, yaw=180, who="a", bend=-6, ll=(8, 90, 0, 0), rl=(8, 90, 0, 0),
             ra=("ik", "w", (1.45, 2.5, zend + 1.0), (0, 0.2, -1)), la=("ik", "g", (0.8, 0.14, -0.7), (0.6, 0.3, -1)))
    b = dict(x=0.72, z=zend + 0.45, py=0.5 / 0.93, yaw=180, who="b", size=0.93, sh=-10, tilt=14, ll=(8, 90, 0, 0), rl=(8, 90, 0, 0),
             la=(8, 30, 0, 60), ra=("ik", "g", (-0.8, 0.14, -0.7), (-0.6, 0.3, -1)))
    Ja, Jb = solve(a), solve(b)
    Ja["noshins"] = Jb["noshins"] = True
    return sc_pier(cam, zend) + figs(cam, [Ja, Jb])


@card(152, "Sit and stand", "P Mx T Stu f", "One sits upright on a chair, the other stands close behind with both hands on the sitter's shoulders.",
      "A classic portrait. Camera at the sitter's eye level, crop below the seat.")
def h12():
    cam = cam_tq(top=130, s=104, hc=4.4, D=11, headtop=7.6)
    Ja = solve(sit(seat=1.9, x=-0.1, who="a", la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")), tilt=3))
    b = dict(x=0.25, z=-1.05, who="c", size=0.97, bend=6, tilt=-4,
             la=("ik", lambda J: Ja["sl"] + V(0.05, 0.32, -0.1), (1, -0.6, 0)), ra=("ik", lambda J: Ja["sr"] + V(-0.05, 0.32, -0.1), (-1, -0.6, 0)))
    return bg_plain("#E3DDD3", "#EEE9E1") + figs(cam, [Ja, b], extra=chair_front(cam, -0.1), shadow=False)


@card(153, "Step stack", "P Se F Ste f", "One sits two steps above the other with feet either side and hands on the lower one's shoulders, who leans back.",
      "Straight on with the steps level. Stack the two heads on the centre line.")
def h13():
    cam = Cam(s=76, D=13, hc=4.0, feet_y=690)
    o, zf, rise = sc_stairs(cam)
    Jb = solve(stair_sitter(zf, rise, 0, 2, "b", size=0.93, bend=-4, tilt=-4))
    a = stair_sitter(zf, rise, 0, 4, "a", bend=20,
                     ll=("ik", "w", (1.0, 3 * rise + 0.17, zf(3) - 0.42), (0.5, 1, 0.3)), rl=("ik", "w", (-1.0, 3 * rise + 0.17, zf(3) - 0.42), (-0.5, 1, 0.3)),
                     la=("ik", lambda J: Jb["sl"] + V(0.05, 0.3, -0.05), (1, -0.4, 0)), ra=("ik", lambda J: Jb["sr"] + V(-0.05, 0.3, -0.05), (-1, -0.4, 0)))
    return o + figs(cam, [a, Jb], shadow=False)


@card(154, "Elbows side by side", "P Ly F Par f", "Lie on your fronts next to each other, propped on the elbows with feet kicked up, shoulders touching.",
      "Put the camera on the ground a few steps in front, level with their eyes.")
def h14():
    cam = Cam(s=104, D=9.5, hc=1.7, feet_y=640)
    return sc_park(cam) + figs(cam, [prone(x=-1.25, yaw=10, who="a", tilt=5), prone(x=1.2, yaw=-10, who="b", size=0.95, tilt=-5)])


@card(155, "Head in lap", "P Ly F Hom f", "One sits at the end of the sofa, the other lies along it with knees up and head resting in the sitter's lap.",
      "Camera at seat height, square to the sofa, with both faces in frame.")
def h15():
    cam = Cam(s=66, D=15, hc=3.9, feet_y=716)
    a = sit(x=-2.25, z=0.05, who="a", bend=-4, nod=18, turn=14, la=("ik", "w", (-1.15, 2.9, 1.05), (0.6, -0.6, 0.3)), ra=("ik", on_thigh("r")))
    b = dict(x=1.15, z=0.95, py=2.2 / 0.93, yaw=90, who="b", size=0.93, bend=-86, nod=-6,
             ll=("ik", "w", (2.75, 1.87, 0.75), (0, 1, 0)), rl=("ik", "w", (2.6, 1.87, 1.15), (0, 1, 0)),
             la=("ik", "c", (0.15, 1.1, 0.6), (1, -0.5, 0.5)), ra=("ik", "c", (-0.15, 1.2, 0.6), (-1, -0.5, 0.5)))
    return sc_home(cam, zw=-3.2) + figs(cam, [a, b], extra=sofa_front(cam, -3.9, 3.9))


@card(156, "Cheers", "P St U Caf s", "Face each other and clink cups at chest height between you, free hands at the pockets.",
      "Shoot from the side, crop at the waist and keep the cups in the centre of the frame.")
def h16():
    cam = cam_tq(**PORT)
    Ja = solve(P(x=-1.05, yaw=70, who="a", ra=("ik", "w", (-0.2, 5.6, 0.4), (-0.5, -1, 0)), la=POCKET(1)))
    Jb = solve(P(x=1.05, yaw=-70, who="c", size=0.96, la=("ik", "w", (0.2, 5.55, 0.4), (0.5, -1, 0)), ra=POCKET(-1)))
    cups = [small_cup(cam, Ja["hdr"] + V(0.05, 0.3, 0), z=1.2), small_cup(cam, Jb["hdl"] + V(-0.05, 0.3, 0), z=1.2)]
    return bg_cafe() + figs(cam, [Ja, Jb], extra=cups, shadow=False)


@card(157, "Selfie for two", "P St U Bea f", "Heads together, one arm around, the other stretches an arm out toward the camera as if holding the phone.",
      "Hold the phone a little above eye level and keep the horizon behind the shoulders.")
def h17():
    cam = cam_tq(top=140, s=140, hc=5.5, D=8)
    a = dict(x=-0.62, yaw=12, who="a", sh=-4, tilt=10, la=("ik", "w", (1.45, 5.8, -0.3), (0, 0.3, -1)), ra=RELAX)
    b = dict(x=0.62, z=0.1, yaw=-12, who="b", size=0.95, sh=4, tilt=-10, la=("ik", "r", (0.75, 2.0, 2.1), (1, -0.6, 0)), ra=RELAX)
    return sc_beach(cam) + figs(cam, [a, b], shadow=False)


@card(158, "Whisper", "P St U Str s", "One leans in side-on to whisper with a hand on the other's shoulder; the listener faces the camera, hand to the mouth.",
      "Crop at the waist and focus on the listener's face. Shoot through the reaction.")
def h18():
    cam = cam_tq(**PORT)
    b = dict(x=0.5, yaw=-6, who="b", size=0.95, tilt=-8, la=RELAX, ra=("ik", lambda J: J["head"] + J["Rh"] @ V(-0.05, -0.5, 0.45), (-0.6, -1, 0.3)))
    a = dict(x=-0.95, z=0.05, yaw=74, who="a", bend=10, nod=4, ra=("ik", "w", (-0.25, 5.95, 0.3), (-0.5, -1, 0)), la=RELAX)
    return sc_street(cam, stripes=False) + figs(cam, [a, b], shadow=False)


@card(159, "Forehead kiss", "P St T Hom s", "The taller one cups the other's face and kisses the forehead; the shorter one rests both hands on the chest.",
      "Shoot side-on by a window and crop at mid-thigh.")
def h19():
    cam = cam_tq(top=120, s=118)
    a = dict(x=-0.85, yaw=82, who="a", bend=6, nod=26, la=("ik", "w", (0.5, 6.0, -0.45), (0.5, -1, 0)), ra=("ik", "w", (0.5, 6.0, 0.45), (-0.5, -1, 0)))
    b = dict(x=0.8, yaw=-82, who="b", size=0.9, nod=6, la=("ik", "w", (-0.38, 5.35, 0.28), (0.5, -1, 0)), ra=("ik", "w", (-0.38, 5.35, -0.28), (-0.5, -1, 0)))
    return bg_window() + figs(cam, [a, b], shadow=False)


@card(160, "Bench face to face", "P Se F Par s", "Sit sideways at opposite ends of the bench with feet up and knees bent, and join hands over the knees.",
      "Shoot from the front of the bench at seat height so the two shapes mirror each other.")
def h20():
    cam = Cam(s=70, D=15, hc=4.2, feet_y=708)

    def side(x, sg, who, size):
        return dict(x=x, z=0.05, py=(1.7 + 0.42 * size) / size, yaw=90 * sg, who=who, size=size, bend=10,
                    rl=("ik", "w", (x + sg * 1.25, 1.87, 0.3 * sg), (0, 1, 0)), ll=("ik", "w", (x + sg * 1.45, 1.87, -0.3 * sg), (0, 1, 0)),
                    rf=(0, -35), lf=(0, -35),
                    la=("ik", "w", (-0.12 * sg, 3.75, -0.2 * sg), (0, -1, 0)), ra=("ik", "w", (-0.12 * sg, 3.75, 0.2 * sg), (0, -1, 0)))

    return sc_park(cam) + figs(cam, [side(-1.95, 1, "a", 1.0), side(1.95, -1, "b", 0.93)], extra=bench(cam, -3.4, 3.4))


@card(161, "Wall talk", "P Le F Str s", "One leans back on the wall with arms folded, the other stands side-on with a straight arm planted on the wall.",
      "Square to the wall and full length. Leave a clear gap between the two faces.")
def h21():
    cam = Cam(s=66, D=15, hc=4.4, feet_y=712)
    zw = -0.72
    b = dict(x=1.05, yaw=-18, who="b", size=0.94, bend=-8, turn=-28, rl=(3, 10, 2, 10), ll=(3, 10, 2, 10), la=CROSS_L, ra=CROSS_R)
    a = P(LX, x=-1.25, z=0.2, yaw=78, who="a", la=("ik", "w", (-0.05, 6.2, zw + 0.1), (0, -0.4, -1)), ra=POCKET(-1), turn=-8)
    return sc_wall(cam, col="#B9C2B4", zw=zw, dado=None, brick="#A6B0A1") + figs(cam, [a, b], zclip=zw + 0.1)


@card(162, "Jump for two", "P Ac F Bea f", "Hold hands and jump together, joined hands thrown high and outer arms up, heels kicked back.",
      "Shoot from low in burst mode and count them in so both leave the ground together.")
def h22():
    cam = Cam(s=58, D=16, hc=4.0, feet_y=722)
    legs = dict(ll=(18, 30, 8, -72), rl=(20, 18, 10, -84), lf=(10, 50), rf=(10, 50))
    a = P(legs, x=-1.25, py=5.3, who="a", bend=-5, la=("ik", "w", (-0.05, 8.75, 0.1), (0.5, 0, -1)), ra=(138, 0, 152, -6))
    b = P(legs, x=1.25, py=5.25 / 0.93, who="b", size=0.93, bend=-5, ra=("ik", "w", (0.05, 8.7, 0.1), (-0.5, 0, -1)), la=(138, 0, 152, -6))
    return sc_beach(cam) + figs(cam, [a, b])


@card(163, "Run together", "P Ac F Fie f", "Run toward the camera hand in hand, outer arms pumping, both mid-stride.",
      "Shoot a burst from low down and keep the frame where both have a foot off the ground.")
def h23():
    cam = Cam(s=60, D=16, hc=4.2, feet_y=716)
    a = run(1, x=-1.2, who="a", la=("ik", "w", (-0.06, 4.3, 0.35), (0.3, 0, -1)))
    b = run(-1, x=1.2, who="b", size=0.93, ra=("ik", "w", (0.06, 4.3, 0.35), (-0.3, 0, -1)))
    return sc_field(cam) + figs(cam, [a, b])


@card(164, "Dance hold", "P St F Stu s", "Stand close in a ballroom hold: one hand at the partner's back, one on the shoulder, joined hands held out to the side.",
      "Shoot from the side of the joined hands, full length, with the pair centred.")
def h24():
    cam = Cam(s=64, D=15, hc=4.4, feet_y=714)
    a = P(LSTEP, x=-0.66, yaw=80, who="a", la=("ik", "w", (1.2, 5.2, -0.45), (0.3, -1, 0)), ra=("ik", "w", (0.0, 6.0, 1.3), (-0.6, -0.8, 0)))
    b = P(LTOE, x=0.66, yaw=-80, who="b", size=0.93, nod=-6, la=("ik", "w", (0.0, 5.95, 1.3), (0.6, -0.8, 0)), ra=("ik", "w", (-0.8, 6.3, -0.5), (-0.3, -1, 0)))
    return sc_studio(cam) + figs(cam, [a, b])


@card(165, "Heads together", "P St W Vie b", "Stand facing the view with arms around each other's waists, one head resting on the other's shoulder.",
      "Go wide from behind with the pair small and low in the frame.")
def h25():
    cam = Cam(**WIDE)
    a = dict(x=-0.78, yaw=180, who="a", ra=("ik", "w", (1.15, 4.6, 0.52), (0, -0.2, -1)), la=RELAX)
    b = dict(x=0.75, yaw=180, who="b", size=0.93, sh=-7, tilt=12, la=("ik", "w", (-1.1, 4.4, 0.54), (0, -0.2, -1)), ra=RELAX)
    return sc_view(cam) + figs(cam, [a, b])


@card(166, "Fist bump", "P St T Str s", "Face each other a step apart and meet fists at chest height, free hands at the pockets.",
      "Shoot from the side and crop at mid-thigh, with the fists on the centre line.")
def h26():
    cam = cam_tq(top=130, s=104)
    a = P(LSTEP, x=-1.3, yaw=72, who="a", ra=("ik", "w", (-0.16, 5.3, 0.35), (-0.4, -1, 0)), la=POCKET(1))
    b = P(LSTEP, x=1.3, yaw=-72, who="c", la=("ik", "w", (0.16, 5.3, 0.35), (0.4, -1, 0)), ra=POCKET(-1))
    return sc_street(cam, stripes=False) + figs(cam, [a, b], shadow=False)


@card(167, "Elbow rest", "P St F Stu f", "The taller one props a forearm on the shorter one's shoulder and crosses the ankles; the shorter one folds the arms.",
      "Full length and square-on. Works for friends and siblings with a height difference.")
def h27():
    cam = Cam(**FULL)
    b = dict(x=-0.8, who="b", size=0.9, la=CROSS_L, ra=CROSS_R, tilt=6, yaw=6)
    Jb = solve(b)
    a = P(LX, x=0.85, who="a", size=1.05, sh=5, tilt=-5,
          ra=("ik", lambda J: Jb["sl"] + V(-0.75, 0.3, 0.15), lambda J: Jb["sl"] + V(0.1, 0.34, 0.05) - J["sr"]), la=HIP(1))
    return sc_studio(cam) + figs(cam, [a, Jb])


@card(168, "Crouch and stand", "P Mx F Str f", "One squats in front with forearms on the knees, the other stands just behind with arms folded.",
      "Drop the camera to the squatter's eye level so the standing figure towers behind.")
def h28():
    cam = Cam(s=80, D=13, hc=2.6, feet_y=716)
    zw = -1.9
    a = dict(x=-0.5, z=0.7, py=1.3, yaw=-10, who="a", bend=30, nod=-18,
             ll=("ik", "g", (0.72, 0.17, 0.5), (0.45, 1, 0.9)), rl=("ik", "g", (-0.72, 0.17, 0.55), (-0.45, 1, 0.9)), lf=(30, 0), rf=(30, 0),
             la=("ik", "r", (0.28, 0.72, 1.72), lambda J: J["kl"] - J["sl"]), ra=("ik", "r", (-0.22, 0.66, 1.74), lambda J: J["kr"] - J["sr"]))
    b = P(LW, x=0.75, z=-0.8, who="c", yaw=-8, la=CROSS_L, ra=CROSS_R, nod=6)
    return sc_wall(cam, col="#C98F78", zw=zw, dado=None, brick="#B67C66") + figs(cam, [a, b], zclip=zw + 0.1)


@card(169, "Curb sit", "P Se F Str f", "Sit side by side on a low step, knees up, forearms on the knees, shoulders touching.",
      "Get low and square-on. Keep both pairs of feet inside the frame.")
def h29():
    cam = Cam(s=92, D=12, hc=2.6, feet_y=700)

    def low(x, who, size, **kw):
        p = dict(x=x, py=(0.75 + 0.42 * size) / size, who=who, size=size, bend=22, nod=-12,
                 ll=("ik", "g", (0.4, 0.17, 1.55), (0.2, 1, 0.3)), rl=("ik", "g", (-0.4, 0.17, 1.5), (-0.2, 1, 0.3)),
                 la=("ik", "r", (0.2, 0.85, 1.6), lambda J: J["kl"] - J["sl"]), ra=("ik", "r", (-0.2, 0.82, 1.62), lambda J: J["kr"] - J["sr"]))
        p.update(kw)
        return p

    curb = lowwall(cam, -9, 9, 0.75, -1.2, 0.45, "#D6D0C6", "#BDB7AE")
    o = sc_wall(cam, col="#B9C6D2", dado=None, zw=-1.2)
    return o + figs(cam, [low(-0.92, "a", 1.0, tilt=5), low(0.88, "c", 0.96, tilt=-5)], extra=curb, zclip=-1.1)


@card(170, "Little hand", "P Wa F Par b", "Walk away down the path holding a child's hand, the adult leaning slightly toward them.",
      "Shoot from behind at the child's height and let them walk at their own pace.")
def h30():
    cam = Cam(s=66, D=15, hc=3.2, feet_y=716)
    a = walk(1, x=-0.55, yaw=178, who="a", sh=3, ra=("ik", "w", (0.22, 3.45, -0.05), (-0.3, 0, -1)))
    b = walk(-1, x=0.95, yaw=182, who="b", size=0.58, la=("ik", "w", (0.3, 3.4, -0.05), (0.3, 0.5, -1)), turn=20, nod=-14)
    return sc_path(cam) + figs(cam, [a, b])


@card(171, "Stairs together", "P Wa F Ste b", "Climb the steps hand in hand away from the camera; one glances back over the shoulder.",
      "Stand at the bottom with the camera level and keep the pair in the upper half.")
def h31():
    cam = Cam(s=70, D=14, hc=4.4, feet_y=742)
    o, zf, rise = sc_stairs(cam)

    def climb(x, who, size, **kw):
        p = dict(x=x, z=zf(2) - 0.9, py=5.45 / size, yaw=180, who=who, size=size, bend=6,
                 ll=("ik", "w", (x - 0.4, 3 * rise + 0.17, zf(3) - 0.55), (0, 0.2, 1)),
                 rl=("ik", "w", (x + 0.42, 2 * rise + 0.17, zf(2) - 0.5), (0, 0.2, 1)), la=(5, 16, 2, 30), ra=(5, -14, 2, -4))
        p.update(kw)
        return p

    a = climb(-0.95, "a", 1.0, ra=("ik", "w", (-0.05, 5.3, -0.45), (-0.3, 0, -1)))
    b = climb(0.95, "b", 0.93, la=("ik", "w", (0.05, 5.3, -0.45), (0.3, 0, -1)), twist=26, turn=70)
    return o + figs(cam, [a, b], shadow=False)


@card(172, "Rail chat", "P Le F Wat f", "One leans back on the rail with elbows hooked over it, the other leans forward on it beside them, heads turned to each other.",
      "Square to the rail and full length. Keep the rail level behind the waist.")
def h32():
    cam = Cam(**FULL)
    zr = -0.62
    a = dict(x=-1.15, yaw=8, who="a", bend=-11, turn=34, hip=-4, rl=(-5, 9, -4, 9), ll=(-2, 14, -9, 4), lf=(12, 30),
             la=("ik", "w", (0.8, 4.2, -0.3), lambda J: V(0.0, 4.36, zr) - J["sl"]), ra=("ik", "w", (-3.0, 4.2, -0.3), lambda J: V(-2.2, 4.36, zr) - J["sr"]))
    b = dict(x=1.3, z=0.75, yaw=180, who="b", size=0.93, bend=34, turn=56, nod=-8, ll=(0, -8, 0, -8), rl=(0, 12, 0, -30), rf=(8, 40),
             la=("ik", "w", (1.0, 4.42, zr - 0.9), lambda J: V(0.75, 4.36, zr) - J["sl"]), ra=("ik", "w", (1.6, 4.42, zr - 0.9), lambda J: V(1.85, 4.36, zr) - J["sr"]))
    return sc_water_x(cam, zr) + figs(cam, [a, b], zclip=zr)


@card(173, "Picnic for two", "P Se F Par s", "Sit cross-legged facing each other on a blanket, one with hands on the knees, the other holding a cup.",
      "Shoot from the side at ground level and keep the blanket edge parallel to the frame.")
def h33():
    cam = Cam(s=92, D=11.5, hc=2.6, feet_y=690)
    rug = quad(cam, [(-3.4, 0, -1.6), (3.4, 0, -1.6), (3.8, 0, 2.2), (-3.8, 0, 2.2)], "#E3B9A9")
    a = crosslegs(x=-1.5, yaw=84, who="a", turn=-24)
    Jb = solve(crosslegs(x=1.5, yaw=-84, who="b", size=0.95, turn=24,
                         la=("ik", "c", (0.2, 1.4, 0.8), (0.5, -1, 0)), ra=("ik", "c", (-0.2, 1.4, 0.8), (-0.5, -1, 0))))
    return sc_park(cam) + rug + figs(cam, [a, Jb], extra=[mug(cam, Jb)])


@card(174, "Doorway pair", "P Le F Hom f", "Each leans a shoulder on one side of the door frame with ankles crossed, facing in toward the other.",
      "Use the doorway as the frame and keep the camera level so both uprights stay vertical.")
def h34():
    cam = Cam(s=64, D=15, hc=4.4, feet_y=712)
    base = dict(yaw=-6, hip=3, sh=-8, turn=-12, tilt=-4, ll=(-8, 0, -8, 0), rl=(-11, 10, -10, -4), rf=(10, 48), lf=(14, 0),
                la=POCKET(1), ra=POCKET(-1))
    Jb = solve(P(base, x=1.25, who="b", size=0.95))
    xj = float(Jb["sl"][0]) + 0.3
    Ja = solve(mirror(P(base, x=xj - 0.3 - 0.84 - 0.02 + 0.0, who="a")))
    xl = float(Ja["sr"][0]) - 0.3
    lint, zf_, zb = 9.3, 0.3, -7.0
    o = R(0, 0, W, H, "#566468") + R(0, 0, W, cam.gy(zb), "#6C7B7E") + R(0, cam.gy(zb), W, H, "#8F8E86")
    o += R(0, cam.gy(zf_), W, H, "#CFCAC2")
    wall = zrect(cam, zf_, -30, 0, xl, 14, "#E6DCCB") + zrect(cam, zf_, xj, 0, 30, 14, "#E6DCCB") + zrect(cam, zf_, xl, lint, xj, 14, "#E6DCCB")
    wall += zrect(cam, zf_, xl - 0.3, 0, xl, lint + 0.3, "#FFFFFF") + zrect(cam, zf_, xj, 0, xj + 0.3, lint + 0.3, "#FFFFFF")
    wall += zrect(cam, zf_, xl - 0.3, lint, xj + 0.3, lint + 0.3, "#FFFFFF")
    return o + figs(cam, [Ja, Jb], extra=[Raw(0.05, wall)], zclip=-6.5)
