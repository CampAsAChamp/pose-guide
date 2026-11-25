"""Scenes, props and helpers shared by all pose cards."""
from .mannequin import *
from .samples import R, C, PG, LN, quad, zrect, W, H

FULL = dict(s=68, D=15, hc=4.4, feet_y=704)


def cam_tq(top=115, s=122, hc=5.0, D=10, headtop=7.55):
    hy = top + (headtop - hc) * s
    return Cam(s=s, D=D, hc=hc, feet_y=hy + hc * s)


def cam_waist(top=105, s=180, hc=5.6, D=8, headtop=7.55):
    return cam_tq(top, s, hc, D, headtop)


def figs(cam, poses, extra=(), shadow=True, gy=0.0, zclip=None):
    prims, sh = list(extra), []
    for po in poses:
        J = po if "P" in po else solve(po)
        pr = parts(J, legs=not J.get("nolegs"), shins=not J.get("noshins"))
        prims += pr
        sh += pr
    o = cast_shadow(sh, cam, gy, zclip=zclip) if shadow else ""
    return o + render(prims, cam)


# ---------------------------------------------------------------- pose snippets
def HIP(sg):
    return ("ik", "p", (sg * 0.84, 0.2, 0.12), (sg * 1, 0.1, -0.5))


def POCKET(sg):
    return ("ik", "p", (sg * 0.80, -0.12, 0.22), (sg * 0.9, 0, -0.9))


CROSS_L = ("ik", "c", (-0.50, 1.30, 0.52), (0.9, -0.8, 0.3))
CROSS_R = ("ik", "c", (0.44, 1.42, 0.60), (-0.9, -0.8, 0.3))
RELAX = (6, 3, 2, 10)


def walk(phase=1, **kw):
    fw_leg, fw_foot = (2, 20, 1, 5), (8, -12)
    bk_leg, bk_foot = (2, -12, 1, -38), (10, 32)
    fw_arm, bk_arm = (5, 18, 2, 32), (5, -16, 2, -4)
    if phase == 1:
        p = dict(rl=fw_leg, rf=fw_foot, ll=bk_leg, lf=bk_foot, la=fw_arm, ra=bk_arm)
    else:
        p = dict(ll=fw_leg, lf=fw_foot, rl=bk_leg, rf=bk_foot, ra=fw_arm, la=bk_arm)
    p.update(kw)
    return p


def sit(seat=1.7, size=1.0, **kw):
    p = dict(py=(seat + 0.42 * size) / size, size=size, ll=(5, 89, 1, 8), rl=(5, 89, 1, 2))
    p.update(kw)
    return p


def mug(cam, J, dy=0.02, col="#EDE4D8"):
    cz = float((J["hdl"][2] + J["hdr"][2]) / 2)
    cc = cam.p((J["hdl"] + J["hdr"]) / 2 + V(0, dy, 0))
    k = cam.k(cz)
    cw, ch = 0.38 * k, 0.50 * k
    cup = ('<rect x="%s" y="%s" width="%s" height="%s" rx="9" fill="%s" stroke="%s" stroke-width="3"></rect>'
           % (f(cc[0] - cw / 2), f(cc[1] - ch / 2), f(cw), f(ch), col, INK))
    cup += ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#FBF7F0" stroke="%s" stroke-width="3"></ellipse>'
            % (f(cc[0]), f(cc[1] - ch / 2 + 2), f(cw / 2), f(cw * 0.13), INK))
    return Raw(cz - 0.05, cup)


