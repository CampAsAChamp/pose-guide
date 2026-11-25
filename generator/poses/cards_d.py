"""Solo cards 39-52."""
from .scenes import *
from .cards_c import kneel


def k39():   # jacket sling
    cam = cam_tq()
    pose = dict(x=0, yaw=16, hip=-5, sh=3, turn=-16, tilt=-3,
                rl=(-7, 0, -5, 0), ll=(14, 10, 9, -6),
                ra=("ik", "c", (-0.62, 2.5, -0.3), (-0.35, -0.3, 1)), la=POCKET(1))
    J = solve(pose)
    sx, sy = float(J["sr"][0]), float(J["sr"][1])
    jk = zrect(cam, -0.7, sx - 0.95, sy - 2.5, sx + 0.25, sy + 0.42, "#5F6B7A", rx=18)
    return sc_street(cam, stripes=False) + figs(cam, [J], extra=[Raw(-0.75, jk)], shadow=False)


def k40():   # lawn lounge
    cam = Cam(s=76, D=13, hc=2.8, feet_y=690)
    pose = dict(x=-1.7, py=0.5, yaw=80, bend=-28, turn=-44, tilt=-4, nod=-8,
                rl=(2, 88, 0, 84), ll=(0, 86, -6, 88), rf=(0, -50), lf=(0, -50),
                la=("ik", "g", (0.6, 0.14, -1.15), (0.6, 0.3, -1)), ra=("ik", "g", (-0.6, 0.14, -1.1), (-0.6, 0.3, -1)))
    return sc_park(cam) + figs(cam, [pose])


def k41():   # chin rest
    cam = Cam(s=120, D=10, hc=4.6, feet_y=455 + 4.6 * 120)
    tx = 0.9
    extra = [Raw(q.z(), q._svg) for q in box(cam, tx - 1.0, tx + 1.0, 3.0, 3.15, -0.9, 0.9, "#C99C75", "#A57750")]
    extra.append(Raw(-0.95, zrect(cam, 0, tx - 0.12, 0, tx + 0.12, 3.0, "#6B5B50")))
    pose = sit(x=-1.15, yaw=78, who="a", bend=20, turn=-14, nod=-8,
               ra=("ik", lambda J: J["head"] + J["Rh"] @ V(-0.1, -0.62, 0.34), lambda J: V(0.05, 3.3, 0.5) - J["sr"]),
               la=("ik", "w", (0.55, 3.38, -0.25), (0.3, -1, 0)))
    extra.append(small_cup(cam, V(1.05, 3.15, 0.3)))
    return cafe_side(cam) + figs(cam, [pose], extra=extra, shadow=False)


def k42():   # stair climb
    cam = Cam(s=72, D=14, hc=4.4, feet_y=745)
    o, zf, rise = sc_stairs(cam)
    pose = dict(x=0.2, z=zf(2) - 0.9, py=5.45, yaw=180, twist=-26, turn=-64, bend=6,
                ll=("ik", "w", (-0.25, 3 * rise + 0.17, zf(3) - 0.55), (0, 0.2, 1)),
                rl=("ik", "w", (0.62, 2 * rise + 0.17, zf(2) - 0.5), (0, 0.2, 1)),
                la=(5, 16, 2, 30), ra=(5, -14, 2, -4))
    return o + figs(cam, [pose], shadow=False)


def k43():   # dock sit
    cam = Cam(s=74, D=13, hc=3.4, feet_y=650)
    zend = -1.2
    pose = dict(x=0.5, z=zend + 0.45, py=0.5, yaw=180, bend=-14, tilt=6, turn=-14,
                ll=(8, 90, 0, 0), rl=(8, 90, 0, 0),
                la=("ik", "g", (0.8, 0.14, -0.75), (0.6, 0.3, -1)), ra=("ik", "g", (-0.8, 0.14, -0.7), (-0.6, 0.3, -1)))
    J = solve(pose)
    J["noshins"] = True
    return sc_pier(cam, zend) + figs(cam, [J])


