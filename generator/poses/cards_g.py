"""Batch 3, part 2: solo seated, low and moving."""
from .helpers import *

CH = dict(s=74, D=14, hc=4.2, feet_y=712)


def knees_pole(sd):
    return lambda J: J["k" + sd] - J["s" + sd]


@card(108, "Chair straddle", "S Se F Stu f", "Sit backwards on a chair with legs either side, forearms folded along the top of the backrest.",
      "Square-on at the sitter's chest height. Keep the chair legs and feet in frame.")
def g01():
    cam = Cam(**CH)
    pose = sit(seat=1.9, bend=12, tilt=5, ll=(38, 75, 20, 14), rl=(38, 75, 20, 14),
               la=("ik", "r", (-0.42, 2.04, 0.64), (1, -0.5, 0.2)), ra=("ik", "r", (0.42, 2.12, 0.7), (-1, -0.5, 0.2)))
    return sc_studio(cam) + figs(cam, [pose], extra=chair_front(cam, back="front"))


@card(109, "Elbows on knees", "S Se F Stu f", "Sit forward on the chair, feet apart, elbows on the knees and hands hanging together. Lift the eyes to the lens.",
      "Shoot from the sitter's eye level so the lean reads as engaged rather than slumped.")
def g02():
    cam = Cam(**CH)
    pose = sit(seat=1.9, bend=32, nod=-24, ll=(16, 86, 6, 4), rl=(16, 86, 6, 4),
               la=("ik", "r", (0.14, 0.25, 1.62), knees_pole("l")), ra=("ik", "r", (-0.14, 0.22, 1.64), knees_pole("r")))
    return sc_studio(cam, "#E3DDD3", "#D6CFC4") + figs(cam, [pose], extra=chair_front(cam))


@card(110, "Knee over knee", "S Se F Hom s", "Sit back in the chair with one knee crossed over the other and both hands resting on the top knee.",
      "Shoot side-on at seat height and leave space in front of the knees.")
def g03():
    cam = Cam(**CH)
    pose = sit(seat=1.9, x=-0.3, yaw=80, bend=-6, turn=-30, ll=(4, 86, 0, 6), rl=(-12, 98, -8, 30), rf=(0, 35),
               la=("ik", lambda J: J["kr"] + V(-0.1, 0.34, -0.1)), ra=("ik", lambda J: J["kr"] + V(-0.15, 0.36, 0.1)))
    return sc_home(cam) + figs(cam, [pose], extra=chair_side(cam, -0.3, 1))


@card(111, "Slouch", "S Se F Stu s", "Slide down in the chair, legs stretched out with ankles crossed, hands at the pockets, head back.",
      "Shoot side-on and low so the long diagonal from head to heels crosses the frame.")
def g04():
    cam = Cam(**CH)
    pose = sit(seat=1.9, x=-1.0, yaw=84, bend=-26, nod=12, turn=-20, ll=(3, 57, 0, 57), rl=(-3, 60, -5, 54), lf=(0, -40), rf=(0, -40),
               la=POCKET(1), ra=POCKET(-1))
    return sc_studio(cam) + figs(cam, [pose], extra=chair_side(cam, -1.25, 1))


@card(112, "Bench knee hug", "S Se F Par s", "Sit sideways on the bench with feet up on the seat and wrap both arms around the nearer shin.",
      "Shoot from the front of the bench at seat height, with the empty end of the bench in frame.")
def g05():
    cam = Cam(s=70, D=15, hc=4.2, feet_y=708)
    mid = lambda J: (J["kr"] + J["ar"]) / 2
    pose = dict(x=-1.7, z=0.05, py=2.12, yaw=90, bend=8, turn=-42,
                rl=("ik", "w", (0.1, 1.87, 0.4), (0, 1, 0)), ll=("ik", "w", (1.4, 1.87, -0.25), (0, 1, 0)), rf=(0, -40), lf=(0, -55),
                la=("ik", lambda J: mid(J) + V(0.32, 0.05, -0.12), (1, -0.4, 0.1)), ra=("ik", lambda J: mid(J) + V(0.34, 0.0, 0.12), (-1, -0.4, 0.1)))
    return sc_park(cam) + figs(cam, [pose], extra=bench(cam, -3.3, 3.3))


