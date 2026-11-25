"""Everything a card module needs: `from .helpers import *` brings in the camera, scenes, props,
the @card decorator and the shared leg, arm and whole-pose snippets below."""
from .scenes import *
from .samples import on_thigh
from .registry import card, TAGS  # noqa: F401  (re-exported for card modules)


def P(*frags, **kw):
    d = {}
    for fr in frags:
        d.update(fr)
    d.update(kw)
    return d


LS_R = dict(hip=-5, rl=(-7, 0, -5, 0), ll=(14, 10, 9, -6), lf=(24, 0))
LS_L = dict(hip=5, ll=(-7, 0, -5, 0), rl=(14, 10, 9, -6), rf=(24, 0))
LX = dict(hip=4, ll=(-6, 0, -4, 0), rl=(-9, 9, -8, -3), rf=(10, 46))
LW = dict(ll=(11, 0, 9, 0), rl=(11, 0, 9, 0))
LSTEP = dict(rl=(2, 14, 1, 4), ll=(2, -8, 1, -10))
LTOE = dict(ll=(-4, 0, -3, 0), rl=(0, 10, 0, -30), rf=(8, 40))

WIDE = dict(s=44, D=22, hc=4.6, feet_y=648)
LOW = dict(s=82, D=12, hc=1.5, feet_y=744)


def cam_close(top=140):
    return cam_tq(top=top, s=300, hc=6.6, D=6)


def BACKH(sg):
    return ("ik", "p", (sg * 0.18, 0.12, -0.52), (sg * 1, -0.3, -0.6))


def CLASP(sg):
    return ("ik", "c", (-sg * 0.06, 0.52, 0.54), (sg * 1, -0.6, 0.1))


def HAIR(sg):
    return ("ik", "c", (sg * 0.42, 2.98, -0.2), (sg * 1, 0.7, 0.2))


WAVE = (35, 5, 150, 12)
UPV = (140, 0, 155, -8)
OUTW = (86, 0, 90, 6)


def SHADE(sg):
    return ("ik", lambda J: J["head"] + J["Rh"] @ V(sg * 0.2, 0.3, 0.42), (sg * 1, 0.2, 0.4))


def PHONE(sg):
    return ("ik", "c", (sg * 0.22, 1.62, 0.78), (sg * 0.6, -1, 0))


def CHIN(sg):
    return ("ik", lambda J: J["head"] + J["Rh"] @ V(sg * 0.08, -0.62, 0.36), (sg * 0.5, -1, 0.2))


def NECK(sg):
    return ("ik", "c", (sg * 0.3, 2.6, -0.38), (sg * 1, 0.3, 0.3))


def THUMB(sg):
    return ("ik", "p", (sg * 0.5, 0.12, 0.44), (sg * 1, -0.1, -0.4))


def ONHEAD(sg):
    return ("ik", lambda J: J["head"] + J["Rh"] @ V(sg * 0.1, 0.55, 0.0), (sg * 1, 0.5, 0.3))


def EAR(sg):
    return ("ik", lambda J: J["head"] + J["Rh"] @ V(sg * 0.46, -0.05, 0.05), (sg * 1, -0.6, 0.3))


def BPOCKET(sg):
    return ("ik", "p", (sg * 0.42, -0.1, -0.5), (sg * 1, 0.2, -0.6))


def phone(cam, J, sd="r"):
    c = cam.p(J["hd" + sd] + V(0, 0.12, 0.02))
    k = cam.k(J["hd" + sd][2])
    svg = ('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="#3F4A52" stroke="%s" stroke-width="2"></rect>'
           % (f(c[0] - 0.13 * k), f(c[1] - 0.28 * k), f(0.26 * k), f(0.5 * k), INK))
    return Raw(float(J["hd" + sd][2]) - 0.02, svg)


def sidewall(cam, x, col="#C9B8A6", line="#B8A795"):
    o = quad(cam, [(x, 0, -40), (x, 16, -40), (x, 16, 9.5), (x, 0, 9.5)], col)
    for y in range(1, 15):
        o += LN(cam.p(V(x, y, -40)), cam.p(V(x, y, 9.5)), line, 1.5)
    return o


def rail_x(cam, zr, rh=4.2, col="#66737C", step=2.2):
    o, x = "", -11.0
    while x < 11.5:
        o += zrect(cam, zr, x - 0.07, 0, x + 0.07, rh, col)
        x += step
    return o + zrect(cam, zr, -30, rh - 0.12, 30, rh + 0.12, col) + zrect(cam, zr, -30, rh * 0.5 - 0.07, 30, rh * 0.5 + 0.07, col)


def lowwall(cam, x0=-5.2, x1=5.2, h=1.7, zb=-0.62, zn=0.62, top="#DAD3C7", front="#C9C1B4"):
    t = quad(cam, [(x0, h, zb), (x1, h, zb), (x1, h, zn), (x0, h, zn)], top)
    a0, a1 = cam.p(V(x0, h, zn)), cam.p(V(x1, 0, zn))
    fr = R(a0[0], a0[1], a1[0] - a0[0], a1[1] - a0[1] + 4, front)
    return [Raw(zb - 0.08, t), Raw(zn - 0.12, fr)]


