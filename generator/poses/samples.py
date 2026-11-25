from .mannequin import *

W, H = 600, 800


def R(x, y, w, h, c, rx=0, extra=""):
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"%s%s></rect>' % (
        f(x), f(y), f(w), f(h), c, (' rx="%s"' % f(rx)) if rx else "", extra)


def C(x, y, r, c, extra=""):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"%s></circle>' % (f(x), f(y), f(r), c, extra)


def PG(pts, c, extra=""):
    return '<polygon points="%s" fill="%s"%s></polygon>' % (
        " ".join("%s,%s" % (f(x), f(y)) for x, y in pts), c, extra)


def LN(a, b, c, w=2, extra=""):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s></line>' % (
        f(a[0]), f(a[1]), f(b[0]), f(b[1]), c, f(w), extra)


def quad(cam, pts, c, extra=""):
    return PG([cam.p(V(*q)) for q in pts], c, extra)


def zrect(cam, z, x0, y0, x1, y1, c, rx=0):
    a, b = cam.p(V(x0, y1, z)), cam.p(V(x1, y0, z))
    return R(a[0], a[1], b[0] - a[0], b[1] - a[1], c, rx)


def figs(cam, poses, extra=(), shadow_gy=0.0, shadow=True):
    prims = list(extra)
    sh = []
    for po in poses:
        pr = parts(po, legs=not po.get("nolegs")) if "P" in po else parts(solve(po))
        prims += pr
        sh += pr
    o = cast_shadow(sh, cam, shadow_gy) if shadow else ""
    return o + render(prims, cam)


# ================================================================ 01 weight shift
def c_weight_shift():
    cam = Cam(s=68, D=15, hc=4.4, feet_y=706)
    zw = -3.4
    base = cam.gy(zw)
    o = R(0, 0, W, base, "#D8B49C")
    o += zrect(cam, zw, -30, 0, 30, 1.3, "#C8A088")
    o += zrect(cam, zw, 1.55, 0, 5.35, 9.3, "#B98F76")
    o += zrect(cam, zw, 1.8, 0, 5.1, 9.05, "#5F7C7A")
    o += zrect(cam, zw, 2.15, 4.9, 4.75, 8.6, "#7D9B97") + zrect(cam, zw, 2.15, 0.6, 4.75, 4.3, "#7D9B97")
    kn = cam.p(V(2.2, 4.6, zw))
    o += C(kn[0], kn[1], 6, "#D9C48A")
    o += R(0, base, W, H - base, "#CFCAC2") + R(0, base, W, 7, "#B9B3AA")
    for x0 in (-12, -8, -4, 0, 4, 8, 12):
        o += LN(cam.p(V(x0, 0, zw)), cam.p(V(x0, 0, 9)), "#BDB7AE", 2)
    for z in (-0.9, 2.2):
        o += R(0, cam.gy(z), W, 2, "#BDB7AE")
    # plant in a pot, just in front of the wall
    zp, xp = -2.7, -4.6
    k = cam.k(zp)
    b = cam.p(V(xp, 0, zp))
    o += PG([(b[0] - 0.62 * k, b[1] - 1.15 * k), (b[0] + 0.62 * k, b[1] - 1.15 * k),
             (b[0] + 0.45 * k, b[1]), (b[0] - 0.45 * k, b[1])], "#A8684B")
    for dx, dy, r in ((-0.5, 1.9, 0.62), (0.1, 2.5, 0.74), (0.62, 1.85, 0.58), (0.0, 1.5, 0.62)):
        o += C(b[0] + dx * k, b[1] - dy * k, r * k, "#6F9A72")
    pose = dict(x=-0.95, yaw=14, hip=-6, sh=4, turn=-22, tilt=-3,
                rl=(-7, 0, -5, 0), ll=(16, 10, 10, -6), lf=(26, 0), rf=(8, 0),
                ra=("ik", "p", (-0.82, 0.2, 0.12), (-1, 0.1, -0.5)), la=(7, 3, 3, 12))
    return o + figs(cam, [pose])


