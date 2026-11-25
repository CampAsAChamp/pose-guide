"""Batch 3, part 4: group poses."""
import math
from .helpers import *

WHO = "acbde"


@card(175, "Linked trio walk", "G Wa F Str f", "Three walk toward the camera in step, the middle one with arms over both shoulders, outer arms swinging.",
      "Shoot a burst from in front and leave a margin either side of the outer walkers.")
def i01():
    cam = Cam(s=62, D=16, hc=4.4, feet_y=708)
    l = walk(1, x=-1.75, z=-0.2, yaw=4, who="c", size=0.97, tilt=5, la=("ik", "w", (0.3, 4.6, -0.5), (0, -0.3, -1)))
    m = walk(-1, x=0, z=0.15, who="a", size=1.03, la=("ik", "w", (2.3, 5.9, -0.5), (0, 0.3, -1)), ra=("ik", "w", (-2.3, 5.9, -0.5), (0, 0.3, -1)))
    r = walk(1, x=1.75, z=-0.2, yaw=-4, who="b", size=0.94, tilt=-5, ra=("ik", "w", (-0.3, 4.4, -0.5), (0, -0.3, -1)))
    return sc_street(cam) + figs(cam, [l, m, r])


@card(176, "Beach family line", "G Wa W Bea s", "Walk along the shore in a line holding hands, adults at the ends and children between.",
      "Go wide and side-on, keep the whole chain in the lower half with open beach ahead.")
def i02():
    cam = Cam(s=48, D=21, hc=3.6, feet_y=656)
    xs, sizes, who = (-3.0, -1.0, 0.9, 2.9), (0.97, 0.58, 0.7, 1.0), ("b", "c", "d", "a")
    hy_ = (3.0, 2.55, 3.1)
    ps = []
    for i in range(4):
        p = walk(1 if i % 2 else -1, x=xs[i], yaw=84, who=who[i], size=sizes[i])
        if i < 3:   # leading (far-side) hand reaches forward
            p["la"] = ("ik", "w", ((xs[i] + xs[i + 1]) / 2, hy_[i], -0.2), (0, -1, 0))
        if i > 0:   # near-side hand reaches back
            p["ra"] = ("ik", "w", ((xs[i] + xs[i - 1]) / 2, hy_[i - 1], -0.15), (0, -1, 0))
        ps.append(p)
    return sc_beach(cam) + figs(cam, ps)


@card(177, "Family portrait", "G St F Par f", "Adults stand close behind with an arm around each other, children in front with a parent's hand on each shoulder.",
      "Full length and square-on. Camera at the children's head height keeps everyone in proportion.")
def i03():
    cam = Cam(s=66, D=15, hc=3.6, feet_y=716)
    k1 = dict(x=-0.8, z=0.45, who="c", size=0.6, la=RELAX, ra=RELAX, tilt=4)
    k2 = dict(x=0.75, z=0.45, who="d", size=0.72, la=RELAX, ra=RELAX, tilt=-4)
    J1, J2 = solve(k1), solve(k2)
    a = dict(x=-0.95, z=-0.6, who="a", tilt=5, la=("ik", "w", (0.9, 4.5, -1.1), (0, -0.3, -1)),
             ra=("ik", lambda J: J1["sr"] + V(0, 0.22, -0.05), (-1, -0.4, 0.3)))
    b = dict(x=0.95, z=-0.6, who="b", size=0.94, tilt=-5, ra=("ik", "w", (-0.9, 4.3, -1.1), (0, -0.3, -1)),
             la=("ik", lambda J: J2["sl"] + V(0, 0.22, -0.05), (1, -0.4, 0.3)))
    return sc_park(cam) + figs(cam, [a, b, J1, J2])


@card(178, "Swing walk", "G Wa F Par b", "Two adults walk away with a child between them, lifting the child off the ground by both hands.",
      "Shoot from behind in burst mode and keep the frame at the top of the swing.")