@card(113, "Bench lean", "S Se F Par f", "Sit forward on the bench with elbows on the knees and hands clasped, head turned to look off to one side.",
      "Camera at seated eye level. Leave space on the side of the gaze.")
def g06():
    cam = Cam(s=70, D=15, hc=4.2, feet_y=708)
    pose = sit(bend=32, turn=36, nod=-18, ll=(14, 86, 5, 4), rl=(14, 86, 5, 4),
               la=("ik", "r", (0.12, -0.02, 1.6), knees_pole("l")), ra=("ik", "r", (-0.12, -0.04, 1.62), knees_pole("r")))
    return sc_park(cam) + figs(cam, [pose], extra=bench(cam, -3.3, 3.3))


@card(114, "Bench with a view", "S Se F Vie b", "Sit at one end of the bench facing the view, one arm stretched along the top of the backrest.",
      "Shoot from behind with the sitter on a third line and the view over the empty end of the bench.")
def g07():
    cam = Cam(s=80, D=13, hc=4.3, feet_y=716)
    pose = sit(x=-0.9, yaw=180, bend=-6, tilt=-6, ra=("ik", "w", (1.45, 3.8, 0.95), (0, -0.6, -1)), la=(8, 30, 0, 60))
    return sc_view(cam) + figs(cam, [pose], extra=bench(cam, -2.9, 2.9, back=-1))


@card(115, "Step recline", "S Se F Ste f", "Sit on a step and lean back with both elbows on the step behind, one foot a step lower than the other.",
      "Straight on with the steps level. Keep the camera at chest height so the chin doesn't dominate.")
def g08():
    cam = Cam(s=80, D=12, hc=3.6, feet_y=650)
    o, zf, rise = sc_stairs(cam)
    pose = dict(x=0, z=0, py=1.92, yaw=-6, bend=-30, nod=26,
                ll=("ik", "w", (0.45, 0.17, 2.75), (0.2, 1, 0.3)), rl=("ik", "w", (-0.5, 0.92, 1.45), (-0.2, 1, 0.3)),
                la=("ik", "w", (2.0, 2.42, -1.15), lambda J: V(0.98, 2.44, -1.05) - J["sl"]),
                ra=("ik", "w", (-2.0, 2.42, -1.15), lambda J: V(-0.98, 2.44, -1.05) - J["sr"]))
    return o + figs(cam, [pose], shadow=False)


@card(116, "Stoop sit", "S Se F Ste f", "Sit on the steps with feet wide on the step below, forearms on the knees and hands hanging.",
      "Get low and shoot slightly upward so the sitter looks down into the lens.")
def g09():
    cam = Cam(s=84, D=12, hc=2.4, feet_y=632)
    o, zf, rise = sc_stairs(cam)
    pose = stair_sitter(zf, rise, 0, 3, "a", bend=24, nod=-12,
                        ll=("ik", "w", (0.85, 2 * rise + 0.17, zf(2) - 0.42), (0.5, 1, 0.3)),
                        rl=("ik", "w", (-0.85, 2 * rise + 0.17, zf(2) - 0.4), (-0.5, 1, 0.3)),
                        la=("ik", "r", (0.18, 0.3, 1.5), knees_pole("l")), ra=("ik", "r", (-0.18, 0.28, 1.52), knees_pole("r")))
    return o + figs(cam, [pose], shadow=False)


@card(117, "Wall dangle", "S Se F Par f", "Sit on a low wall with hands on the edge either side, ankles crossed and swinging, head tilted.",
      "Full length from the front. Keep the wall level and both feet in frame.")
def g10():
    cam = Cam(s=74, D=14, hc=4.4, feet_y=712)
    pose = sit(z=0.05, tilt=6, sh=-2, ll=(4, 89, 6, -2), rl=(0, 89, -10, 8),
               la=("ik", "p", (1.0, -0.28, -0.05), (0.6, 0.3, -1)), ra=("ik", "p", (-1.0, -0.28, -0.05), (-0.6, 0.3, -1)))
    return sc_park(cam) + figs(cam, [pose], extra=lowwall(cam))