# ================================================================ 02 mid-stride
def c_walk():
    cam = Cam(s=68, D=15, hc=4.4, feet_y=704)
    hy = cam.hy
    o = R(0, 0, W, H, "#CFE0EA")
    blds = [(-10, 190, 130, "#B9C3CC"), (110, 250, 120, "#A9B5C0"), (222, 150, 116, "#C3CBD2"),
            (330, 280, 140, "#B3BEC8"), (462, 200, 150, "#A9B5C0")]
    for x, hgt, w, c in blds:
        top = hy + 8 - hgt
        o += R(x, top, w, hgt, c)
        for wy in range(int(top) + 22, int(hy) - 20, 40):
            for wx in range(int(x) + 14, int(x + w) - 20, 30):
                o += R(wx, wy, 14, 20, "#DDE6EC")
    o += R(0, hy + 8, W, 16, "#B4AFA6")
    o += R(0, hy + 24, W, H, "#7F8894")
    for x0 in [i * 2.6 - 16.9 for i in range(14)]:
        o += quad(cam, [(x0, 0, -2.3), (x0 + 1.3, 0, -2.3), (x0 + 1.3, 0, 2.7), (x0, 0, 2.7)], "#E8E5DE")
    pose = dict(x=-0.1, yaw=70, bend=4, turn=-10,
                rl=(0, 24, 0, 6), rf=(6, -14), ll=(0, -14, 0, -44), lf=(6, 38),
                la=(4, 26, -4, 54), ra=(4, -22, 2, -4))
    return o + figs(cam, [pose])


# ================================================================ 03 step sit
def c_steps():
    cam = Cam(s=84, D=12, hc=3.6, feet_y=347 + 3.6 * 84)
    rise, tread = 0.75, 1.3

    def zf(n):                     # front edge of step n (step 2 is the seat)
        return 0.5 - (n - 2) * tread

    o = R(0, 0, W, H, "#E6DDD0")
    top_n = 9
    wall_y = cam.gy(zf(top_n + 1), top_n * rise)
    o += R(0, 0, W, wall_y, "#E9E1D5")
    dz = zf(top_n + 1)
    o += zrect(cam, dz, -2.2, top_n * rise, 2.2, top_n * rise + 9.5, "#B7A894")
    o += zrect(cam, dz, -1.85, top_n * rise, 1.85, top_n * rise + 9.1, "#6F7F86")
    for n in range(top_n, 0, -1):
        y0, y1 = cam.gy(zf(n), n * rise), cam.gy(zf(n), (n - 1) * rise)
        if n * rise < cam.hc:
            yt = cam.gy(zf(n + 1), n * rise)
            o += R(0, yt, W, y0 - yt + 1, "#D6CCBD" if n % 2 else "#CFC5B5")
        o += R(0, y0, W, y1 - y0 + 1, "#B5A998")
        o += R(0, y0, W, 3, "#DCD3C5")
    g0 = cam.gy(zf(1), 0)
    o += R(0, g0, W, H - g0, "#C9C3B9")
    pose = dict(x=-0.1, z=0.0, py=1.92, yaw=-28, bend=24, twist=6, turn=22, tilt=-3, nod=-14, sh=-4,
                ll=("ik", "r", (0.52, -1.0, 1.42), (0.25, 1, 0.3)),
                rl=("ik", "r", (-0.55, -1.75, 2.45), (-0.2, 1, 0.3)),
                la=("ik", lambda J: J["kl"] + J["Rr"] @ V(-0.5, -0.9, 0.3), lambda J: J["kl"] + V(0, 0.2, 0) - J["sl"]),
                ra=("ik", "r", (-1.0, -0.26, -0.25), (-0.8, 0.2, -1)))
    return o + figs(cam, [pose], shadow=False)


