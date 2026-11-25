"""Partner cards 23-30 and group cards 31-38."""
from .scenes import *
from .samples import on_thigh


def k23():   # forehead touch
    cam = cam_tq(top=120, s=118)
    a = dict(x=-0.9, yaw=80, who="a", bend=8, nod=20,
             ra=("ik", "w", (0.66, 4.0, 0.6), (-1, -0.6, 0)), la=("ik", "w", (0.66, 4.0, -0.6), (1, -0.6, 0)))
    b = dict(x=0.9, yaw=-80, who="b", size=0.93, bend=6, nod=-6,
             la=("ik", "w", (-0.6, 6.2, 0.5), (0.5, -1, 0)), ra=("ik", "w", (-0.6, 6.2, -0.5), (-0.5, -1, 0)))
    return sc_field(cam) + figs(cam, [a, b], shadow=False)


def k24():   # back hug
    cam = cam_tq(top=120, s=118)
    a = dict(x=-0.25, z=-0.38, yaw=6, who="a", bend=6, tilt=12, turn=4,
             la=("ik", "w", (0.4, 4.6, 1.0), (1, -0.3, 0.4)), ra=("ik", "w", (-0.15, 4.5, 1.0), (-1, -0.3, 0.4)))
    b = dict(x=0.2, z=0.45, yaw=10, who="b", size=0.93, tilt=-8, turn=-10,
             la=("ik", "w", (0.3, 4.95, 1.2), (1, -1, 0)), ra=("ik", "w", (0.0, 4.82, 1.22), (-1, -1, 0)))
    return sc_park(cam) + figs(cam, [a, b], shadow=False)


def k25():   # piggyback
    cam = Cam(s=64, D=15, hc=4.4, feet_y=712)
    a = dict(x=0, z=0.1, yaw=0, who="a", bend=14, nod=-10, ll=(6, 8, 3, -4), rl=(6, -6, 3, 4),
             la=("ik", "w", (1.0, 4.0, 0.3), (1, -0.5, -1)), ra=("ik", "w", (-1.0, 4.0, 0.3), (-1, -0.5, -1)))
    b = dict(x=0.55, z=-0.5, py=4.72 / 0.9, who="b", size=0.9, bend=24, tilt=-12, nod=-10, twist=-8,
             ll=("ik", "w", (1.0, 3.1, 1.0), (1, 0.3, 1)), rl=("ik", "w", (-0.95, 3.1, 1.0), (-1, 0.3, 1)),
             lf=(10, 25), rf=(10, 25),
             la=("ik", "w", (-0.3, 5.7, 0.9), (1, 0.2, 0.3)), ra=("ik", "w", (0.35, 5.6, 0.95), (-1, 0.2, 0.3)))
    return sc_path(cam) + figs(cam, [a, b])


def k26():   # side by side
    cam = Cam(**FULL)
    a = dict(x=-0.98, yaw=8, who="a", hip=-5, sh=-3, tilt=5,
             rl=(-6, 0, -4, 0), ll=(14, 8, 9, -5),
             la=("ik", "w", (1.75, 6.0, -0.3), (0, 0.3, -1)), ra=POCKET(-1))
    b = dict(x=0.98, yaw=-8, who="c", size=0.96, sh=3, tilt=-5, hip=4,
             ll=(-6, 0, -4, 0), rl=(-9, 9, -8, -3), rf=(10, 46),
             ra=("ik", "w", (-1.6, 4.5, -0.4), (0, -0.3, -1)), la=(35, 5, 150, 12))
    o = sc_wall(cam, col="#B9C9B5", dado="#A9BBA5", zw=-2.4, plant=-4.6)
    return o + figs(cam, [a, b], zclip=-2.3)


def k27():   # bench for two, from behind
    cam = Cam(s=80, D=13, hc=4.3, feet_y=716)
    a = sit(x=-0.85, yaw=180, who="a", bend=-5, ll=(6, 88, 2, 4), rl=(6, 88, 2, 4),
            ra=("ik", "w", (1.55, 4.15, 0.55), (0, 0.3, -1)), la=(8, 30, 4, 60))
    b = sit(x=0.72, size=0.93, yaw=180, who="b", sh=-9, tilt=14, la=(8, 30, 0, 60), ra=(8, 30, 0, 60))
    return sc_view(cam) + figs(cam, [a, b], extra=bench(cam, -2.9, 2.9, back=-1))