@card(118, "Knee up on the wall", "S Se F Vie f", "Sit on the wall with one foot up on it, arms wrapped around that knee, other leg hanging.",
      "Shoot from the front with the view behind. Camera at the sitter's chest height.")
def g11():
    cam = Cam(s=74, D=14, hc=4.4, feet_y=712)
    mid = lambda J: (J["kl"] + J["al"]) / 2
    pose = sit(z=0.05, yaw=-12, bend=8, tilt=6, rl=(4, 89, 0, 4),
               ll=("ik", "r", (0.55, -0.25, 0.42), (0.3, 1, 0.4)), lf=(20, 0),
               la=("ik", lambda J: mid(J) + V(0.15, 0.05, 0.32), (1, -0.4, 0.2)), ra=("ik", lambda J: mid(J) + V(-0.15, 0.0, 0.34), (-1, -0.4, 0.2)))
    return sc_view(cam) + figs(cam, [pose], extra=lowwall(cam))


@card(119, "Cross-legged", "S Se F Hom f", "Sit cross-legged on the floor, back tall, a hand resting on each knee.",
      "Bring the camera down to the sitter's chest height and shoot square-on.")
def g12():
    cam = Cam(s=110, D=10, hc=2.6, feet_y=690)
    pose = dict(py=0.5, bend=4, tilt=3, ll=("ik", "g", (-0.3, 0.2, 0.85), (1, 0.12, 0.5)), rl=("ik", "g", (0.3, 0.2, 0.7), (-1, 0.12, 0.5)),
                lf=(60, 0), rf=(60, 0),
                la=("ik", lambda J: J["kl"] + V(-0.15, 0.34, 0.05), (1, -0.5, -0.3)), ra=("ik", lambda J: J["kr"] + V(0.15, 0.34, 0.05), (-1, -0.5, -0.3)))
    rug = quad(cam, [(-3, 0, -1.4), (3, 0, -1.4), (3.4, 0, 3), (-3.4, 0, 3)], "#B7C4BD")
    return sc_home(cam, zw=-2.2) + rug + figs(cam, [pose])


@card(120, "Back to the wall", "S Se F Str f", "Sit on the ground against the wall, one leg out straight, the other knee up with a forearm resting on it.",
      "Shoot from low down, square to the wall, with a little ground in front of the feet.")
def g13():
    cam = Cam(s=100, D=11, hc=2.4, feet_y=700)
    zw = -0.62
    pose = dict(py=0.5, yaw=14, bend=-8, turn=-10, ll=(4, 88, 2, 86), lf=(10, -60),
                rl=("ik", "g", (-0.45, 0.17, 1.3), (-0.1, 1, 0.2)),
                ra=("ik", lambda J: J["kr"] + J["Rr"] @ V(0.1, 0.08, 0.8), (-1, -0.4, 0.1)), la=("ik", "g", (0.8, 0.14, 0.2), (1, 0.3, -0.5)))
    return sc_wall(cam, col="#C98F78", zw=zw, dado=None, brick="#B67C66") + figs(cam, [pose], zclip=zw + 0.1)


@card(121, "Elbow recline", "S Ly F Bea s", "Lie back propped on both elbows, one knee up, chin tucked to look along the body toward the camera.",
      "Get down to ground level and shoot side-on so the whole body crosses the frame.")
def g14():
    cam = Cam(s=80, D=12.5, hc=2.4, feet_y=690)
    pose = dict(x=-0.3, py=0.5, yaw=80, bend=-58, nod=34, turn=-36, ll=(2, 86, 0, 86), lf=(0, -50),
                rl=("ik", "g", (-0.3, 0.17, 1.5), (0, 1, 0.2)),
                la=("ik", "g", (0.6, 0.14, -0.6), lambda J: J["P"] + J["Rr"] @ V(0.95, -0.3, -1.75) - J["sl"]),
                ra=("ik", "g", (-0.6, 0.14, -0.6), lambda J: J["P"] + J["Rr"] @ V(-0.95, -0.3, -1.75) - J["sr"]))
    return sc_beach(cam) + figs(cam, [pose])


