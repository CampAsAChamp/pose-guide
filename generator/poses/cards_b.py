"""Solo pose cards 07-22."""
from .helpers import *


@card(7, "Wall lean", "S Le F Str f",
      "Shoulders and hips against the wall, one foot flat on it behind you. Fold the arms loosely, chin off to one side.",
      "Stand square to the wall so its lines stay level. Leave space on the side the face is turned toward.",
      alt="Mannequin leaning back against a brick wall with arms folded and one foot up on the wall.")
def k07():   # wall lean
    cam = Cam(s=76, D=14, hc=4.4, feet_y=716)
    zw = -0.72
    o = sc_wall(cam, col="#C98F78", zw=zw, dado=None, brick="#B67C66")
    pose = dict(x=0.15, yaw=-10, bend=-8, turn=22, tilt=3,
                rl=(3, 10, 2, 10), ll=(6, 38, 2, -62), lf=(0, 80), la=CROSS_L, ra=CROSS_R)
    return o + figs(cam, [pose], zclip=zw + 0.1)


@card(8, "Over the shoulder", "S St T Str b",
      "Turn your back three-quarters to the camera, hand on the far hip, then look back over the near shoulder.",
      "Crop at mid-thigh, never at the knee. Focus on the eye nearest the lens.",
      alt="Mannequin seen from behind on a street, cropped at the thigh, looking back over one shoulder.")
def k08():   # over the shoulder
    cam = cam_tq()
    pose = dict(x=0.1, yaw=142, twist=-18, turn=-68, tilt=-4, hip=4, sh=-3,
                ll=(-6, 0, -4, 0), rl=(13, 6, 8, -6), la=HIP(1), ra=(6, -4, 3, 6))
    return sc_street(cam, stripes=False) + figs(cam, [pose], shadow=False)


@card(9, "The lookout", "S St W Vie b",
      "Back to the camera, weight on one leg, a hand in a pocket. Turn the head a little so the profile shows.",
      "Go wide and keep the person small on a third line, with the view filling the rest of the frame.",
      alt="Small mannequin seen from behind on the left third, looking out over layered mountains.")
def k09():   # lookout
    cam = Cam(s=44, D=22, hc=4.6, feet_y=648)
    pose = dict(x=-2.3, yaw=168, hip=-5, sh=3, turn=24,
                rl=(-6, 0, -4, 0), ll=(14, 4, 9, -4), la=RELAX, ra=POCKET(-1))
    return sc_view(cam) + figs(cam, [pose])


@card(10, "Crossed arms", "S St U Stu f",
      "Angle the body about 30 degrees away, fold the arms loosely and bring the face back to the lens.",
      "Crop just below the folded arms. Camera at eye level, eyes near the upper third line.",
      alt="Waist-up mannequin angled slightly away with arms folded, against a plain backdrop.")
def k10():   # crossed arms
    cam = cam_waist()
    pose = dict(x=0, yaw=24, twist=-6, turn=-20, tilt=3, la=CROSS_L, ra=CROSS_R)
    return bg_plain("#D9DFE3", "#E7EBEE") + figs(cam, [pose], shadow=False)


@card(11, "Doorway lean", "S Le F Hom f",
      "Lean a shoulder on the door frame, cross one ankle over the other, hands at the pockets.",
      "Use the doorway as a frame within the frame. Keep the camera level so the uprights stay vertical.",
      alt="Mannequin leaning a shoulder against a door frame with ankles crossed.")
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


@card(12, "Hair touch", "S St T Fie f",
      "Weight on one hip, raise the opposite hand behind the head with the elbow out. Other hand on the hip.",
      "Crop at mid-thigh. Shoot in the last hour of sun with the light behind or beside the subject.",
      alt="Mannequin cropped at the thigh in a golden field, one hand behind the head and one on the hip.")
def k12():   # hair touch
    cam = cam_tq()
    pose = dict(x=0, yaw=-18, hip=5, sh=-4, tilt=7, turn=14,
                ll=(-7, 0, -5, 0), rl=(14, 10, 9, -6),
                la=("ik", "c", (0.42, 2.98, -0.2), (1, 0.7, 0.2)), ra=HIP(-1))
    return sc_field(cam) + figs(cam, [pose], shadow=False)


@card(13, "Walk in", "S Wa F Par f",
      "Walk straight toward the camera, one hand at a pocket, eyes off to the side rather than at the lens.",
      "Centre the path so it leads to the walker. Shoot a burst and keep the frame where the front foot lands.",
      alt="Mannequin walking toward the camera along a tree-lined path.")
def k13():   # walk in
    cam = Cam(**FULL)
    pose = walk(1, x=0, yaw=4, turn=26, nod=5, la=POCKET(1))
    return sc_path(cam) + figs(cam, [pose])


@card(14, "Jump", "S Ac F Bea f",
      "Jump straight up, kick the heels back and throw both arms up in a V.",
      "Get low and shoot a burst. Leave plenty of sky above so the hands stay in frame.",
      alt="Mannequin in mid-air on a beach with arms up and heels kicked back, its shadow on the sand below.")
def k14():   # jump
    cam = Cam(s=62, D=15, hc=4.2, feet_y=720)
    pose = dict(x=0, py=5.5, yaw=-8, bend=-6, nod=-8,
                ll=(22, 35, 10, -75), rl=(26, 20, 12, -85), lf=(10, 50), rf=(10, 50),
                la=(140, 0, 155, -8), ra=(132, 5, 150, 0))
    return sc_beach(cam) + figs(cam, [pose])


