"""Solo pose cards 07-22."""
from .scenes import *


def k07():   # wall lean
    cam = Cam(s=76, D=14, hc=4.4, feet_y=716)
    zw = -0.72
    o = sc_wall(cam, col="#C98F78", zw=zw, dado=None, brick="#B67C66")
    pose = dict(x=0.15, yaw=-10, bend=-8, turn=22, tilt=3,
                rl=(3, 10, 2, 10), ll=(6, 38, 2, -62), lf=(0, 80), la=CROSS_L, ra=CROSS_R)
    return o + figs(cam, [pose], zclip=zw + 0.1)


def k08():   # over the shoulder
    cam = cam_tq()
    pose = dict(x=0.1, yaw=142, twist=-18, turn=-68, tilt=-4, hip=4, sh=-3,
                ll=(-6, 0, -4, 0), rl=(13, 6, 8, -6), la=HIP(1), ra=(6, -4, 3, 6))
    return sc_street(cam, stripes=False) + figs(cam, [pose], shadow=False)


def k09():   # lookout
    cam = Cam(s=44, D=22, hc=4.6, feet_y=648)
    pose = dict(x=-2.3, yaw=168, hip=-5, sh=3, turn=24,
                rl=(-6, 0, -4, 0), ll=(14, 4, 9, -4), la=RELAX, ra=POCKET(-1))
    return sc_view(cam) + figs(cam, [pose])


def k10():   # crossed arms
    cam = cam_waist()
    pose = dict(x=0, yaw=24, twist=-6, turn=-20, tilt=3, la=CROSS_L, ra=CROSS_R)
    return bg_plain("#D9DFE3", "#E7EBEE") + figs(cam, [pose], shadow=False)


def k11():   # doorway lean
    cam = Cam(**FULL)
    pose = dict(x=-0.35, yaw=-6, hip=3, sh=-8, turn=8, tilt=-4,
                ll=(-8, 0, -8, 0), rl=(-11, 10, -10, -4), rf=(10, 48), lf=(14, 0),
                la=POCKET(1), ra=POCKET(-1))
    J = solve(pose)
    xj = float(J["sl"][0]) + 0.3
    xl, lint, zf = xj - 4.6, 9.3, 0.3
    zb = -7.0
    o = R(0, 0, W, H, "#566468")
    o += R(0, 0, W, cam.gy(zb), "#6C7B7E")
    o += R(0, cam.gy(zb), W, H, "#8F8E86")
    o += zrect(cam, zb, -3.5, 0, 1.2, 6.5, "#7F9092")
    o += R(0, cam.gy(zf), W, H, "#CFCAC2")
    wall = zrect(cam, zf, -30, 0, xl, 14, "#E6DCCB") + zrect(cam, zf, xj, 0, 30, 14, "#E6DCCB")
    wall += zrect(cam, zf, xl, lint, xj, 14, "#E6DCCB")
    wall += zrect(cam, zf, xl - 0.3, 0, xl, lint + 0.3, "#FFFFFF") + zrect(cam, zf, xj, 0, xj + 0.3, lint + 0.3, "#FFFFFF")
    wall += zrect(cam, zf, xl - 0.3, lint, xj + 0.3, lint + 0.3, "#FFFFFF")
    wall += zrect(cam, zf, xj + 1.2, 5.6, xj + 2.0, 6.7, "#3F4A4D")
    return o + figs(cam, [J], extra=[Raw(0.05, wall)], zclip=-6.5)


def k12():   # hair touch
    cam = cam_tq()
    pose = dict(x=0, yaw=-18, hip=5, sh=-4, tilt=7, turn=14,
                ll=(-7, 0, -5, 0), rl=(14, 10, 9, -6),
                la=("ik", "c", (0.42, 2.98, -0.2), (1, 0.7, 0.2)), ra=HIP(-1))
    return sc_field(cam) + figs(cam, [pose], shadow=False)


def k13():   # walk in
    cam = Cam(**FULL)
    pose = walk(1, x=0, yaw=4, turn=26, nod=5, la=POCKET(1))
    return sc_path(cam) + figs(cam, [pose])