def i04():
    cam = Cam(s=66, D=15, hc=3.4, feet_y=716)
    a = walk(1, x=-1.3, yaw=178, who="a", ra=("ik", "w", (-0.72, 3.95, 0), (-0.3, 0.3, -1)))
    b = walk(-1, x=1.3, yaw=182, who="b", size=0.95, la=("ik", "w", (0.72, 3.9, 0), (0.3, 0.3, -1)))
    c = dict(x=0, py=2.75 / 0.55, yaw=180, who="c", size=0.55, bend=-8, ll=(6, 52, 2, 28), rl=(6, 44, 2, 22), lf=(0, -20), rf=(0, -20),
             la=("ik", "w", (-0.62, 3.9, 0), (0.3, 1, 0)), ra=("ik", "w", (0.62, 3.85, 0), (-0.3, 1, 0)))
    return sc_path(cam) + figs(cam, [a, b, c])


@card(179, "Peek stack", "G Mx F Str f", "Hide behind a corner and lean out one above the other: one squatting, one crouched, one standing, each with a hand on the wall.",
      "Keep the wall edge near the centre line with the three heads stacked beside it.")
def i05():
    cam = Cam(s=64, D=15, hc=4.0, feet_y=716)
    wall = box(cam, 0.45, 9, 0, 16, -0.4, 0.4, "#D9CDBD", "#D9CDBD", "#C6B9A8")
    hand = lambda y: ("ik", "w", (0.5, y, 0.5), (0.2, -1, 0.3))
    top = P(x=1.2, z=-1.5, who="d", size=1.03, sh=18, tilt=-8, la=hand(6.6), ra=RELAX)
    mid = P(x=0.95, z=-1.0, who="a", bend=10, sh=14, tilt=-6, ll=(20, 30, 10, -40), rl=(20, 30, 10, -40), la=hand(4.6), ra=RELAX)
    low = dict(x=0.6, z=-0.55, py=1.3, who="b", size=0.95, sh=10, tilt=-6, bend=8,
               ll=("ik", "g", (0.6, 0.17, 0.3), (0.45, 1, 0.6)), rl=("ik", "g", (-0.6, 0.17, 0.3), (-0.45, 1, 0.6)), la=hand(2.6), ra=RELAX)
    return sc_street(cam, stripes=False) + figs(cam, [top, mid, low], extra=wall)


@card(180, "Stack", "G St F Stu f", "Line up one behind the other and lean out alternately left and right so every face shows. Front one bends with hands on knees.",
      "Shoot square-on from chest height and check each head is clear of the one in front.")
def i06():
    cam = Cam(s=64, D=15, hc=4.2, feet_y=716)
    ps = [
        dict(x=0, z=1.0, who="b", size=0.94, bend=44, nod=-40, ll=(8, 14, 5, -12), rl=(8, 14, 5, -12),
             la=("ik", lambda J: J["kl"] + V(0, 0.28, 0.14), (1, 0.3, 0)), ra=("ik", lambda J: J["kr"] + V(0, 0.28, 0.14), (-1, 0.3, 0))),
        P(LW, x=-0.35, z=0.3, who="a", sh=15, tilt=-8, bend=14, la=HIP(1), ra=HIP(-1)),
        P(LW, x=0.4, z=-0.4, who="c", sh=-18, tilt=9, bend=6, la=HIP(1), ra=HIP(-1)),
        P(LW, x=0, z=-1.1, who="d", size=1.05, la=(138, 0, 152, -6), ra=(138, 0, 152, -6)),
    ]
    return sc_studio(cam, "#E3DDD3", "#D6CFC4") + figs(cam, ps)


@card(181, "Bench five", "G Mx F Par f", "Three sit on the bench, two stand behind it leaning forward with hands on the backrest between the heads.",
      "Square to the bench, camera at seated head height, margin outside both ends.")