def k28():   # look back
    cam = Cam(**FULL)
    a = walk(1, x=-1.2, yaw=176, who="a", ra=("ik", "w", (-0.06, 3.75, -0.1), (-0.3, 0, -1)))
    b = walk(-1, x=1.2, yaw=184, who="b", size=0.93, twist=30, turn=80,
             la=("ik", "w", (0.06, 3.75, -0.1), (0.3, 0, -1)))
    return sc_path(cam) + figs(cam, [a, b])


def k29():   # back to back
    cam = cam_tq(top=120, s=118)
    a = dict(x=-0.78, yaw=-58, who="a", bend=-3, turn=42, tilt=-3, la=CROSS_L, ra=CROSS_R)
    b = dict(x=0.78, yaw=58, who="c", size=0.96, bend=-3, turn=-42, tilt=3, la=CROSS_L, ra=CROSS_R)
    return bg_plain("#E3DDD3", "#EEE9E1") + figs(cam, [a, b], shadow=False)


def k30():   # table for two
    cam = Cam(s=105, D=11, hc=4.6, feet_y=470 + 4.6 * 105)
    o = R(0, 0, W, H, "#E4D5C3")
    o += R(60, 60, 480, 330, "#8A6F5A") + R(74, 74, 452, 302, "#CFE2E8") + R(74, 250, 452, 126, "#B9D2C0")
    o += C(170, 250, 60, "#9FC2A6") + C(400, 256, 74, "#A9CBAE")
    o += R(294, 74, 12, 302, "#8A6F5A")
    for lx in (150, 450):
        o += R(lx - 2, 0, 4, 60, "#6B5B50")
    o += R(0, cam.gy(-2.5), W, H, "#C9A77E")
    extra = []
    extra += box(cam, -0.95, 0.95, 3.0, 3.15, -0.9, 0.9, "#C99C75", "#A57750")
    extra.append(Raw(-0.95, zrect(cam, 0, -0.12, 0, 0.12, 3.0, "#6B5B50")))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.75, sx * 2.6))
        extra += box(cam, x0, x1, 1.6, 4.3, -0.6, 0.6, "#7A8C8A", "#66787A")
        x0, x1 = sorted((sx * 2.7, sx * 1.35))
        extra += box(cam, x0, x1, 1.5, 1.7, -0.6, 0.6, "#8B9C9A", "#7A8C8A")
    a = sit(x=-1.95, yaw=82, who="a", bend=16, nod=-6,
            la=("ik", "w", (-0.55, 3.38, -0.2), (0.3, -1, 0)), ra=("ik", "w", (-0.5, 3.38, 0.25), (-0.3, -1, 0)))
    b = sit(x=1.95, size=0.93, yaw=-82, who="b", bend=12,
            la=("ik", "w", (1.0, 4.75, 0.3), (0.3, -1, 0)), ra=("ik", "w", (0.5, 3.36, -0.2), (-0.3, -1, 0)))
    Jb = solve(b)
    hb = cam.p(Jb["hdl"] + V(-0.1, 0.1, 0))
    kk = cam.k(0.3)
    cup = ('<rect x="%s" y="%s" width="%s" height="%s" rx="5" fill="#EDE4D8" stroke="%s" stroke-width="2.5"></rect>'
           % (f(hb[0] - 0.19 * kk), f(hb[1] - 0.22 * kk), f(0.38 * kk), f(0.44 * kk), INK))
    ca = cam.p(V(-0.2, 3.15, 0.5))
    cup2 = ('<rect x="%s" y="%s" width="%s" height="%s" rx="5" fill="#EDE4D8" stroke="%s" stroke-width="2.5"></rect>'
            % (f(ca[0] - 0.19 * kk), f(ca[1] - 0.44 * kk), f(0.38 * kk), f(0.44 * kk), INK))
    extra += [Raw(float(Jb["hdl"][2]) + 0.4, cup), Raw(0.5, cup2)]
    return o + figs(cam, [a, Jb], extra=extra, shadow=False)


