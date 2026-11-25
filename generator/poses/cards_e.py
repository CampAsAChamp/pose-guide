"""Partner cards 53-59 and group cards 60-64."""
from .scenes import *
from .samples import on_thigh


def k53():   # step lean
    cam = Cam(s=84, D=12, hc=3.8, feet_y=347 + 3.8 * 84)
    o, zf, rise = sc_stairs(cam)
    a = stair_sitter(zf, rise, -0.85, 2, "a", yaw=8, bend=10, tilt=6,
                     la=("ik", "w", (1.6, 1.5 + 2.55, -0.45), (0, 0.3, -1)))
    b = stair_sitter(zf, rise, 0.75, 2, "b", size=0.93, yaw=-6, bend=8, sh=9, tilt=-14,
                     la=("ik", lambda J: J["kl"] + V(-0.5, 0.3, 0.1), (1, -0.6, 0.2)),
                     ra=("ik", lambda J: J["kl"] + V(-0.75, 0.34, 0.15), (-1, -0.6, 0.2)))
    return o + figs(cam, [a, b], shadow=False)


def k54():   # twirl
    cam = Cam(s=62, D=15, hc=4.4, feet_y=716)
    a = dict(x=-1.25, yaw=18, who="a", hip=-4, rl=(-6, 0, -4, 0), ll=(13, 8, 8, -5), tilt=4, turn=10,
             la=("ik", "w", (0.45, 7.85, 0.15), (1, -0.2, 0.4)), ra=POCKET(-1))
    b = dict(x=1.15, yaw=-38, who="b", size=0.93, twist=-14, turn=24, tilt=-4,
             ll=(-3, 0, -2, 0), rl=(-8, 10, -10, -18), rf=(10, 48),
             ra=("ik", "w", (0.45, 7.7, 0.15), (-1, -0.2, 0.4)), la=(62, 6, 78, 20))
    return sc_field(cam) + figs(cam, [a, b])


def k55():   # follow me
    cam = Cam(s=62, D=15, hc=4.4, feet_y=712)
    b = walk(1, x=1.25, yaw=78, who="b", size=0.93, twist=-30, turn=-72, bend=4,
             ra=("ik", "w", (-0.1, 4.15, 0.4), (-0.2, 0.3, -1)), la=(5, 30, -4, 70))
    a = walk(-1, x=-1.45, yaw=80, who="a", bend=6,
             ra=("ik", "w", (-0.22, 4.15, 0.4), (-0.3, -1, 0)), la=(5, -22, 2, -4))
    return sc_beach(cam) + figs(cam, [a, b])


def k56():   # railing duo
    cam = Cam(**FULL)
    zr = -1.05

    def lean(x, who, size, turn, knee):
        legs = dict(ll=(0, -8, 0, -8), rl=(0, 12, 0, -30), rf=(8, 40)) if knee == "r" else \
            dict(rl=(0, -8, 0, -8), ll=(0, 12, 0, -30), lf=(8, 40))
        return dict(x=x, yaw=180, who=who, size=size, bend=36, turn=turn, nod=-10,
                    la=("ik", "w", (x - 0.2, 4.42, zr - 1.0), lambda J: V(x - 0.55, 4.36, zr) - J["sl"]),
                    ra=("ik", "w", (x + 0.2, 4.42, zr - 1.0), lambda J: V(x + 0.55, 4.36, zr) - J["sr"]), **legs)

    a = lean(-0.95, "a", 1.0, -52, "l")
    b = lean(0.95, "b", 0.93, 52, "r")
    return sc_water_x(cam, zr) + figs(cam, [a, b], zclip=zr)


def k57():   # cheek to cheek
    cam = cam_tq(top=130, s=150, hc=5.5, D=8)
    a = dict(x=-0.66, yaw=16, who="a", sh=-4, tilt=13,
             la=("ik", "w", (1.5, 5.85, -0.3), (0, 0.3, -1)), ra=RELAX)
    b = dict(x=0.6, z=0.15, yaw=-18, who="b", size=0.95, sh=4, tilt=-13,
             ra=("ik", "w", (-0.5, 5.25, 0.66), (-0.6, -1, 0.3)), la=RELAX)
    return bg_window() + figs(cam, [a, b], shadow=False)