def k14():   # jump
    cam = Cam(s=62, D=15, hc=4.2, feet_y=720)
    pose = dict(x=0, py=5.5, yaw=-8, bend=-6, nod=-8,
                ll=(22, 35, 10, -75), rl=(26, 20, 12, -85), lf=(10, 50), rf=(10, 50),
                la=(140, 0, 155, -8), ra=(132, 5, 150, 0))
    return sc_beach(cam) + figs(cam, [pose])


def k15():   # open arms
    cam = Cam(s=64, D=15, hc=4.4, feet_y=712)
    pose = dict(x=0, yaw=178, bend=-4, nod=-10, ll=(9, 0, 7, 0), rl=(9, 0, 7, 0),
                la=(128, -4, 142, -8), ra=(128, -4, 142, -8))
    return sc_beach(cam, sunset=True) + figs(cam, [pose])


def k16():   # bench lounge
    cam = Cam(s=70, D=15, hc=4.2, feet_y=708)
    pose = dict(x=-0.5, z=0.05, py=2.12, yaw=10, bend=-12, turn=-14, tilt=2,
                ll=(6, 88, 2, 6),
                rl=("ik", lambda J: J["kl"] + V(0.05, 0.46, 0.1), (-1, 0.2, 0.5)), rf=(-78, 8),
                la=("ik", "r", (2.25, 1.62, -0.78), (0.2, -1, -0.2)),
                ra=("ik", lambda J: (J["kr"] + J["ar"]) / 2 + V(0, 0.38, 0.1)))
    return sc_park(cam) + figs(cam, [pose], extra=bench(cam, -3.3, 3.3))


def shin_mid(J):
    return (J["kl"] + J["al"] + J["kr"] + J["ar"]) / 4


def k17():   # knee hug
    cam = Cam(s=110, D=10, hc=3.0, feet_y=704)
    pose = dict(x=-0.9, py=0.5, yaw=74, bend=20, turn=-42, tilt=-3, nod=-4,
                ll=("ik", "g", (0.32, 0.17, 2.0), (0.1, 1, 0.2)), rl=("ik", "g", (-0.32, 0.17, 1.9), (-0.1, 1, 0.2)),
                la=("ik", lambda J: shin_mid(J) + J["Rr"] @ V(-0.12, 0.0, 0.34), (1, -0.4, 0.1)),
                ra=("ik", lambda J: shin_mid(J) + J["Rr"] @ V(0.12, -0.05, 0.36), (-1, -0.4, 0.1)))
    return sc_beach(cam) + figs(cam, [pose])


def k18():   # stool perch
    cam = Cam(s=74, D=14, hc=4.4, feet_y=704)
    pose = dict(x=0, py=3.32, yaw=-14, bend=14, turn=10, tilt=-3,
                rl=("ik", "g", (-0.55, 0.17, 1.15), (-0.2, 0.3, 1)),
                ll=("ik", "r", (0.45, -2.15, 0.82), (0.4, 0.3, 1)), lf=(12, 12),
                la=("ik", "r", (0.1, -0.3, 0.92), (1, -0.5, 0.2)), ra=("ik", "r", (-0.14, -0.36, 0.9), (-1, -0.5, 0.2)))
    st = box(cam, -0.62, 0.62, 2.72, 2.9, -0.62, 0.62, "#6B7780", "#55616A")
    legs = ""
    for lx, lz in ((-0.55, -0.55), (0.45, -0.55), (-0.55, 0.55), (0.45, 0.55)):
        legs += zrect(cam, lz, lx, 0, lx + 0.1, 2.75, "#3F4A52")
    legs += zrect(cam, 0.55, -0.55, 1.0, 0.55, 1.1, "#3F4A52")
    return sc_studio(cam) + figs(cam, [pose], extra=st + [Raw(-0.7, legs)])