# ================================================================ 04 warm cup
def c_coffee():
    cam = Cam(s=150, D=9, hc=4.75, feet_y=372 + 4.75 * 150)
    o = R(0, 0, W, H, "#E4D5C3")
    o += R(40, 70, 330, 470, "#8A6F5A") + R(54, 84, 302, 442, "#CFE2E8")
    o += R(54, 300, 302, 226, "#B9D2C0")
    o += C(120, 300, 70, "#9FC2A6") + C(270, 310, 86, "#A9CBAE")
    o += R(199, 84, 12, 442, "#8A6F5A") + R(54, 296, 302, 10, "#8A6F5A")
    o += R(478, 0, 4, 120, "#6B5B50")
    o += PG([(440, 180), (520, 180), (500, 118), (460, 118)], "#C9775A") + C(480, 184, 14, "#F6E3B0")
    o += R(410, 330, 170, 10, "#8A6F5A")
    for x in (428, 468, 508):
        o += R(x, 300, 26, 30, "#F4EEE6", rx=4)
    pose = dict(x=0, py=2.12, yaw=8, bend=6, turn=-10, tilt=6, nod=3, sh=-2,
                ll=(4, 88, 0, 2), rl=(4, 88, 0, 2),
                la=("ik", "c", (0.24, 1.74, 1.02), (0.25, -1, 0.0)),
                ra=("ik", "c", (-0.24, 1.74, 1.02), (-0.25, -1, 0.0)))
    J = solve(pose)
    J["nolegs"] = True
    cz = float((J["hdl"][2] + J["hdr"][2]) / 2)
    cc = cam.p((J["hdl"] + J["hdr"]) / 2 + V(0, 0.02, 0))
    k = cam.k(cz)
    cw, ch = 0.38 * k, 0.50 * k
    cup = ('<rect x="%s" y="%s" width="%s" height="%s" rx="9" fill="#EDE4D8" stroke="%s" stroke-width="3"></rect>'
           % (f(cc[0] - cw / 2), f(cc[1] - ch / 2), f(cw), f(ch), INK))
    cup += ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#FBF7F0" stroke="%s" stroke-width="3"></ellipse>'
            % (f(cc[0]), f(cc[1] - ch / 2 + 2), f(cw / 2), f(cw * 0.13), INK))
    ty = cam.gy(0.42, 3.15)
    table = R(0, ty, W, H - ty, "#B88A63") + R(0, ty, W, 10, "#C99C75")
    extra = [Raw(cz - 0.05, cup), Raw(0.40, table)]
    return o + figs(cam, [J], extra=extra, shadow=False)


# ================================================================ 05 shoreline walk
def c_couple():
    cam = Cam(s=70, D=15, hc=5.5, feet_y=716)
    hy = cam.hy
    o = R(0, 0, W, H, "#CBE3EE")
    o += C(468, 120, 44, "#F8EBC6")
    shore = cam.gy(-17)
    o += R(0, hy, W, (shore - hy) * 0.5, "#7FB3C6") + R(0, hy + (shore - hy) * 0.5, W, (shore - hy) * 0.5 + 30, "#93C2D1")
    o += '<path d="M0 %s Q150 %s 300 %s T600 %s V%s H0Z" fill="#B5D6DF"></path>' % (
        f(shore), f(shore - 16), f(shore + 2), f(shore - 4), f(shore + 60))
    o += '<path d="M0 %s Q160 %s 320 %s T600 %s V800 H0Z" fill="#E9D8B4"></path>' % (
        f(shore + 30), f(shore + 12), f(shore + 28), f(shore + 22))
    o += '<path d="M0 %s Q220 %s 600 %s V800 H0Z" fill="#E2CEA4"></path>' % (f(cam.gy(2.6)), f(cam.gy(1.9)), f(cam.gy(2.8)))
    a = dict(x=-1.25, yaw=10, who="a", turn=30, tilt=4, sh=-2,
             rl=(2, 18, 1, 4), rf=(8, -10), ll=(2, -12, 1, -34), lf=(10, 30),
             la=("ik", "w", (-0.06, 3.75, 0.15), (0.3, 0, -1)), ra=(6, -14, 3, -4))
    b = dict(x=1.25, yaw=-10, who="b", size=0.93, turn=-32, tilt=-4, nod=3, sh=2,
             ll=(2, 18, 1, 4), lf=(8, -10), rl=(2, -12, 1, -34), rf=(10, 30),
             ra=("ik", "w", (0.06, 3.75, 0.15), (-0.3, 0, -1)), la=(6, -14, 3, -4))
    return o + figs(cam, [a, b])