def k31():   # squad walk
    cam = Cam(s=60, D=16, hc=4.4, feet_y=704)
    ps = [walk(1, x=-2.9, z=-0.7, yaw=6, who="c", la=POCKET(1), turn=20),
          walk(-1, x=-0.95, z=0.35, yaw=2, who="a", turn=-8),
          walk(1, x=0.95, z=0.35, yaw=-2, who="b", size=0.95, la=("ik", "c", (0.42, 2.98, -0.2), (1, 0.7, 0.2)), turn=10),
          walk(-1, x=2.9, z=-0.7, yaw=-6, who="d", size=1.03, ra=POCKET(-1), turn=-18)]
    return sc_street(cam) + figs(cam, ps)


def k32():   # staggered line
    cam = Cam(s=56, D=17, hc=4.5, feet_y=704)
    xs, zs = (-3.5, -1.75, 0, 1.75, 3.5), (0.35, -0.25, 0.1, -0.25, 0.35)
    back = lambda i: (xs[i], 4.7, zs[i] - 0.55)
    sh_ = lambda i, sg: (xs[i] + sg * 0.5, 6.0, zs[i] - 0.45)
    ps = [
        dict(x=xs[0], z=zs[0], yaw=22, who="a", size=0.97, hip=-4, rl=(-6, 0, -4, 0), ll=(13, 8, 8, -5),
             ra=HIP(-1), la=("ik", "w", back(1), (0, -0.3, -1)), tilt=4),
        dict(x=xs[1], z=zs[1], yaw=8, who="c", size=1.02, ra=("ik", "w", back(0), (0, -0.3, -1)),
             la=("ik", "w", sh_(2, 1), (0, 0.3, -1)), tilt=3),
        dict(x=xs[2], z=zs[2], yaw=0, who="d", size=1.05, la=("ik", "w", sh_(3, 1), (0, 0.3, -1)),
             ra=("ik", "w", back(1), (0, -0.3, -1)), hip=3, ll=(-5, 0, -3, 0), rl=(12, 8, 8, -5)),
        dict(x=xs[3], z=zs[3], yaw=-8, who="b", size=0.95, ra=("ik", "w", back(2), (0, -0.3, -1)),
             la=("ik", "w", back(4), (0, -0.3, -1)), tilt=-4),
        dict(x=xs[4], z=zs[4], yaw=-22, who="e", size=1.0, hip=4, ll=(-6, 0, -4, 0), rl=(13, 8, 8, -5),
             ra=("ik", "w", back(3), (0, -0.3, -1)), la=(35, 5, 150, 12), tilt=-4),
    ]
    return sc_park(cam) + figs(cam, ps)


def kneel(**kw):
    p = dict(py=2.33, ll=(2, 0, 0, -86), lf=(180, 8), rl=(8, 86, 3, 0),
             ra=("ik", lambda J: J["kr"] + V(0.0, 0.34, 0.1)), la=HIP(1))
    p.update(kw)
    return p


def k33():   # two rows
    cam = Cam(s=58, D=16, hc=4.0, feet_y=712)
    zb = -1.3
    ps = [
        dict(x=-1.9, z=zb, yaw=10, who="c", ra=HIP(-1), la=("ik", "w", (-0.1, 4.7, zb - 0.55), (0, -0.3, -1)), tilt=4),
        dict(x=0, z=zb, who="d", size=1.04, la=("ik", "w", (2.4, 6.0, zb - 0.45), (0, 0.3, -1)),
             ra=("ik", "w", (-2.4, 6.0, zb - 0.45), (0, 0.3, -1))),
        dict(x=1.9, z=zb, yaw=-10, who="e", size=0.97, la=HIP(1), ra=("ik", "w", (0.1, 4.7, zb - 0.55), (0, -0.3, -1)), tilt=-4),
        kneel(x=-1.0, z=0.55, yaw=16, who="a", turn=-8),
        mirror(kneel(x=-1.05, z=0.55, yaw=16, who="b", size=0.95, turn=-8,
                     ra=("ik", "r", (-0.5, 0.2, 1.75), (-1, -0.3, 0)))),
    ]
    return sc_field(cam) + figs(cam, ps)