def k44():   # rail recline
    cam = Cam(**FULL)
    zr = -0.62
    pose = dict(x=0, yaw=8, bend=-11, turn=-16, hip=-4,
                rl=(-5, 9, -4, 9), ll=(-2, 14, -9, 4), lf=(12, 30),
                la=("ik", "w", (1.95, 4.2, -0.3), lambda J: V(1.15, 4.36, zr) - J["sl"]),
                ra=("ik", "w", (-1.85, 4.2, -0.3), lambda J: V(-1.05, 4.36, zr) - J["sr"]))
    return sc_water_x(cam, zr) + figs(cam, [pose], zclip=zr)


def k45():   # headshot turn
    cam = cam_tq(top=140, s=300, hc=6.6, D=6)
    pose = dict(x=0.05, yaw=34, turn=-30, tilt=4, nod=2)
    return bg_plain("#DDD8D0", "#EAE6DF") + figs(cam, [pose], shadow=False)


def k46():   # one knee
    cam = Cam(s=92, D=12, hc=2.8, feet_y=700)
    pose = kneel(x=0, yaw=-22, turn=14, nod=-6, bend=6)
    return sc_field(cam) + figs(cam, [pose])


def k47():   # beach run
    cam = Cam(s=66, D=15, hc=4.4, feet_y=712)
    pose = dict(x=-0.2, py=4.35, yaw=76, bend=12, turn=-8,
                rl=(0, 58, 0, -18), rf=(4, 20), ll=(0, -24, 0, -98), lf=(4, 60),
                la=(6, 42, -4, 132), ra=(6, -46, 2, 44))
    return sc_beach(cam) + figs(cam, [pose])


def k48():   # rock sit
    cam = Cam(s=46, D=22, hc=4.4, feet_y=654)
    rock = box(cam, 1.25, 3.1, 0, 1.7, -0.85, 0.85, "#B7B2A8", "#9E998F", "#A9A49A")
    pose = sit(x=2.15, yaw=-84, bend=-4, turn=4,
               la=("ik", lambda J: J["kl"] + V(0.3, 0.36, 0)), ra=("ik", "g", (-0.2, 1.84, -0.75), (-0.5, 0.2, -1)))
    return sc_view(cam) + figs(cam, [pose], extra=rock)


def k49():   # elbows on the grass
    cam = Cam(s=120, D=9, hc=1.7, feet_y=640)
    pose = dict(x=0.1, z=-2.3, py=0.5, yaw=-14, bend=70, nod=-62, turn=6, who="a",
                ll=(8, -90, 6, -150), rl=(8, -90, 8, -128), lf=(0, 0), rf=(0, 0),
                la=("ik", "g", (0.35, 0.16, 2.75), (0.9, -0.6, 0.3)), ra=("ik", "g", (-0.2, 0.16, 2.8), (-0.9, -0.6, 0.3)))
    return sc_park(cam) + figs(cam, [pose])


def k50():   # coffee walk
    cam = cam_tq()
    pose = walk(1, x=0, yaw=6, turn=-18, tilt=-2, la=POCKET(1),
                ra=("ik", "c", (-0.42, 1.5, 0.78), (-0.6, -1, 0)))
    J = solve(pose)
    cup = small_cup(cam, J["hdr"] + V(0, -0.1, 0.05), z=float(J["hdr"][2]) + 0.3)
    return sc_street(cam, stripes=False) + figs(cam, [J], extra=[cup], shadow=False)


def k51():   # hero stance
    cam = Cam(s=82, D=12, hc=1.5, feet_y=744)
    pose = dict(x=0, yaw=-6, nod=-10, ll=(11, 0, 9, 0), rl=(11, 0, 9, 0), la=HIP(1), ra=HIP(-1))
    return sc_field(cam) + figs(cam, [pose])


def k52():   # cuff check
    cam = cam_waist(s=170)
    pose = dict(x=0, yaw=-14, nod=24, turn=12, tilt=3, sh=2,
                ra=("ik", "c", (0.12, 1.02, 0.55), (-0.8, -0.6, 0.2)), la=("ik", "c", (-0.12, 1.1, 0.6), (0.8, -0.6, 0.2)))
    return sc_street(cam, stripes=False) + figs(cam, [pose], shadow=False)


SOLO2 = [k39, k40, k41, k42, k43, k44, k45, k46, k47, k48, k49, k50, k51, k52]