def k58():   # high five
    cam = Cam(s=62, D=15, hc=4.4, feet_y=714)
    a = walk(1, x=-1.45, yaw=68, who="c", bend=5, turn=-6,
             ra=("ik", "w", (-0.08, 7.5, 0.35), (-0.4, -0.3, 1)), la=(5, -20, 2, -4))
    b = walk(-1, x=1.45, yaw=-68, who="d", size=1.02, bend=5, turn=6,
             la=("ik", "w", (0.08, 7.55, 0.35), (0.4, -0.3, 1)), ra=(5, -20, 2, -4))
    return sc_path(cam) + figs(cam, [a, b])


def sofa_front(cam, x0=-4.3, x1=4.3):
    c1, c2, c3 = "#8FA7A0", "#7C958E", "#A4B8B2"
    s = box(cam, x0, x1, 0, 3.9, -1.5, -0.9, c3, c2)
    s += box(cam, x0 + 0.8, x1 - 0.8, 0.5, 1.7, -0.9, 0.9, c3, c1)
    s += box(cam, x0, x0 + 0.8, 0, 2.8, -1.5, 0.9, c3, c2, c1)
    s += box(cam, x1 - 0.8, x1, 0, 2.8, -1.5, 0.9, c3, c2, c1)
    return s


def k59():   # sofa lean
    cam = Cam(s=74, D=14, hc=3.9, feet_y=722)
    a = sit(x=-0.8, z=0.1, yaw=6, who="a", bend=-8, tilt=6,
            la=("ik", "w", (1.6, 4.1, -0.35), (0, 0.3, -1)), ra=("ik", on_thigh("r")),
            rl=(10, 88, 6, 4), ll=(4, 89, 0, 10))
    b = sit(x=0.72, z=0.1, size=0.93, yaw=-8, who="b", bend=-4, sh=10, tilt=-14,
            la=("ik", "c", (0.2, 1.3, 0.8), (0.4, -1, 0)), ra=("ik", "c", (-0.2, 1.3, 0.8), (-0.4, -1, 0)))
    Jb = solve(b)
    return sc_home(cam, zw=-3.2) + figs(cam, [a, Jb], extra=sofa_front(cam, -3.6, 3.6) + [mug(cam, Jb)])


def k60():   # hands-up line, from behind
    cam = Cam(s=50, D=20, hc=4.4, feet_y=694)
    xs = (-3.3, -1.1, 1.1, 3.3)
    mids = (-2.2, 0.0, 2.2)
    whos, sizes = ("c", "a", "b", "d"), (0.97, 1.03, 0.95, 1.0)
    ps = []
    for i, x in enumerate(xs):
        p = dict(x=x, yaw=180, who=whos[i], size=sizes[i], nod=-8, ll=(7, 0, 5, 0), rl=(7, 0, 5, 0))
        # facing away: the figure's left hand is on screen left
        p["la"] = ("ik", "w", (mids[i - 1] + 0.07, 7.9, 0.0), (0.5, 0, -1)) if i > 0 else (150, 0, 165, 0)
        p["ra"] = ("ik", "w", (mids[i] - 0.07, 7.9, 0.0), (-0.5, 0, -1)) if i < 3 else (150, 0, 165, 0)
        ps.append(p)
    return sc_beach(cam, sunset=True) + figs(cam, ps)