def k34():   # selfie huddle
    cam = cam_tq(top=150, s=118, hc=5.4, D=9)
    b = dict(x=0, z=0.45, who="b", size=0.94, tilt=2, la=(8, 6, 4, 30), ra=(8, 6, 4, 30))
    a = dict(x=-1.25, z=-0.2, yaw=14, who="a", sh=-5, tilt=10,
             la=("ik", "w", (0.85, 5.75, 0.35), (0, 0.3, -1)), ra=RELAX)
    c = dict(x=1.25, z=-0.2, yaw=-14, who="c", size=1.02, sh=5, tilt=-10,
             ra=("ik", "w", (-0.85, 5.8, 0.3), (0, 0.3, -1)), la=("ik", "r", (0.75, 2.0, 2.1), (1, -0.6, 0)))
    return sc_park(cam) + figs(cam, [a, b, c], shadow=False)


def k35():   # group jump
    cam = Cam(s=50, D=18, hc=3.8, feet_y=724)
    ps = [
        dict(x=-3.6, py=5.2, who="c", yaw=8, bend=-5, ll=(20, 30, 8, -70), rl=(24, 15, 10, -80), lf=(10, 50), rf=(10, 50),
             la=(140, 0, 155, -8), ra=(135, 5, 150, 0)),
        dict(x=-1.2, py=5.75, who="a", bend=4, ll=(30, 80, 12, 0), rl=(30, 80, 12, 0), lf=(10, 30), rf=(10, 30),
             la=(60, 10, 150, 20), ra=(60, 10, 150, 20), nod=-6),
        dict(x=1.2, py=5.4 / 0.95, who="b", size=0.95, ll=(28, 0, 26, 0), rl=(28, 0, 26, 0), lf=(10, 30), rf=(10, 30),
             la=(118, 0, 124, 0), ra=(118, 0, 124, 0)),
        dict(x=3.6, py=5.9 / 1.03, who="d", size=1.03, yaw=-10, bend=-8, ll=(10, 40, 4, -60), rl=(12, -20, 6, -95),
             lf=(10, 50), rf=(10, 50), la=(150, 0, 165, 0), ra=(20, 30, 100, 60), nod=-8),
    ]
    return sc_beach(cam) + figs(cam, ps)


def k36():   # sofa stack
    cam = Cam(s=62, D=16, hc=3.9, feet_y=716)
    c1, c2, c3 = "#8FA7A0", "#7C958E", "#A4B8B2"
    sofa = []
    sofa += box(cam, -4.3, 4.3, 0, 3.9, -1.5, -0.9, c3, c2)
    sofa += box(cam, -3.5, 3.5, 0.5, 1.7, -0.9, 0.9, c3, c1)
    sofa += box(cam, -4.3, -3.5, 0, 2.8, -1.5, 0.9, c3, c2, c1)
    sofa += box(cam, 3.5, 4.3, 0, 2.8, -1.5, 0.9, c3, c2, c1)
    a = sit(x=-1.9, z=0.1, yaw=14, who="a", bend=-8, tilt=4,
            la=("ik", on_thigh("l")), ra=("ik", "p", (-1.0, -0.26, -0.05), (-0.6, 0.3, -1)))
    b = sit(x=0.9, z=0.1, yaw=-10, who="b", size=0.95, bend=-6, tilt=-4,
            rl=("ik", lambda J: J["kl"] + V(-0.05, 0.46, 0.1), (-1, 0.2, 0.5)), rf=(-78, 8), ll=(6, 88, 2, 6),
            la=("ik", "r", (1.2, 1.3, -0.6), (0.2, -1, -0.2)), ra=("ik", lambda J: (J["kr"] + J["ar"]) / 2 + V(0, 0.38, 0.1)))
    c = dict(x=3.85, z=0.0, py=(2.8 + 0.42) / 1.0, yaw=-24, who="c", sh=4, tilt=-5,
             ll=("ik", "g", (0.35, 0.17, 0.95), (0.3, 0.3, 1)), rl=("ik", "r", (-0.5, -1.9, 1.15), (-0.3, 0.3, 1)), rf=(12, 25),
             ra=("ik", "w", (1.75, 4.05, -0.45), (0, 0.3, -1)), la=("ik", on_thigh("l")))
    d = dict(x=-0.5, z=-2.15, yaw=4, who="d", size=1.03, bend=24, nod=-14,
             la=("ik", "w", (0.35, 4.08, -1.1), (1, -0.4, -0.3)), ra=("ik", "w", (-1.25, 4.08, -1.1), (-1, -0.4, -0.3)))
    return sc_home(cam, zw=-3.2) + figs(cam, [a, b, c, d], extra=sofa)