@card(122, "On the back", "S Ly F Par s", "Lie flat on the back with knees up and both hands behind the head, elbows wide.",
      "Shoot side-on from ground level. Grass or a blanket gives a clean base line.")
def g15():
    cam = Cam(s=80, D=12.5, hc=2.4, feet_y=690)
    pose = dict(x=0.5, py=0.5, yaw=85, bend=-88, nod=-4,
                ll=("ik", "g", (0.3, 0.17, 1.35), (0, 1, 0.2)), rl=("ik", "g", (-0.3, 0.17, 1.45), (0, 1, 0.2)),
                la=("ik", lambda J: J["head"] + J["Rr"] @ V(0.42, 0.0, -0.3), (1, 0.3, 0)),
                ra=("ik", lambda J: J["head"] + J["Rr"] @ V(-0.42, 0.0, -0.3), (-1, 0.3, 0)))
    return sc_park(cam) + figs(cam, [pose])


@card(123, "Side lying", "S Ly F Bea f", "Lie on one side facing the camera, head propped on a hand, top knee bent forward, free hand on the ground.",
      "Camera at ground level and square to the body. Leave a little space beyond the feet.")
def g16():
    cam = Cam(s=72, D=13, hc=2.2, feet_y=690)
    pose = dict(x=0.5, py=0.74, hip=-88, sh=-84, tilt=-48, ll=(0, 0, 0, 8), rl=(0, 38, 0, -28),
                la=("ik", lambda J: J["head"] + J["Rh"] @ V(0.4, -0.15, 0.0), lambda J: V(0.3, -1, 0.4)),
                ra=("ik", "w", (1.1, 0.22, 0.9), (0, 0.5, 1)))
    return sc_beach(cam) + figs(cam, [pose])


@card(124, "Swing", "S Se F Par s", "Sit on the swing holding both ropes, lean back and stretch the legs out in front.",
      "Shoot side-on in burst mode and keep the frame at the front of the arc.")
def g17():
    cam = Cam(s=70, D=14, hc=4.2, feet_y=712)
    sx = -0.4
    pose = sit(seat=2.0, x=sx, yaw=86, bend=-16, nod=-6, turn=-14, ll=(3, 72, 0, 48), rl=(3, 78, 0, 56), lf=(0, -20), rf=(0, -20),
               ra=("ik", "w", (sx, 4.7, 0.62), (0, -1, -0.5)), la=("ik", "w", (sx, 4.7, -0.62), (0, -1, -0.5)))
    rope = lambda z: LN(cam.p(V(sx, 1.95, z)), cam.p(V(sx, 15, z)), "#8C6A4C", 4)
    extra = box(cam, sx - 0.5, sx + 0.5, 1.82, 2.0, -0.7, 0.7, "#B8926E", "#A9825F") + [Raw(-0.75, rope(-0.62)), Raw(0.6, rope(0.62))]
    return sc_park(cam) + figs(cam, [pose], extra=extra)


@card(125, "Window seat", "S Se F Hom s", "Sit sideways in the window with the back against the frame, near knee up, hands on the knee, looking out.",
      "Expose for the window light and shoot from inside the room at seat height.")