def k61():   # wall trio
    cam = Cam(s=62, D=16, hc=4.4, feet_y=712)
    zw = -0.72
    o = sc_wall(cam, col="#C98F78", zw=zw, dado=None, brick="#B67C66")
    a = mirror(dict(x=2.6, yaw=-12, bend=-8, turn=24, who="c", rl=(3, 10, 2, 10), ll=(6, 38, 2, -62), lf=(0, 80),
                    la=CROSS_L, ra=CROSS_R))
    b = dict(x=0, yaw=2, bend=-8, who="a", size=1.03, tilt=-3,
             ll=(-3, 10, -3, 10), rl=(-9, 16, -9, 6), rf=(10, 40), la=POCKET(1), ra=POCKET(-1))
    c = dict(x=2.6, yaw=-14, bend=-8, who="b", size=0.95, turn=-10, tilt=5, hip=4,
             ll=(-5, 10, -3, 10), rl=(12, 16, 8, 2),
             la=("ik", "c", (0.42, 2.98, -0.2), (1, 0.7, 0.2)), ra=POCKET(-1))
    return o + figs(cam, [a, b, c], zclip=zw + 0.1)


def k62():   # café trio
    cam = Cam(s=100, D=11.5, hc=4.6, feet_y=470 + 4.6 * 100)
    extra = cafe_table(cam, hw=1.15, hd=0.95) + cafe_chair(cam, -1) + cafe_chair(cam, 1)
    a = sit(x=-2.15, yaw=80, who="a", bend=15, nod=-6, turn=-10,
            la=("ik", "w", (-0.7, 3.38, -0.2), (0.3, -1, 0)), ra=("ik", "w", (-0.65, 3.38, 0.3), (-0.3, -1, 0)))
    b = sit(x=2.15, size=0.93, yaw=-80, who="b", bend=14, turn=10,
            la=("ik", "w", (0.75, 3.38, 0.3), (0.3, -1, 0)), ra=("ik", "w", (0.7, 3.36, -0.2), (-0.3, -1, 0)))
    c = sit(x=0, z=-2.0, size=1.02, who="c", bend=8, tilt=-4,
            la=("ik", "w", (0.7, 3.4, -0.8), (0.6, -1, 0)), ra=("ik", "w", (-0.55, 5.1, -1.3), (-0.7, -1, 0.2)))
    Jc = solve(c)
    extra += [small_cup(cam, Jc["hdr"] + V(0, 0.32, 0), z=float(Jc["hdr"][2]) + 0.4),
              small_cup(cam, V(-0.45, 3.15, 0.45)), small_cup(cam, V(0.5, 3.15, 0.5))]
    return cafe_side(cam) + figs(cam, [a, b, Jc], extra=extra, shadow=False)


def k63():   # arm in arm, walking away
    cam = Cam(s=60, D=16, hc=4.4, feet_y=710)
    l = walk(1, x=-1.85, yaw=178, who="c", size=0.97, ra=("ik", "w", (0.35, 4.6, 0.55), (0, -0.2, -1)), la=(5, 14, 2, 26))
    m = walk(-1, x=0, yaw=180, who="a", size=1.03, turn=-70, twist=-22,
             la=("ik", "w", (-2.35, 5.95, 0.5), (0, 0.2, -1)), ra=("ik", "w", (2.3, 5.8, 0.5), (0, 0.2, -1)))
    r = walk(1, x=1.8, yaw=182, who="b", size=0.94, la=("ik", "w", (-0.35, 4.4, 0.57), (0, -0.2, -1)), ra=(5, -14, 2, -4))
    return sc_path(cam) + figs(cam, [l, m, r])


def k64():   # trio portrait
    cam = cam_tq(top=150, s=126, hc=5.5, D=9)
    b = dict(x=0, z=0.4, who="b", size=0.95, tilt=-2, la=CROSS_L, ra=CROSS_R)
    a = dict(x=-1.2, z=-0.25, yaw=20, who="a", sh=-4, tilt=9,
             la=("ik", "w", (-0.62, 6.0, 0.72), (0.6, -0.4, 0.6)), ra=HIP(-1))
    c = dict(x=1.2, z=-0.25, yaw=-20, who="c", size=1.02, sh=4, tilt=-9, la=POCKET(1),
             ra=("ik", "w", (-0.3, 4.6, -0.2), (0, -0.3, -1)))
    return bg_plain("#D9DFE3", "#E7EBEE") + figs(cam, [a, b, c], shadow=False)


PARTNER2 = [k53, k54, k55, k56, k57, k58, k59]
GROUP2 = [k60, k61, k62, k63, k64]