def k37():   # stair rows
    cam = Cam(s=70, D=14, hc=4.4, feet_y=704)
    rise, tread = 0.75, 1.3
    zf = lambda n: 0.5 - (n - 2) * tread
    o = R(0, 0, W, H, "#E6DDD0")
    top_n = 9
    o += R(0, 0, W, cam.gy(zf(top_n + 1), top_n * rise), "#E9E1D5")
    dz = zf(top_n + 1)
    o += zrect(cam, dz, -2.2, top_n * rise, 2.2, top_n * rise + 9.5, "#B7A894")
    o += zrect(cam, dz, -1.85, top_n * rise, 1.85, top_n * rise + 9.1, "#6F7F86")
    for n in range(top_n, 0, -1):
        y0, y1 = cam.gy(zf(n), n * rise), cam.gy(zf(n), (n - 1) * rise)
        if n * rise < cam.hc:
            yt = cam.gy(zf(n + 1), n * rise)
            o += R(0, yt, W, y0 - yt + 1, "#D6CCBD" if n % 2 else "#CFC5B5")
        o += R(0, y0, W, y1 - y0 + 1, "#B5A998") + R(0, y0, W, 3, "#DCD3C5")
    g0 = cam.gy(zf(1), 0)
    o += R(0, g0, W, H - g0, "#C9C3B9")

    def sitter(x, n, who, size=1.0, **kw):
        pz = zf(n) - 0.5
        fy, fz = (n - 1) * rise + 0.17, zf(n - 1) - 0.42
        p = dict(x=x, z=pz, py=(n * rise + 0.42 * size) / size, size=size, who=who, bend=16,
                 ll=("ik", "w", (x + 0.45, fy, fz), (0.3, 1, 0.3)), rl=("ik", "w", (x - 0.45, fy, fz + 0.05), (-0.3, 1, 0.3)),
                 la=("ik", lambda J: J["kl"] + V(-0.25, 0.3, 0.2), (1, -0.6, 0.2)),
                 ra=("ik", lambda J: J["kr"] + V(0.25, 0.3, 0.2), (-1, -0.6, 0.2)))
        p.update(kw)
        return p

    ps = [sitter(-2.6, 4, "c", yaw=12, tilt=4), sitter(0, 4, "d", size=1.03, bend=10),
          sitter(2.6, 4, "e", size=0.97, yaw=-12, tilt=-4),
          sitter(-1.3, 2, "a", yaw=10, tilt=4, bend=20), sitter(1.3, 2, "b", size=0.95, yaw=-10, tilt=-4, bend=20)]
    return o + figs(cam, ps, shadow=False)


def k38():   # shoulder to shoulder, from behind
    cam = Cam(s=50, D=20, hc=4.4, feet_y=660)
    xs = (-2.7, -0.9, 0.9, 2.7)
    P_ = (0, 0.2, -1)
    ps = [
        dict(x=xs[0], yaw=176, who="c", size=0.97, ra=("ik", "w", (xs[1] - 0.1, 4.6, 0.55), (0, -0.2, -1)),
             la=(150, 0, 165, 0), hip=-3),
        dict(x=xs[1], yaw=180, who="a", size=1.03, ra=("ik", "w", (xs[2] + 0.55, 6.1, 0.52), P_),
             la=("ik", "w", (xs[0] - 0.5, 5.9, 0.52), P_)),
        dict(x=xs[2], yaw=180, who="b", size=0.95, la=("ik", "w", (xs[1] + 0.2, 4.4, 0.56), (0, -0.2, -1)),
             ra=("ik", "w", (xs[3] + 0.5, 5.9, 0.52), P_)),
        dict(x=xs[3], yaw=184, who="d", size=1.0, la=("ik", "w", (xs[2] + 0.1, 4.5, 0.55), (0, -0.2, -1)),
             ra=RELAX, hip=3),
    ]
    return sc_view(cam) + figs(cam, ps)


PARTNER = [k23, k24, k25, k26, k27, k28, k29, k30]
GROUP = [k31, k32, k33, k34, k35, k36, k37, k38]