def chair_front(cam, x=0.0, zc=0.0, seat=1.9, back="rear", col="#6B7780", dark="#55616A"):
    out = box(cam, x - 0.8, x + 0.8, seat - 0.18, seat, zc - 0.7, zc + 0.7, col, dark)
    legs = "".join(zrect(cam, zc + lz, x + lx, 0, x + lx + 0.12, seat - 0.15, "#3F4A52")
                   for lx, lz in ((-0.75, -0.6), (0.63, -0.6), (-0.75, 0.6), (0.63, 0.6)))
    out.append(Raw(zc - 0.9, legs))
    zb = zc - 0.72 if back == "rear" else zc + 0.62
    bk = zrect(cam, zb, x - 0.8, seat + 1.2, x + 0.8, seat + 2.5, dark, rx=6)
    bk += zrect(cam, zb, x - 0.78, seat, x - 0.66, seat + 1.3, "#3F4A52") + zrect(cam, zb, x + 0.66, seat, x + 0.78, seat + 1.3, "#3F4A52")
    out.append(Raw(zb - 0.05 if back == "rear" else zb, bk))
    return out


def chair_side(cam, x=0.0, sg=1, seat=1.9, col="#6B7780", dark="#55616A"):
    """Chair seen from the side; sg=+1 means the sitter faces +X (back rest on the -X side)."""
    out = box(cam, x - 0.8, x + 0.8, seat - 0.18, seat, -0.7, 0.7, col, dark)
    xb = x - sg * 0.82
    x0, x1 = sorted((xb, xb - sg * 0.14))
    out += box(cam, x0, x1, seat, seat + 2.5, -0.7, 0.7, col, dark, "#606C75")
    legs = "".join(zrect(cam, 0.68, lx, 0, lx + 0.12, seat - 0.15, "#3F4A52") for lx in (x - 0.78, x + 0.66))
    out.append(Raw(-0.9, legs))
    return out


def trunk(cam, x0, x1, z0=-0.5, z1=0.5):
    return box(cam, x0, x1, 0, 16, z0, z1, "#8A6F5A", "#8A6F5A", "#7A604C")


# ---------------------------------------------------------------- shared pose snippets
def shin_mid(J):
    return (J["kl"] + J["al"] + J["kr"] + J["ar"]) / 4


def kneel(**kw):
    p = dict(py=2.33, ll=(2, 0, 0, -86), lf=(180, 8), rl=(8, 86, 3, 0),
             ra=("ik", lambda J: J["kr"] + V(0.0, 0.34, 0.1)), la=HIP(1))
    p.update(kw)
    return p


def sofa_front(cam, x0=-4.3, x1=4.3):
    c1, c2, c3 = "#8FA7A0", "#7C958E", "#A4B8B2"
    s = box(cam, x0, x1, 0, 3.9, -1.5, -0.9, c3, c2)
    s += box(cam, x0 + 0.8, x1 - 0.8, 0.5, 1.7, -0.9, 0.9, c3, c1)
    s += box(cam, x0, x0 + 0.8, 0, 2.8, -1.5, 0.9, c3, c2, c1)
    s += box(cam, x1 - 0.8, x1, 0, 2.8, -1.5, 0.9, c3, c2, c1)
    return s


def hug_knees(J, dx):
    return shin_mid(J) + J["Rr"] @ V(dx, 0.0, 0.34)


def floor_knees(**kw):
    p = dict(py=0.5, bend=18, ll=("ik", "g", (0.3, 0.17, 1.75), (0.1, 1, 0.2)), rl=("ik", "g", (-0.3, 0.17, 1.7), (-0.1, 1, 0.2)),
             la=("ik", lambda J: hug_knees(J, -0.12), (1, -0.4, 0.1)), ra=("ik", lambda J: hug_knees(J, 0.12), (-1, -0.4, 0.1)))
    p.update(kw)
    return p


def prone(**kw):
    p = dict(z=-2.3, py=0.5, bend=70, nod=-62, ll=(8, -90, 6, -150), rl=(8, -90, 8, -128), lf=(0, 0), rf=(0, 0),
             la=("ik", "g", (0.35, 0.16, 2.75), (0.9, -0.6, 0.3)), ra=("ik", "g", (-0.2, 0.16, 2.8), (-0.9, -0.6, 0.3)))
    p.update(kw)
    return p


def run(phase=1, **kw):
    f_leg, f_foot, b_leg, b_foot = (3, 62, 2, -25), (8, 20), (3, -18, 2, -85), (8, 55)
    f_arm, b_arm = (8, 35, -8, 125), (8, -40, 0, 40)
    p = dict(py=4.3, bend=10, nod=-6)
    p.update(dict(rl=f_leg, rf=f_foot, ll=b_leg, lf=b_foot, la=f_arm, ra=b_arm) if phase == 1 else
             dict(ll=f_leg, lf=f_foot, rl=b_leg, rf=b_foot, ra=f_arm, la=b_arm))
    p.update(kw)
    return p