# ================================================================ 06 wall triangle
def on_thigh(sd):
    return lambda J: J["h" + sd] * 0.38 + J["k" + sd] * 0.62 + V(0, 0.4, 0)


def c_group():
    cam = Cam(s=68, D=15, hc=4.6, feet_y=706)
    hy = cam.hy
    o = R(0, 0, W, H, "#D4E6EC")
    for x, y, r, c in ((50, hy - 60, 112, "#8DB58D"), (200, hy - 86, 122, "#7DAA80"), (390, hy - 70, 132, "#8DB58D"),
                       (548, hy - 80, 112, "#7DAA80"), (300, hy - 20, 110, "#9BC09A")):
        o += C(x, y, r, c)
    o += R(0, hy + 14, W, H, "#A9CC9C")
    o += '<path d="M0 %s Q300 %s 600 %s V800 H0Z" fill="#9CC290"></path>' % (f(cam.gy(2.2)), f(cam.gy(1.2)), f(cam.gy(2.4)))
    # low wall: top face then front face, sorted among the figures by depth
    x0, x1, hw, zb, zfr = -5.2, 5.2, 1.7, -0.62, 0.62
    top = quad(cam, [(x0, hw, zb), (x1, hw, zb), (x1, hw, zfr), (x0, hw, zfr)], "#DAD3C7")
    a0, a1 = cam.p(V(x0, hw, zfr)), cam.p(V(x1, 0, zfr))
    front = R(a0[0], a0[1], a1[0] - a0[0], a1[1] - a0[1] + 4, "#C9C1B4")
    for xj in (-2.6, 0, 2.6):
        q0, q1 = cam.p(V(xj, hw, zfr)), cam.p(V(xj, 0, zfr))
        front += R(q0[0], q0[1], 2, q1[1] - q0[1], "#B8AFA1")
    extra = [Raw(-0.7, top), Raw(0.5, front)]
    a = dict(x=-2.85, z=0.05, py=2.12, yaw=24, who="a", sh=-3, turn=12, tilt=3,
             ll=(4, 89, 0, 10), rl=(9, 88, 3, -5),
             ra=("ik", "p", (-1.02, -0.28, -0.05), (-0.6, 0.3, -1)), la=("ik", on_thigh("l")))
    b = mirror(a)
    b.update(who="b", ra=("ik", on_thigh("r")), ll=(9, 88, 3, 6), rl=(4, 89, 0, -4))
    c = dict(x=-0.95, z=-1.5, yaw=8, who="c", sh=-3, tilt=5, turn=6, hip=3,
             ra=("ik", "p", (-0.84, 0.22, 0.1), (-1, 0, -0.5)),
             la=("ik", "w", (1.5, 6.3, -1.8), (0, 0.2, -1)))
    d = dict(x=0.95, z=-1.5, yaw=-8, who="d", size=1.03, sh=3, tilt=-5, turn=-6, hip=-3,
             ra=("ik", "w", (-0.25, 4.3, -2.0), (0, -0.3, -1)), la=(6, 4, 3, 14))
    return o + figs(cam, [a, b, c, d], extra=extra)


SAMPLES = [c_weight_shift, c_walk, c_steps, c_coffee, c_couple, c_group]

GRID = ('<g stroke="#FFFFFF" stroke-width="1.5" opacity="0.7">'
        '<line x1="200" y1="0" x2="200" y2="800"></line><line x1="400" y1="0" x2="400" y2="800"></line>'
        '<line x1="0" y1="266.7" x2="600" y2="266.7"></line><line x1="0" y1="533.3" x2="600" y2="533.3"></line></g>')