def k19():   # sofa read
    cam = Cam(s=80, D=13, hc=4.0, feet_y=716)
    sofa = []
    c1, c2, c3 = "#8FA7A0", "#7C958E", "#A4B8B2"
    sofa += box(cam, -3.4, 5.6, 0, 3.9, -1.5, -0.9, c3, c2)
    sofa += box(cam, -2.6, 5.6, 0.5, 1.7, -0.9, 0.9, c3, c1)
    sofa += box(cam, -3.4, -2.6, 0, 2.8, -1.5, 0.9, c3, c2, c1)
    pose = dict(x=-1.6, z=0.0, py=2.12, yaw=90, bend=-24, nod=18, turn=-12,
                rl=("ik", "w", (0.6, 1.87, 0.38), (0, 1, 0)), ll=("ik", "w", (1.7, 1.87, -0.3), (0, 1, 0)),
                rf=(0, -62), lf=(0, -62),
                la=("ik", "c", (0.22, 1.42, 1.0), (0.4, -1, 0.1)), ra=("ik", "c", (-0.22, 1.42, 1.0), (-0.4, -1, 0.1)))
    J = solve(pose)
    hc_ = (J["hdl"] + J["hdr"]) / 2
    book = quad(cam, [(hc_[0], hc_[1] - 0.1, 0.4), (hc_[0] + 0.3, hc_[1] + 0.7, 0.4),
                      (hc_[0] + 0.3, hc_[1] + 0.7, -0.4), (hc_[0], hc_[1] - 0.1, -0.4)], "#6F8FA8",
                extra=' stroke="%s" stroke-width="2.5" stroke-linejoin="round"' % INK)
    return sc_home(cam) + figs(cam, [J], extra=sofa + [Raw(float(hc_[2]) - 0.3, book)])


def k20():   # window light
    cam = cam_waist(s=170)
    o = R(0, 0, W, H, "#E7DDCF")
    o += R(330, 40, 250, 640, "#FFFFFF") + R(346, 56, 218, 608, "#D5E7EC")
    o += R(346, 430, 218, 234, "#BCD5C4") + C(420, 440, 60, "#A6C7AD") + C(520, 450, 70, "#AFCDB3")
    o += R(449, 56, 12, 608, "#FFFFFF") + R(346, 350, 218, 10, "#FFFFFF")
    o += R(300, 20, 46, 700, "#D9C7B0") + R(564, 20, 46, 700, "#D9C7B0")
    pose = dict(x=-0.25, yaw=66, turn=-10, nod=5, bend=3,
                la=("ik", "c", (0.2, 1.56, 0.86), (0.4, -1, 0)), ra=("ik", "c", (-0.2, 1.56, 0.86), (-0.4, -1, 0)))
    J = solve(pose)
    return o + figs(cam, [J], extra=[mug(cam, J)], shadow=False)


def k21():   # low crouch
    cam = Cam(s=100, D=11, hc=2.4, feet_y=700)
    zw = -1.6
    o = sc_wall(cam, col="#B9C2B4", zw=zw, dado=None, brick="#A6B0A1", floor="#CFCAC2")
    pose = dict(x=0, py=1.3, yaw=-16, bend=30, nod=-18, turn=10,
                ll=("ik", "g", (0.72, 0.17, 0.5), (0.45, 1, 0.9)), rl=("ik", "g", (-0.72, 0.17, 0.55), (-0.45, 1, 0.9)),
                lf=(30, 0), rf=(30, 0),
                la=("ik", "r", (0.28, 0.72, 1.72), lambda J: J["kl"] - J["sl"]),
                ra=("ik", "r", (-0.22, 0.66, 1.74), lambda J: J["kr"] - J["sr"]))
    return o + figs(cam, [pose], zclip=zw + 0.1)


def k22():   # railing lean
    cam = Cam(**FULL)
    pose = dict(x=-0.5, yaw=90, bend=38, turn=-34, nod=-16,
                ll=(0, -9, 0, -9), rl=(0, 12, 0, -34), rf=(8, 40),
                la=("ik", "w", (2.25, 4.45, -0.12), lambda J: V(1.2, 4.3, -0.5) - J["sl"]),
                ra=("ik", "w", (2.3, 4.42, 0.12), lambda J: V(1.2, 4.3, 0.5) - J["sr"]))
    return sc_water(cam) + figs(cam, [pose])


SOLO = [k07, k08, k09, k10, k11, k12, k13, k14, k15, k16, k17, k18, k19, k20, k21, k22]