def g18():
    cam = Cam(s=74, D=14, hc=4.0, feet_y=716)
    zw = -1.3
    o = R(0, 0, W, H, "#E9E0D2")
    o += zrect(cam, zw, -3.4, 2.0, 3.4, 9.6, "#FFFFFF") + zrect(cam, zw, -3.15, 2.0, 3.15, 9.35, "#CFE2E8")
    o += zrect(cam, zw, -3.15, 2.0, 3.15, 4.4, "#B9D2C0") + zrect(cam, zw, -0.08, 2.0, 0.08, 9.35, "#FFFFFF")
    o += R(0, cam.gy(0.3), W, H, "#CDAE88")
    extra = box(cam, -3.4, 3.4, 0, 2.0, zw, 0.3, "#F4EEE6", "#E0D6C8")
    extra += box(cam, -4.0, -3.4, 0, 14, zw, 0.3, "#E9E0D2", "#E9E0D2", "#DCD2C2") + box(cam, 3.4, 4.0, 0, 14, zw, 0.3, "#E9E0D2", "#E9E0D2", "#DCD2C2")
    pose = sit(seat=2.0, x=-2.3, z=-0.45, yaw=90, bend=-10, turn=28,
               rl=("ik", "w", (-0.3, 2.17, -0.2), (0, 1, 0)), ll=("ik", "w", (0.8, 2.17, -0.75), (0, 1, 0)), rf=(0, -50), lf=(0, -55),
               ra=("ik", lambda J: J["kr"] + V(0.1, 0.32, 0.1)), la=("ik", lambda J: J["kr"] + V(0.2, 0.28, -0.15)))
    return o + figs(cam, [pose], extra=extra, shadow=False)


@card(126, "Desk candid", "S Se T Hom s", "Sit at the desk with both hands on the laptop and turn the head toward the camera mid-task.",
      "Shoot from the side of the desk at seated eye level. Clear the clutter behind the screen.")
def g19():
    cam = Cam(s=120, D=10, hc=4.6, feet_y=455 + 4.6 * 120)
    o = R(0, 0, W, H, "#E9E0D2") + R(60, 90, 150, 190, "#B88A63") + R(74, 104, 122, 162, "#DDE6D8") + R(420, 150, 140, 12, "#8A6F5A")
    o += R(440, 96, 26, 54, "#7A8C8A") + R(474, 110, 40, 40, "#C9775A") + R(0, cam.gy(-2.5), W, H, "#CDAE88")
    desk = box(cam, 0.1, 3.6, 3.0, 3.2, -1.0, 1.0, "#D9C3A5", "#B99F7E", "#A98F6E")
    desk.append(Raw(-1.05, zrect(cam, 0.9, 3.2, 0, 3.4, 3.0, "#8A6F5A")))
    lap = quad(cam, [(0.45, 3.2, -0.55), (1.55, 3.2, -0.55), (1.55, 3.2, 0.55), (0.45, 3.2, 0.55)], "#9AA4AB")
    lap += quad(cam, [(1.55, 3.2, -0.55), (1.95, 4.3, -0.55), (1.95, 4.3, 0.55), (1.55, 3.2, 0.55)], "#55616A",
                extra=' stroke="%s" stroke-width="2.5" stroke-linejoin="round"' % INK)
    pose = sit(seat=1.9, x=-1.2, yaw=82, bend=14, turn=-52,
               la=("ik", "w", (0.75, 3.36, -0.3), (0.3, -1, 0)), ra=("ik", "w", (0.8, 3.36, 0.3), (-0.3, -1, 0)))
    return o + figs(cam, [pose], extra=desk + [Raw(-0.6, lap)] + chair_side(cam, -1.2, 1), shadow=False)


@card(127, "Counter stool", "S Se T Caf s", "Sit side-on on a high stool, feet on the rung, one forearm on the counter with a cup, other hand on the thigh.",
      "Shoot along the counter and crop below the knees. Leave space in front of the face.")
def g20():
    cam = Cam(s=110, D=11, hc=5.0, feet_y=430 + 5.0 * 110)
    extra = box(cam, 0.6, 6, 0, 4.4, -1.2, 1.0, "#C99C75", "#A57750", "#96683F")
    extra += box(cam, -1.55, -0.3, 2.72, 2.9, -0.6, 0.6, "#6B7780", "#55616A")
    extra.append(Raw(-0.7, zrect(cam, 0, -1.0, 0, -0.85, 2.75, "#3F4A52") + zrect(cam, 0.5, -1.5, 1.0, -0.35, 1.1, "#3F4A52")))
    J = solve(sit(seat=2.9, x=-0.9, yaw=84, bend=8, turn=-26,
                  ll=("ik", "r", (0.3, -2.1, 0.8), (0.2, 0.3, 1)), rl=("ik", "r", (-0.3, -2.1, 0.85), (-0.2, 0.3, 1)),
                  ra=("ik", "w", (1.3, 4.72, 0.4), lambda J: V(0.8, 4.5, 0.7) - J["sr"]), la=("ik", on_thigh("l"))))
    extra.append(small_cup(cam, J["hdr"] + V(0.05, -0.05, 0), z=float(J["hdr"][2]) + 0.3))
    return cafe_side(cam) + figs(cam, [J], extra=extra, shadow=False)