@card(15, "Open arms", "S St F Bea b",
      "Face the water with feet apart, arms up in a wide V and chin lifted.",
      "Centre the figure against the brightest part of the sky. Keep the horizon level and below the shoulders.",
      alt="Mannequin seen from behind at sunset on a beach with both arms raised in a V.")
def k15():   # open arms
    cam = Cam(s=64, D=15, hc=4.4, feet_y=712)
    pose = dict(x=0, yaw=178, bend=-4, nod=-10, ll=(9, 0, 7, 0), rl=(9, 0, 7, 0),
                la=(128, -4, 142, -8), ra=(128, -4, 142, -8))
    return sc_beach(cam, sunset=True) + figs(cam, [pose])


@card(16, "Bench lounge", "S Se F Par f",
      "Sit back, rest one ankle on the opposite knee and stretch an arm along the top of the bench.",
      "Sit them off-centre and let the empty half of the bench balance the frame. Camera at seated chest height.",
      alt="Mannequin lounging on a park bench with one ankle on the other knee and an arm along the backrest.")
def k16():   # bench lounge
    cam = Cam(s=70, D=15, hc=4.2, feet_y=708)
    pose = dict(x=-0.5, z=0.05, py=2.12, yaw=10, bend=-12, turn=-14, tilt=2,
                ll=(6, 88, 2, 6),
                rl=("ik", lambda J: J["kl"] + V(0.05, 0.46, 0.1), (-1, 0.2, 0.5)), rf=(-78, 8),
                la=("ik", "r", (2.25, 1.62, -0.78), (0.2, -1, -0.2)),
                ra=("ik", lambda J: (J["kr"] + J["ar"]) / 2 + V(0, 0.38, 0.1)))
    return sc_park(cam) + figs(cam, [pose], extra=bench(cam, -3.3, 3.3))


@card(17, "Knee hug", "S Se F Bea s",
      "Sit on the ground with knees up and hands clasped around the shins. Turn the face to the camera.",
      "Drop the camera to the sitter's eye level and shoot from the side so the shape reads clearly.",
      alt="Mannequin sitting on sand seen from the side, knees drawn up with arms around the shins.")
def k17():   # knee hug
    cam = Cam(s=110, D=10, hc=3.0, feet_y=704)
    pose = dict(x=-0.9, py=0.5, yaw=74, bend=20, turn=-42, tilt=-3, nod=-4,
                ll=("ik", "g", (0.32, 0.17, 2.0), (0.1, 1, 0.2)), rl=("ik", "g", (-0.32, 0.17, 1.9), (-0.1, 1, 0.2)),
                la=("ik", lambda J: shin_mid(J) + J["Rr"] @ V(-0.12, 0.0, 0.34), (1, -0.4, 0.1)),
                ra=("ik", lambda J: shin_mid(J) + J["Rr"] @ V(0.12, -0.05, 0.36), (-1, -0.4, 0.1)))
    return sc_beach(cam) + figs(cam, [pose])


@card(18, "Stool perch", "S Se F Stu f",
      "Perch on a high stool, one foot on the rung and one on the floor, hands loosely together on the thigh.",
      "Full length with floor showing under the feet. Angle the stool slightly rather than square-on.",
      alt="Mannequin perched on a high stool with one foot on the rung and one on the floor.")
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


@card(19, "Sofa read", "S Se F Hom s",
      "Sit sideways with your back against the arm of the sofa, legs along the seat, one knee up, book in both hands.",
      "Shoot from the side at seat height. Keep both feet and the top of the head inside the frame.",
      alt="Mannequin reclining sideways on a sofa with one knee up, holding a book.")
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


@card(20, "Window light", "S St U Hom s",
      "Stand side-on to a window holding a mug at chest height, eyes toward the glass.",
      "Expose for the lit side of the face. Leave space in the direction of the gaze.",
      alt="Waist-up mannequin in profile beside a window, holding a mug.")
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


@card(21, "Low crouch", "S Cr F Str f",
      "Squat with knees apart, forearms resting on the knees, hands hanging. Look up at the lens.",
      "Bring the camera down to knee height so the figure fills the frame. Leave a little ground in front of the feet.",
      alt="Mannequin in a low squat in front of a brick wall, forearms on the knees.")
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


@card(22, "Railing lean", "S Le F Wat s",
      "Lean forward with both forearms on the rail, one knee bent with the toe down, face turned back to the camera.",
      "Stand along the rail so it runs into the distance. Put the figure on a third line, water on the open side.",
      alt="Mannequin leaning on a waterfront railing that recedes into the distance.")
def k22():   # railing lean
    cam = Cam(**FULL)
    pose = dict(x=-0.5, yaw=90, bend=38, turn=-34, nod=-16,
                ll=(0, -9, 0, -9), rl=(0, 12, 0, -34), rf=(8, 40),
                la=("ik", "w", (2.25, 4.45, -0.12), lambda J: V(1.2, 4.3, -0.5) - J["sl"]),
                ra=("ik", "w", (2.3, 4.42, 0.12), lambda J: V(1.2, 4.3, 0.5) - J["sr"]))
    return sc_water(cam) + figs(cam, [pose])