def i07():
    cam = Cam(s=62, D=16, hc=4.2, feet_y=712)
    seated = [sit(x=-1.95, z=0.05, who="a", yaw=10, tilt=4, la=("ik", on_thigh("l")), ra=("ik", on_thigh("r"))),
              sit(x=0, z=0.05, who="b", size=0.95, la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")), rl=(5, 89, -6, 6), ll=(5, 89, 6, -4)),
              sit(x=1.95, z=0.05, who="c", yaw=-10, tilt=-4, la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")))]
    back = [dict(x=sx * 0.98, z=-1.75, who=w, size=sz, bend=22, nod=-12,
                 la=("ik", "w", (sx * 0.98 + 0.45, 3.86, -0.86), (1, -0.4, -0.3)), ra=("ik", "w", (sx * 0.98 - 0.45, 3.86, -0.86), (-1, -0.4, -0.3)))
            for sx, w, sz in ((-1, "d", 1.03), (1, "e", 0.98))]
    return sc_park(cam) + figs(cam, seated + back, extra=bench(cam, -3.3, 3.3))


@card(182, "Sofa trio", "G Se F Hom f", "Three sit close on the sofa. The middle one puts an arm round each neighbour, who lean in.",
      "Square to the sofa at seated eye level with some floor in front of the feet.")
def i08():
    cam = Cam(s=70, D=15, hc=3.9, feet_y=720)
    l = sit(x=-1.7, z=0.1, who="a", yaw=8, sh=-6, tilt=8, la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")))
    m = sit(x=0, z=0.1, who="c", size=1.02, bend=-6, la=("ik", "w", (2.4, 4.05, -0.3), (0, 0.3, -1)), ra=("ik", "w", (-2.4, 4.05, -0.3), (0, 0.3, -1)),
            ll=(8, 89, 4, 6), rl=(8, 89, 4, 0))
    r = sit(x=1.65, z=0.1, who="b", size=0.94, yaw=-8, sh=6, tilt=-8, la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")),
            rl=("ik", lambda J: J["kl"] + V(-0.05, 0.46, 0.1), (-1, 0.2, 0.5)), rf=(-78, 8), ll=(6, 88, 2, 6))
    return sc_home(cam, zw=-3.2) + figs(cam, [l, m, r], extra=sofa_front(cam, -3.9, 3.9))


@card(183, "Toast", "G St T Caf s", "Four stand in a loose ring and bring their cups together in the middle at chest height.",
      "Shoot through a gap in the ring, crop at mid-thigh and focus on the cups.")
def i09():
    cam = cam_tq(top=130, s=100)
    spots = ((-1.5, 0.55, "a", 1.0), (1.5, 0.55, "c", 0.97), (-0.85, -1.15, "b", 0.94), (0.9, -1.15, "d", 1.03))
    ps, cups = [], []
    for x, z, w, sz in spots:
        yaw = math.degrees(math.atan2(-x, -0.3 - z))
        sd = "r" if x < 0 else "l"
        tgt = (0.24 * (1 if x > 0 else -1), 5.75, -0.3 + (0.2 if z > 0 else -0.2))
        p = dict(x=x, z=z, yaw=yaw, who=w, size=sz)
        p[sd + "a"] = ("ik", "w", tgt, (0.4 if sd == "l" else -0.4, -1, 0))
        p[("l" if sd == "r" else "r") + "a"] = POCKET(1 if sd == "r" else -1)
        J = solve(p)
        ps.append(J)
        cups.append(small_cup(cam, J["hd" + sd] + V(0, 0.34, 0), z=float(J["hd" + sd][2]) + 0.35))
    return bg_cafe() + figs(cam, ps, extra=cups, shadow=False)


@card(184, "Power V", "G St F Stu f", "Stand in a V with one at the point and two each side stepping back, arms folded or hands on hips, feet apart.",
      "Shoot from waist height, square to the point person, with the back pair inside the frame edges.")
def i10():
    cam = Cam(s=56, D=17, hc=3.6, feet_y=716)
    ps = [P(LW, x=0, z=0.9, who="a", la=CROSS_L, ra=CROSS_R),
          P(LW, x=-1.7, z=0, who="c", yaw=10, la=HIP(1), ra=HIP(-1)), P(LW, x=1.7, z=0, who="b", size=0.96, yaw=-10, la=HIP(1), ra=HIP(-1)),
          P(LW, x=-3.4, z=-0.9, who="d", size=1.03, yaw=16, la=CROSS_L, ra=CROSS_R), P(LW, x=3.4, z=-0.9, who="e", yaw=-16, la=CROSS_L, ra=CROSS_R)]
    return sc_studio(cam) + figs(cam, ps)


@card(185, "Step levels", "G Mx F Ste f", "Use the steps for height: one sits low in front, two sit a couple of steps up either side, two stand at the back.",
      "Straight on with the steps level, stepping back until the top pair's heads have space above.")
def i11():
    cam = Cam(s=60, D=16, hc=4.4, feet_y=728)
    o, zf, rise = sc_stairs(cam)
    ps = [P(LW, x=-1.0, z=zf(6) - 0.65, gy=6 * rise, who="d", size=1.02, la=HIP(1), ra=("ik", "w", (0.3, 8.3 + 0.9, zf(6) - 1.1), (0, -0.3, -1))),
          P(LW, x=1.0, z=zf(6) - 0.65, gy=6 * rise, who="e", la=CROSS_L, ra=CROSS_R),
          stair_sitter(zf, rise, -2.1, 4, "c", yaw=10, tilt=4), stair_sitter(zf, rise, 2.1, 4, "b", size=0.95, yaw=-10, tilt=-4),
          stair_sitter(zf, rise, 0, 2, "a", bend=20)]
    return o + figs(cam, ps, shadow=False)


@card(186, "Wall row", "G Se F Par f", "Four sit along a low wall with legs hanging, arms round each other, end people angled in.",
      "Square to the wall and full length with a margin beyond each end.")
def i12():
    cam = Cam(s=58, D=17, hc=4.4, feet_y=708)
    xs = (-2.9, -0.97, 0.97, 2.9)
    ps = [sit(x=xs[0], z=0.05, who="c", yaw=14, tilt=5, la=("ik", "w", (xs[1] + 0.3, 4.0, -0.35), (0, 0.3, -1)), ra=("ik", "p", (-1.0, -0.28, -0.05), (-0.6, 0.3, -1))),
          sit(x=xs[1], z=0.05, who="a", size=1.02, la=("ik", on_thigh("l")), ra=("ik", on_thigh("r")), ll=(4, 89, 6, -4), rl=(4, 89, -6, 8)),
          sit(x=xs[2], z=0.05, who="b", size=0.95, la=("ik", "w", (xs[3] + 0.3, 4.0, -0.35), (0, 0.3, -1)), ra=("ik", "w", (xs[1] - 0.3, 4.0, -0.35), (0, 0.3, -1))),
          sit(x=xs[3], z=0.05, who="d", yaw=-14, tilt=-5, la=("ik", "p", (1.0, -0.28, -0.05), (0.6, 0.3, -1)), ra=("ik", on_thigh("r")))]
    return sc_park(cam) + figs(cam, ps, extra=lowwall(cam, -5.6, 5.6))


@card(187, "Wall row with a view", "G Se W Vie b", "Four sit along the wall facing the view, arms across each other's backs, one pointing at something in the distance.",
      "Go wide from behind with the row low in the frame and the landscape above.")
def i13():
    cam = Cam(s=52, D=19, hc=4.2, feet_y=668)
    xs = (-2.9, -0.97, 0.97, 2.9)
    Pb = (0, 0.2, -1)
    ps = [sit(x=xs[0], yaw=180, who="c", size=0.97, ra=("ik", "w", (xs[1] + 0.4, 3.9, 0.55), Pb), la=(70, 60, 75, 70)),
          sit(x=xs[1], yaw=180, who="a", size=1.02, la=(8, 30, 0, 60), ra=("ik", "w", (xs[2] + 0.4, 3.95, 0.55), Pb)),
          sit(x=xs[2], yaw=180, who="b", size=0.94, sh=-6, tilt=8, la=(8, 30, 0, 60), ra=(8, 30, 0, 60)),
          sit(x=xs[3], yaw=180, who="d", la=("ik", "w", (xs[2] - 0.3, 3.8, 0.55), Pb), ra=(8, 30, 0, 60))]
    return sc_view(cam) + figs(cam, ps, extra=lowwall(cam, -5.6, 5.6))


@card(188, "Crouch trio", "G Mx T Str f", "One squats low in front, two stand close behind and lean in with hands on their knees.",
      "Camera at the squatter's eye level so the three faces stack in a tight triangle.")
def i14():
    cam = Cam(s=84, D=12.5, hc=2.8, feet_y=722)
    zw = -2.2
    a = dict(x=0, z=0.8, py=1.3, who="a", bend=30, nod=-18,
             ll=("ik", "g", (0.72, 0.17, 0.5), (0.45, 1, 0.9)), rl=("ik", "g", (-0.72, 0.17, 0.55), (-0.45, 1, 0.9)), lf=(30, 0), rf=(30, 0),
             la=("ik", "r", (0.28, 0.72, 1.72), lambda J: J["kl"] - J["sl"]), ra=("ik", "r", (-0.22, 0.66, 1.74), lambda J: J["kr"] - J["sr"]))

    def lean(x, who, size, yaw):
        return dict(x=x, z=-0.75, who=who, size=size, yaw=yaw, bend=40, nod=-36, ll=(8, 14, 5, -12), rl=(8, 14, 5, -12),
                    la=("ik", lambda J: J["kl"] + V(0, 0.28, 0.14), (1, 0.3, 0)), ra=("ik", lambda J: J["kr"] + V(0, 0.28, 0.14), (-1, 0.3, 0)))

    return sc_wall(cam, col="#B9C2B4", zw=zw, dado=None, brick="#A6B0A1") + figs(
        cam, [a, lean(-1.35, "c", 1.0, 14), lean(1.35, "b", 0.95, -14)], zclip=zw + 0.1)


@card(189, "Field run", "G Ac F Fie f", "Four run toward the camera in a loose line, each at a different point in the stride.",
      "Shoot a burst from low down and let them run past either side of you.")
def i15():
    cam = Cam(s=54, D=17, hc=4.0, feet_y=716)
    ps = [run(1, x=-3.2, z=-0.6, who="c", size=0.97), run(-1, x=-1.05, z=0.4, who="a", py=4.5),
          run(1, x=1.05, z=0.1, who="b", size=0.94, py=4.45), run(-1, x=3.2, z=-0.8, who="d", size=1.02)]
    return sc_field(cam) + figs(cam, ps)


@card(190, "Crossing line", "G Wa F Str b", "Four walk away across the crossing in single file with even gaps, each mid-stride.",
      "Shoot from behind and slightly to one side so the four figures don't overlap.")
def i16():
    cam = Cam(s=56, D=17, hc=4.4, feet_y=708)
    ps = [walk(1 if i % 2 else -1, x=x, z=z, yaw=176, who=WHO[i], size=sz, **kw)
          for i, (x, z, sz, kw) in enumerate(((-3.0, 1.0, 1.0, dict(la=POCKET(1), ra=POCKET(-1))), (-1.0, 0.3, 0.95, {}),
                                              (1.0, -0.4, 1.03, dict(la=POCKET(1))), (3.0, -1.1, 0.97, {})))]
    return sc_street(cam) + figs(cam, ps)


@card(191, "Group selfie", "G St U Bea f", "Two in front, three behind leaning in between the gaps, the tallest at the edge stretching an arm out with the phone.",
      "Hold the phone high and tilt it down. Check both ends of the group are inside the frame.")
def i17():
    cam = cam_tq(top=170, s=92, hc=5.4, D=10)
    ps = [dict(x=-0.85, z=0.5, who="b", size=0.93, tilt=4, la=RELAX, ra=RELAX), dict(x=0.85, z=0.5, who="c", size=0.95, tilt=-4, la=RELAX, ra=RELAX),
          dict(x=-1.9, z=-0.35, who="a", yaw=14, sh=-5, tilt=9, la=RELAX, ra=RELAX), dict(x=0, z=-0.45, who="d", size=1.03, la=RELAX, ra=RELAX),
          dict(x=1.95, z=-0.3, who="e", size=1.02, yaw=-14, sh=5, tilt=-9, ra=RELAX, la=("ik", "r", (0.75, 2.0, 2.3), (1, -0.6, 0)))]
    return sc_beach(cam) + figs(cam, ps, shadow=False)


@card(192, "Elbows row", "G Ly F Par f", "Three lie on their fronts in a row, propped on the elbows with feet kicked up, shoulders touching.",
      "Camera on the ground a few steps in front, level with their eyes.")
def i18():
    cam = Cam(s=84, D=11, hc=1.7, feet_y=636)
    return sc_park(cam) + figs(cam, [prone(x=-2.2, yaw=14, who="c", tilt=5), prone(x=0, who="a", size=1.02),
                                    prone(x=2.2, yaw=-14, who="b", size=0.95, tilt=-5)])


@card(193, "Sunset row", "G Se W Bea b", "Three sit on the sand facing the water, legs out, the middle one with arms round the other two.",
      "Go wide from behind at sunset with the row small and low in the frame.")
def i19():
    cam = Cam(s=52, D=20, hc=3.2, feet_y=640)
    base = dict(py=0.5, yaw=180, bend=-8, ll=(6, 84, 2, 82), rl=(6, 84, 2, 82))
    ps = [P(base, x=-1.75, who="c", sh=5, tilt=-6, la=("ik", "g", (0.75, 0.14, -0.9), (0.6, 0.3, -1)), ra=(8, 30, 0, 60)),
          P(base, x=0, who="a", size=1.02, la=("ik", "w", (-2.3, 2.5, 0.52), (0, 0.2, -1)), ra=("ik", "w", (2.3, 2.45, 0.52), (0, 0.2, -1))),
          P(base, x=1.75, who="b", size=0.94, sh=-5, tilt=6, ra=("ik", "g", (-0.75, 0.14, -0.9), (-0.6, 0.3, -1)), la=(8, 30, 0, 60))]
    return sc_beach(cam, sunset=True) + figs(cam, ps)


@card(194, "Rail row", "G Le F Wat f", "Four lean back on the rail in a row with elbows hooked over it, each crossing a different foot.",
      "Square to the rail and full length with a margin at both ends.")
def i20():
    cam = Cam(s=56, D=17, hc=4.4, feet_y=710)
    zr = -0.62

    def lean(x, who, size, turn, flip):
        legs = dict(rl=(-5, 9, -4, 9), ll=(-2, 14, -9, 4), lf=(12, 30)) if not flip else dict(ll=(-5, 9, -4, 9), rl=(-2, 14, -9, 4), rf=(12, 30))
        return dict(x=x, who=who, size=size, bend=-11, turn=turn,
                    la=("ik", "w", (x + 1.75, 4.2, -0.3), lambda J: V(x + 1.05, 4.36, zr) - J["sl"]),
                    ra=("ik", "w", (x - 1.75, 4.2, -0.3), lambda J: V(x - 1.05, 4.36, zr) - J["sr"]), **legs)

    ps = [lean(-3.3, "c", 0.97, 20, False), lean(-1.1, "a", 1.02, -10, True), lean(1.1, "b", 0.94, 12, False), lean(3.3, "d", 1.0, -20, True)]
    return sc_water_x(cam, zr) + figs(cam, ps, zclip=zr)


@card(195, "Fence row", "G Le F Fie b", "Three lean on the fence side by side with forearms over the top rail, looking out across the field.",
      "Shoot from behind, square to the fence, with the field filling the top half.")
def i21():
    cam = Cam(s=64, D=15, hc=4.4, feet_y=712)
    zr = -1.05

    def lean(x, who, size, turn, knee):
        legs = dict(ll=(0, -8, 0, -8), rl=(0, 12, 0, -30), rf=(8, 40)) if knee == "r" else dict(rl=(0, -8, 0, -8), ll=(0, 12, 0, -30), lf=(8, 40))
        return dict(x=x, yaw=180, who=who, size=size, bend=36, turn=turn, nod=-10,
                    la=("ik", "w", (x - 0.2, 4.42, zr - 1.0), lambda J: V(x - 0.55, 4.36, zr) - J["sl"]),
                    ra=("ik", "w", (x + 0.2, 4.42, zr - 1.0), lambda J: V(x + 0.55, 4.36, zr) - J["sr"]), **legs)

    fence = rail_x(cam, zr, 4.2, "#A9825F", step=2.6)
    return sc_field(cam) + fence + figs(cam, [lean(-2.1, "c", 0.97, -40, "l"), lean(0, "a", 1.02, 0, "r"), lean(2.1, "b", 0.94, 40, "r")], zclip=zr)


@card(196, "Hands in", "G St T Stu s", "Four stand in a ring, each with one arm stretched to the middle so the hands stack on top of each other.",
      "Shoot through a gap in the ring and crop at mid-thigh with the stacked hands in the centre.")
def i22():
    cam = cam_tq(top=130, s=100)
    spots = ((-1.55, 0.6, "a", 1.0), (1.55, 0.6, "c", 0.97), (-0.9, -1.2, "b", 0.94), (0.95, -1.2, "d", 1.03))
    ps = []
    for i, (x, z, w, sz) in enumerate(spots):
        yaw = math.degrees(math.atan2(-x, -0.3 - z))
        sd = "r" if x < 0 else "l"
        p = dict(x=x, z=z, yaw=yaw, who=w, size=sz, bend=14)
        p[sd + "a"] = ("ik", "w", (0.0, 4.55 + 0.1 * i, -0.3), (0, 1, 0))
        p[("l" if sd == "r" else "r") + "a"] = RELAX
        ps.append(p)
    return bg_plain("#DCE2E6", "#E8ECEF") + figs(cam, ps, shadow=False)


@card(197, "Conga", "G Wa F Bea s", "Four walk in a line side-on with hands on the shoulders of the person in front; the leader throws both arms up.",
      "Shoot side-on in burst mode with the whole line in frame and space ahead of the leader.")
def i23():
    cam = Cam(s=54, D=18, hc=4.2, feet_y=712)
    xs, sizes, who = (-3.0, -1.0, 1.0, 3.0), (0.97, 1.02, 0.94, 1.0), "cabd"
    ps = []
    for i in range(4):
        p = walk(1 if i % 2 else -1, x=xs[i], yaw=86, who=who[i], size=sizes[i])
        if i < 3:
            sy = 6.08 * sizes[i + 1] + 0.3
            p["la"] = ("ik", "w", (xs[i + 1] - 0.15, sy, -0.6), (0, -1, 0))
            p["ra"] = ("ik", "w", (xs[i + 1] - 0.15, sy, 0.6), (0, -1, 0))
        else:
            p["la"], p["ra"] = (20, 150, 10, 165), (20, 150, 10, 165)
        ps.append(p)
    return sc_beach(cam) + figs(cam, ps)


@card(198, "Cheer", "G Ac F Fie f", "Five stand in a staggered line and throw their arms up together, each with a different gesture.",
      "Shoot from low with sky behind the hands and count them in.")
def i24():
    cam = Cam(s=52, D=18, hc=3.4, feet_y=716)
    arms = [dict(la=(138, 0, 152, -6), ra=(138, 0, 152, -6)), dict(la=(150, 0, 165, 0), ra=HIP(-1)),
            dict(la=(128, -4, 142, -8), ra=(128, -4, 142, -8)), dict(ra=(150, 0, 165, 0), la=(30, 20, 120, 40)),
            dict(la=(138, 0, 152, -6), ra=(138, 0, 152, -6))]
    xs, zs = (-3.8, -1.9, 0, 1.9, 3.8), (-0.3, 0.3, 0.0, 0.3, -0.3)
    ps = [P(LW if i % 2 else LSTEP, arms[i], x=xs[i], z=zs[i], who=WHO[i], size=(0.97, 1.0, 1.04, 0.94, 1.0)[i], bend=-4, nod=-8) for i in range(5)]
    return sc_field(cam) + figs(cam, ps)


@card(199, "Diagonal line", "G St T Str f", "Line up on a diagonal running away from the camera, bodies angled and shoulders overlapping, all faces to the lens.",
      "Stand at the near end of the line and crop at mid-thigh so the heads step back across the frame.")
def i25():
    cam = cam_tq(top=130, s=96, D=10)
    spots = ((-1.45, 1.0, "a", 1.0, dict(la=CROSS_L, ra=CROSS_R)), (-0.5, 0.2, "c", 0.97, dict(la=POCKET(1), ra=POCKET(-1))),
             (0.45, -0.6, "b", 0.95, dict(la=HIP(1), ra=RELAX)), (1.4, -1.4, "d", 1.03, dict(la=POCKET(1), ra=POCKET(-1))))
    ps = [P(kw, x=x, z=z, yaw=30, turn=-24, who=w, size=sz) for x, z, w, sz, kw in spots]
    return sc_street(cam, stripes=False) + figs(cam, ps, shadow=False)


@card(200, "Class photo", "G St F Ste f", "Stand in two rows on the steps, back row two steps up and offset into the gaps, hands in front or at the sides.",
      "Straight on from the bottom with the camera level, far enough back for a margin all round.")
def i26():
    cam = Cam(s=54, D=17, hc=4.4, feet_y=728)
    o, zf, rise = sc_stairs(cam)
    front = [P(x=x, z=zf(1) - 0.65, gy=rise, who=WHO[i], size=(0.95, 1.0, 0.97)[i], la=CLASP(1), ra=CLASP(-1)) for i, x in enumerate((-1.9, 0, 1.9))]
    back = [P(x=x, z=zf(3) - 0.65, gy=3 * rise, who=WHO[(i + 3) % 5], size=(1.0, 1.03, 0.97, 1.0)[i], la=RELAX, ra=RELAX)
            for i, x in enumerate((-2.85, -0.95, 0.95, 2.85))]
    return o + figs(cam, back + front, shadow=False)