@card(128, "Edge of the bed", "S Se F Hom f", "Sit on the edge and lean back on both hands, legs stretched forward with ankles crossed, head tilted.",
      "Square-on at seated chest height with some floor in front of the feet.")
def g21():
    cam = Cam(s=74, D=14, hc=4.0, feet_y=716)
    bed = box(cam, -4.8, 4.8, 0, 1.9, -3.0, 0.4, "#F1EBE2", "#D9D0C4")
    pose = sit(seat=1.9, bend=-22, tilt=6, nod=10, ll=(4, 64, 0, 40), rl=(-4, 68, -6, 36), lf=(10, -10), rf=(10, -10),
               la=("ik", "r", (0.85, -0.25, -0.9), (0.6, 0.3, -1)), ra=("ik", "r", (-0.85, -0.25, -0.9), (-0.6, 0.3, -1)))
    return sc_home(cam, zw=-3.4) + figs(cam, [pose], extra=bed)


@card(129, "Sunset sit", "S Se W Bea b", "Sit on the sand facing the water, legs out, leaning back on both hands.",
      "Go wide from behind with the figure small and low in the frame against the bright sky.")
def g22():
    cam = Cam(s=54, D=20, hc=3.4, feet_y=640)
    pose = dict(x=1.6, py=0.5, yaw=180, bend=-16, tilt=-6, ll=(6, 84, 2, 82), rl=(6, 84, 2, 82),
                la=("ik", "g", (0.75, 0.14, -0.9), (0.6, 0.3, -1)), ra=("ik", "g", (-0.75, 0.14, -0.9), (-0.6, 0.3, -1)))
    return sc_beach(cam, sunset=True) + figs(cam, [pose])


@card(130, "Walk away", "S Wa F Str b", "Walk away from the camera across the street with hands at the pockets and an easy stride.",
      "Shoot a burst from behind and keep the frame with the legs at full stride.")
def g23():
    cam = Cam(**FULL)
    return sc_street(cam) + figs(cam, [walk(1, yaw=178, la=POCKET(1), ra=POCKET(-1))])


@card(131, "Walk and text", "S Wa F Str f", "Walk toward the camera looking down at the phone in one hand, other arm swinging.",
      "A candid city frame. Shoot a burst and keep the one where the face is still visible.")
def g24():
    cam = Cam(**FULL)
    J = solve(walk(-1, yaw=-3, nod=24, ra=PHONE(-1)))
    return sc_street(cam) + figs(cam, [J], extra=[phone(cam, J)])


@card(132, "Shoreline stroll", "S Wa W Bea s", "Stroll along the water's edge side-on, hands at the pockets, eyes down at the sand.",
      "Go wide, place the walker small on a third line and leave the beach open ahead of them.")
def g25():
    cam = Cam(**WIDE)
    return sc_beach(cam) + figs(cam, [walk(1, x=-1.6, yaw=84, nod=12, la=POCKET(1), ra=POCKET(-1))])


@card(133, "Stairs down", "S Wa F Ste f", "Come down the steps toward the camera mid-stride, arms swinging, eyes on the next step.",
      "Stand at the bottom, keep the camera level and shoot a burst as they descend.")
def g26():
    cam = Cam(s=72, D=14, hc=4.4, feet_y=745)
    o, zf, rise = sc_stairs(cam)
    pose = dict(x=0, z=-0.55, py=5.38, bend=4, nod=12, rl=("ik", "w", (-0.38, 1.67, 0.02), (0, 0.2, 1)),
                ll=("ik", "w", (0.38, 2.42, -1.2), (0, 0.2, 1)), la=(5, 18, 2, 32), ra=(5, -16, 2, -4))
    return o + figs(cam, [pose], shadow=False)