# ---------------------------------------------------------------- props
def box(cam, x0, x1, y0, y1, z0, z1, top, front, side=None):
    out = []
    side = side or front
    if y1 < cam.hc:
        out.append(Raw(z0 - 0.01, quad(cam, [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top)))
    if x0 > 0.05:
        out.append(Raw((z0 + z1) / 2, quad(cam, [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], side)))
    if x1 < -0.05:
        out.append(Raw((z0 + z1) / 2, quad(cam, [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], side)))
    out.append(Raw(z1 - 0.02, zrect(cam, z1, x0, y0, x1, y1, front)))
    return out


def bench(cam, x0, x1, zc=0.0, seat=1.7, d=0.78, back=1, wood="#A9825F", dark="#8C6A4C", topc="#B8926E"):
    out = []
    zb, zn = zc - d, zc + d
    legs = "".join(zrect(cam, zn, lx, 0, lx + 0.22, seat - 0.2, dark) for lx in (x0 + 0.25, x1 - 0.47))
    out.append(Raw(zb - 0.3, legs + quad(cam, [(x0, seat, zb), (x1, seat, zb), (x1, seat, zn), (x0, seat, zn)], topc)))
    out.append(Raw(zn - 0.02, zrect(cam, zn, x0, seat - 0.24, x1, seat, wood)))
    if back:
        zr = zb - 0.08 if back > 0 else zn + 0.1
        s = "".join(zrect(cam, zr, lx, 0 if back < 0 else seat - 0.2, lx + 0.22, seat + 2.05, dark)
                    for lx in (x0 + 0.25, x1 - 0.47))
        for i in range(3):
            s += zrect(cam, zr, x0, seat + 0.35 + i * 0.62, x1, seat + 0.77 + i * 0.62, wood, rx=4)
        out.append(Raw(zr - 0.05 if back > 0 else zr, s))
    return out


# ---------------------------------------------------------------- scenes
def ground_lines(cam, z_far, col, xs=(-12, -8, -4, 0, 4, 8, 12), zs=(-0.9, 2.2)):
    o = ""
    for x0 in xs:
        o += LN(cam.p(V(x0, 0, z_far)), cam.p(V(x0, 0, 9)), col, 2)
    for z in zs:
        if z > z_far:
            o += R(0, cam.gy(z), W, 2, col)
    return o


def sc_wall(cam, col="#D8B49C", zw=-3.4, dado="#C8A088", floor="#CFCAC2", line="#BDB7AE", brick=None,
            door=None, plant=None):
    base = cam.gy(zw)
    k = cam.k(zw)
    o = R(0, 0, W, base + 1, col)
    if brick:
        bh, bw = 0.36 * k, 1.25 * k
        d, y, i = "", base - bh, 0
        while y > -bh:
            d += "M0 %sH600" % f(y)
            x = (cam.cx + (i % 2) * bw / 2) % bw - bw
            while x < W:
                d += "M%s %sv%s" % (f(x), f(y), f(bh))
                x += bw
            y -= bh
            i += 1
        o += '<path d="%s" fill="none" stroke="%s" stroke-width="1.5"></path>' % (d, brick)
    if dado:
        o += zrect(cam, zw, -40, 0, 40, 1.3, dado)
    if door is not None:
        o += zrect(cam, zw, door, 0, door + 3.8, 9.3, "#B98F76")
        o += zrect(cam, zw, door + 0.25, 0, door + 3.55, 9.05, "#5F7C7A")
        o += zrect(cam, zw, door + 0.6, 4.9, door + 3.2, 8.6, "#7D9B97") + zrect(cam, zw, door + 0.6, 0.6, door + 3.2, 4.3, "#7D9B97")
        kn = cam.p(V(door + 0.65, 4.6, zw))
        o += C(kn[0], kn[1], 6, "#D9C48A")
    o += R(0, base, W, H - base, floor) + R(0, base, W, 7, line)
    o += ground_lines(cam, zw, line)
    if plant is not None:
        zp = zw + 0.7
        kp = cam.k(zp)
        b = cam.p(V(plant, 0, zp))
        o += PG([(b[0] - 0.62 * kp, b[1] - 1.15 * kp), (b[0] + 0.62 * kp, b[1] - 1.15 * kp),
                 (b[0] + 0.45 * kp, b[1]), (b[0] - 0.45 * kp, b[1])], "#A8684B")
        for dx, dy, r in ((-0.5, 1.9, 0.62), (0.1, 2.5, 0.74), (0.62, 1.85, 0.58), (0.0, 1.5, 0.62)):
            o += C(b[0] + dx * kp, b[1] - dy * kp, r * kp, "#6F9A72")
    return o


def sc_street(cam, stripes=True):
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
    if stripes:
        for x0 in [i * 2.6 - 16.9 for i in range(14)]:
            o += quad(cam, [(x0, 0, -2.3), (x0 + 1.3, 0, -2.3), (x0 + 1.3, 0, 2.7), (x0, 0, 2.7)], "#E8E5DE")
    return o


def sc_beach(cam, sunset=False):
    hy = cam.hy
    sky, sea1, sea2, foam, sand1, sand2, sun = ("#CBE3EE", "#7FB3C6", "#93C2D1", "#B5D6DF", "#E9D8B4", "#E2CEA4", "#F8EBC6")
    if sunset:
        sky, sea1, sea2, foam, sand1, sand2, sun = ("#F6D8BC", "#8FA5B5", "#A5B7C1", "#D9D3CF", "#E6D0AE", "#DCC49E", "#FFF3D9")
    o = R(0, 0, W, H, sky)
    o += C(300, hy - 34, 78, sun) if sunset else C(468, max(90, hy - 220), 44, sun)
    shore = cam.gy(-17)
    o += R(0, hy, W, (shore - hy) * 0.5, sea1) + R(0, hy + (shore - hy) * 0.5, W, (shore - hy) * 0.5 + 30, sea2)
    o += '<path d="M0 %s Q150 %s 300 %s T600 %s V%s H0Z" fill="%s"></path>' % (
        f(shore), f(shore - 16), f(shore + 2), f(shore - 4), f(shore + 60), foam)
    o += '<path d="M0 %s Q160 %s 320 %s T600 %s V800 H0Z" fill="%s"></path>' % (
        f(shore + 30), f(shore + 12), f(shore + 28), f(shore + 22), sand1)
    o += '<path d="M0 %s Q220 %s 600 %s V800 H0Z" fill="%s"></path>' % (f(cam.gy(2.6)), f(cam.gy(1.9)), f(cam.gy(2.8)), sand2)
    return o


def sc_park(cam):
    hy = cam.hy
    o = R(0, 0, W, H, "#D4E6EC")
    for x, y, r, c in ((50, hy - 60, 112, "#8DB58D"), (200, hy - 86, 122, "#7DAA80"), (390, hy - 70, 132, "#8DB58D"),
                       (548, hy - 80, 112, "#7DAA80"), (300, hy - 20, 110, "#9BC09A")):
        o += C(x, y, r, c)
    o += R(0, hy + 14, W, H, "#A9CC9C")
    o += '<path d="M0 %s Q300 %s 600 %s V800 H0Z" fill="#9CC290"></path>' % (f(cam.gy(2.2)), f(cam.gy(1.2)), f(cam.gy(2.4)))
    return o


def sc_view(cam):
    hy = cam.hy
    o = R(0, 0, W, H, "#D6E6EE")
    o += C(455, max(70, hy - 300), 40, "#F8EBC6")
    o += PG([(0, hy - 60), (70, hy - 150), (150, hy - 95), (250, hy - 215), (340, hy - 120), (420, hy - 175),
             (520, hy - 80), (600, hy - 130), (600, hy + 60), (0, hy + 60)], "#BCCDD8")
    o += PG([(0, hy - 20), (90, hy - 85), (190, hy - 40), (300, hy - 120), (410, hy - 50), (500, hy - 100),
             (600, hy - 45), (600, hy + 80), (0, hy + 80)], "#9FB6C3")
    o += PG([(0, hy + 20), (120, hy - 30), (260, hy + 15), (380, hy - 25), (520, hy + 18), (600, hy - 5),
             (600, hy + 120), (0, hy + 120)], "#8FAB96")
    o += R(0, hy + 60, W, H, "#A9C3A6")
    e = cam.gy(-4.5)
    o += '<path d="M0 %s Q150 %s 300 %s T600 %s V800 H0Z" fill="#9DBB8C"></path>' % (f(e + 6), f(e - 12), f(e), f(e + 8))
    o += '<path d="M0 %s Q150 %s 300 %s T600 %s V800 H0Z" fill="#C9BA9F"></path>' % (f(e + 24), f(e + 8), f(e + 20), f(e + 26))
    return o


def sc_field(cam):
    hy = cam.hy
    o = R(0, 0, W, H, "#F8E4C4")
    o += C(438, hy - 52, 50, "#FFF4D8")
    for x, r in ((30, 46), (110, 60), (205, 44), (300, 54), (395, 40), (480, 58), (575, 48)):
        o += C(x, hy + 4, r * 0.62, "#B3AD74")
    o += R(0, hy + 4, W, H, "#E6CC86")
    o += R(0, cam.gy(-6), W, H, "#DFC277")
    o += '<path d="M0 %s Q300 %s 600 %s V800 H0Z" fill="#D6B768"></path>' % (f(cam.gy(1.8)), f(cam.gy(0.9)), f(cam.gy(2.0)))
    d = ""
    for i in range(26):
        x = 12 + i * 23.5
        y0 = hy + 30 + (i * 37 % 60)
        d += "M%s %sl4 -22l4 22Z" % (f(x), f(y0))
    o += '<path d="%s" fill="#C9A955"></path>' % d
    return o


def sc_path(cam):
    hy = cam.hy
    o = R(0, 0, W, H, "#D4E6EC")
    for x, y, r, c in ((40, hy - 120, 150, "#86B088"), (210, hy - 150, 130, "#7AA67E"), (400, hy - 150, 135, "#86B088"),
                       (570, hy - 120, 150, "#7AA67E"), (300, hy - 40, 90, "#9BC09A")):
        o += C(x, y, r, c)
    o += R(0, hy + 6, W, H, "#A9CC9C")
    o += quad(cam, [(-1.6, 0, -60), (1.6, 0, -60), (2.4, 0, 9), (-2.4, 0, 9)], "#DDD2BE")
    for i, z in enumerate((-30, -21, -14, -8.5, -4, -0.6)):
        for sx in (-1, 1):
            k = cam.k(z)
            b = cam.p(V(sx * 3.7, 0, z))
            o += R(b[0] - 0.28 * k, b[1] - 7.2 * k, 0.56 * k, 7.2 * k, "#8A6F5A" if z > -9 else "#9A8370")
            o += C(b[0] + sx * 0.6 * k, b[1] - 8.6 * k, 3.0 * k, ("#7AA67E", "#86B088")[(i + (sx > 0)) % 2])
    return o


def sc_home(cam, zw=-3.0, wall="#E9E0D2"):
    base = cam.gy(zw)
    o = R(0, 0, W, base + 1, wall)
    o += zrect(cam, zw, -6.2, 3.6, -1.8, 9.4, "#FFFFFF") + zrect(cam, zw, -5.95, 3.85, -2.05, 9.15, "#CFE2E8")
    o += zrect(cam, zw, -4.08, 3.85, -3.92, 9.15, "#FFFFFF") + zrect(cam, zw, -5.95, 6.42, -2.05, 6.58, "#FFFFFF")
    o += zrect(cam, zw, 1.6, 5.6, 3.3, 7.9, "#B88A63") + zrect(cam, zw, 1.78, 5.78, 3.12, 7.72, "#DDE6D8")
    o += zrect(cam, zw, 3.9, 6.2, 5.0, 7.6, "#8A6F5A") + zrect(cam, zw, 4.05, 6.35, 4.85, 7.45, "#F1DDC8")
    o += zrect(cam, zw, -40, 0, 40, 0.5, "#FFFFFF")
    o += R(0, base, W, H - base, "#CDAE88")
    for x0 in (-14, -10.5, -7, -3.5, 0, 3.5, 7, 10.5, 14):
        o += LN(cam.p(V(x0, 0, zw)), cam.p(V(x0, 0, 9)), "#BF9E78", 2)
    return o


def sc_studio(cam, col="#DCE2E6", floor="#CBD2D6", zw=-4.0):
    base = cam.gy(zw)
    return R(0, 0, W, H, col) + R(0, base, W, H - base, floor) + R(0, base - 10, W, 20, "#D4DADE")


def bg_plain(col="#DCE2E6", spot="#E8ECEF"):
    return R(0, 0, W, H, col) + C(300, 380, 270, spot)


def bg_cafe():
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
    return o


def sc_water(cam, rx=1.25, rh=4.2):
    hy = cam.hy
    o = R(0, 0, W, H, "#D3E4EC")
    for x, w, hgt in ((330, 40, 46), (376, 30, 70), (412, 52, 38), (470, 34, 84), (510, 60, 52), (575, 40, 66)):
        o += R(x, hy - hgt, w, hgt + 2, "#B5C4CE")
    o += R(0, hy, W, H, "#8DB6C8")
    for i, yy in enumerate((hy + 26, hy + 70, hy + 130, hy + 210, hy + 310)):
        o += R(300 + (i % 2) * 60, yy, 220 - i * 10, 3, "#A7C8D6")
    far, near = cam.p(V(rx + 0.25, 0, -80)), cam.p(V(rx + 0.25, 0, 9.5))
    o += PG([(0, far[1]), (far[0], far[1]), (near[0], near[1]), (0, near[1])], "#CFC8BC")
    for xx in (-9, -6, -3, 0):
        o += LN(cam.p(V(xx, 0, -80)), cam.p(V(xx, 0, 9.5)), "#BDB5A8", 2)
    col = "#66737C"
    for z in (-22, -16, -11.5, -8, -5, -2.4, 0.2, 2.6, 5):
        k = cam.k(z)
        b, t = cam.p(V(rx, 0, z)), cam.p(V(rx, rh, z))
        o += R(b[0] - 0.08 * k, t[1], 0.16 * k, b[1] - t[1], col)
    for y0, th in ((rh, 0.13), (rh * 0.52, 0.07)):
        o += quad(cam, [(rx, y0 + th, -60), (rx, y0 + th, 8), (rx, y0 - th, 8), (rx, y0 - th, -60)], col)
    return o


def sc_stairs(cam, top_n=9):
    rise, tread = 0.75, 1.3
    zf = lambda n: 0.5 - (n - 2) * tread
    o = R(0, 0, W, H, "#E6DDD0")
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
    return o, zf, rise


def stair_sitter(zf, rise, x, n, who, size=1.0, **kw):
    pz = zf(n) - 0.5
    fy, fz = (n - 1) * rise + 0.17, zf(n - 1) - 0.42
    p = dict(x=x, z=pz, py=(n * rise + 0.42 * size) / size, size=size, who=who, bend=16,
             ll=("ik", "w", (x + 0.45, fy, fz), (0.3, 1, 0.3)), rl=("ik", "w", (x - 0.45, fy, fz + 0.05), (-0.3, 1, 0.3)),
             la=("ik", lambda J: J["kl"] + V(-0.25, 0.3, 0.2), (1, -0.6, 0.2)),
             ra=("ik", lambda J: J["kr"] + V(0.25, 0.3, 0.2), (-1, -0.6, 0.2)))
    p.update(kw)
    return p


def sc_water_x(cam, zr=-0.6, rh=4.2):
    hy = cam.hy
    o = R(0, 0, W, H, "#D3E4EC")
    for x, w, hgt in ((20, 50, 40), (80, 34, 66), (130, 60, 34), (330, 40, 46), (376, 30, 70), (412, 52, 38),
                      (470, 34, 84), (510, 60, 52), (575, 40, 66)):
        o += R(x, hy - hgt, w, hgt + 2, "#B5C4CE")
    o += R(0, hy, W, H, "#8DB6C8")
    for i, yy in enumerate((hy + 22, hy + 60, hy + 110, hy + 170)):
        o += R(40 + (i % 2) * 260, yy, 240 - i * 20, 3, "#A7C8D6")
    edge = cam.gy(zr - 0.35)
    o += R(0, edge, W, H - edge, "#CFC8BC") + R(0, edge, W, 6, "#B9B1A4")
    o += ground_lines(cam, zr - 0.35, "#BDB5A8")
    col = "#66737C"
    x = -11.0
    while x < 11.5:
        o += zrect(cam, zr, x - 0.07, 0, x + 0.07, rh, col)
        x += 2.2
    o += zrect(cam, zr, -30, rh - 0.12, 30, rh + 0.12, col) + zrect(cam, zr, -30, rh * 0.5 - 0.07, 30, rh * 0.5 + 0.07, col)
    return o


def sc_pier(cam, zend=-1.2, hw=2.6):
    hy = cam.hy
    o = R(0, 0, W, H, "#D6E6EE") + C(140, max(70, hy - 250), 40, "#F8EBC6")
    o += PG([(0, hy - 22), (110, hy - 46), (240, hy - 26), (380, hy - 52), (520, hy - 30), (600, hy - 40),
             (600, hy + 2), (0, hy + 2)], "#9DB4A6")
    o += R(0, hy, W, H, "#8DB6C8")
    for i, yy in enumerate((hy + 22, hy + 60, hy + 110, hy + 170, hy + 250)):
        o += R(30 + (i % 2) * 300, yy, 230 - i * 14, 3, "#A7C8D6")
    for sx in (-1, 1):
        o += zrect(cam, zend, sx * hw - 0.16, -1.6, sx * hw + 0.16, 0.9, "#8C6A4C")
    o += quad(cam, [(-hw, 0, zend), (hw, 0, zend), (hw, 0, 9.5), (-hw, 0, 9.5)], "#C4A27C")
    z = zend
    while z < 9:
        o += LN(cam.p(V(-hw, 0, z)), cam.p(V(hw, 0, z)), "#B08D66", 2)
        z += 0.7
    return o


def bg_window():
    o = R(0, 0, W, H, "#E7DDCF")
    o += R(330, 40, 250, 640, "#FFFFFF") + R(346, 56, 218, 608, "#D5E7EC")
    o += R(346, 430, 218, 234, "#BCD5C4") + C(420, 440, 60, "#A6C7AD") + C(520, 450, 70, "#AFCDB3")
    o += R(449, 56, 12, 608, "#FFFFFF") + R(346, 350, 218, 10, "#FFFFFF")
    o += R(300, 20, 46, 700, "#D9C7B0") + R(564, 20, 46, 700, "#D9C7B0")
    return o


def cafe_side(cam):
    o = R(0, 0, W, H, "#E4D5C3")
    o += R(60, 60, 480, 330, "#8A6F5A") + R(74, 74, 452, 302, "#CFE2E8") + R(74, 250, 452, 126, "#B9D2C0")
    o += C(170, 250, 60, "#9FC2A6") + C(400, 256, 74, "#A9CBAE")
    o += R(294, 74, 12, 302, "#8A6F5A")
    for lx in (150, 450):
        o += R(lx - 2, 0, 4, 60, "#6B5B50")
    o += R(0, cam.gy(-2.5), W, H, "#C9A77E")
    return o


def cafe_table(cam, hw=0.95, hd=0.9):
    extra = box(cam, -hw, hw, 3.0, 3.15, -hd, hd, "#C99C75", "#A57750")
    extra.append(Raw(-hd - 0.05, zrect(cam, 0, -0.12, 0, 0.12, 3.0, "#6B5B50")))
    return extra


def cafe_chair(cam, sx):
    x0, x1 = sorted((sx * 2.75, sx * 2.6))
    out = box(cam, x0, x1, 1.6, 4.3, -0.6, 0.6, "#7A8C8A", "#66787A")
    x0, x1 = sorted((sx * 2.7, sx * 1.35))
    return out + box(cam, x0, x1, 1.5, 1.7, -0.6, 0.6, "#8B9C9A", "#7A8C8A")


def small_cup(cam, pt, z=None):
    c = cam.p(pt)
    k = cam.k(pt[2])
    svg = ('<rect x="%s" y="%s" width="%s" height="%s" rx="5" fill="#EDE4D8" stroke="%s" stroke-width="2.5"></rect>'
           % (f(c[0] - 0.19 * k), f(c[1] - 0.44 * k), f(0.38 * k), f(0.44 * k), INK))
    return Raw(float(pt[2]) if z is None else z, svg)