@card(134, "Wave back", "S Wa T Par b", "Walk away, then twist round to look back and wave with the arm on that side.",
      "Crop at mid-thigh and shoot as they turn, so the body is still heading away.")
def g27():
    cam = cam_tq()
    return sc_path(cam) + figs(cam, [walk(1, yaw=176, twist=28, turn=70, la=WAVE)], shadow=False)


@card(135, "Run in", "S Ac F Par f", "Run straight at the camera with a high knee and bent arms pumping.",
      "Shoot a burst from low down along the path and keep the frame with both feet off the ground.")
def g28():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    pose = P(py=4.3, bend=10, nod=-6, rl=(3, 62, 2, -25), rf=(8, 20), ll=(3, -18, 2, -85), lf=(8, 55), la=(8, 35, -8, 125), ra=(8, -40, 0, 40))
    return sc_path(cam) + figs(cam, [pose])


@card(136, "Tuck jump", "S Ac F Bea f", "Jump and pull both knees up to the chest, arms wrapped round the shins.",
      "Shoot from low in burst mode with sky behind the whole figure.")
def g29():
    cam = Cam(s=62, D=15, hc=4.2, feet_y=720)
    pose = P(py=5.7, bend=12, nod=-6, ll=(16, 100, 8, 12), rl=(16, 100, 8, 12), lf=(10, 30), rf=(10, 30),
             la=("ik", lambda J: shin_mid(J) + V(0.2, 0, 0.34), (1, -0.3, 0.2)), ra=("ik", lambda J: shin_mid(J) + V(-0.2, 0, 0.34), (-1, -0.3, 0.2)))
    return sc_beach(cam) + figs(cam, [pose])


@card(137, "Spin", "S Ac F Fie f", "Turn on one foot with the other foot tucked at the knee and both arms rounded overhead.",
      "Shoot a burst through the turn and keep the frame where the face comes round to the lens.")
def g30():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    pose = P(yaw=24, nod=-6, ll=(-2, 0, -1, 0), rl=("ik", lambda J: J["kl"] + V(-0.28, 0.05, 0.12), (-1, 0, 0.35)), rf=(0, 75),
             la=("ik", "c", (0.3, 3.95, 0.25), (1, 0.3, 0.2)), ra=("ik", "c", (-0.3, 3.95, 0.25), (-1, 0.3, 0.2)))
    return sc_field(cam) + figs(cam, [pose])


@card(138, "Big stride", "S Ac F Str s", "Take an exaggerated leaping stride across the frame, front leg stretched out and arms swinging wide.",
      "Shoot side-on in burst mode and leave space ahead of the front foot.")
def g31():
    cam = Cam(s=62, D=15, hc=4.4, feet_y=712)
    pose = P(py=4.15, yaw=82, bend=8, rl=(0, 62, 0, 40), rf=(0, -20), ll=(0, -50, 0, -72), lf=(4, 50), la=(5, 50, 0, 72), ra=(5, -50, 0, -30))
    return sc_street(cam) + figs(cam, [pose])


@card(139, "Beach wanderer", "S Wa W Bea b", "Walk away along the beach at an unhurried pace, arms loose.",
      "Go wide at sunset with the walker small on a third line and the sun over the opposite side.")
def g32():
    cam = Cam(**WIDE)
    return sc_beach(cam, sunset=True) + figs(cam, [walk(1, x=2.2, yaw=172)])


@card(140, "Through the grass", "S Wa W Fie s", "Walk side-on through the field with one hand trailing out over the grass.",
      "Go wide in low sun, keep the walker small and leave open field ahead of them.")
def g33():
    cam = Cam(**WIDE)
    return sc_field(cam) + figs(cam, [walk(-1, x=-1.4, yaw=80, nod=8, ra=(30, 8, 38, 14))])
