"""Solo cards 39-52."""
from .helpers import *


@card(39, "Jacket sling", "S St T Str f",
      "Hook a jacket over one shoulder with a raised hand, other hand at the pocket, weight on one hip.",
      "Crop at mid-thigh and leave a little more room on the jacket side.",
      alt="Mannequin cropped at the thigh with one hand raised to hold a jacket over the shoulder.")
def k39():   # jacket sling
    cam = cam_tq()
    pose = dict(x=0, yaw=16, hip=-5, sh=3, turn=-16, tilt=-3,
                rl=(-7, 0, -5, 0), ll=(14, 10, 9, -6),
                ra=("ik", "c", (-0.62, 2.5, -0.3), (-0.35, -0.3, 1)), la=POCKET(1))
    J = solve(pose)
    sx, sy = float(J["sr"][0]), float(J["sr"][1])
    jk = zrect(cam, -0.7, sx - 0.95, sy - 2.5, sx + 0.25, sy + 0.42, "#5F6B7A", rx=18)
    return sc_street(cam, stripes=False) + figs(cam, [J], extra=[Raw(-0.75, jk)], shadow=False)


@card(40, "Lawn lounge", "S Se F Par s",
      "Sit on the grass, lean back on both hands with legs stretched out. Turn the face to the camera.",
      "Get down to the sitter's eye level and shoot side-on so the long line from head to toe fits the width.",
      alt="Mannequin sitting on grass seen from the side, leaning back on both hands with legs stretched out.")
def k40():   # lawn lounge
    cam = Cam(s=76, D=13, hc=2.8, feet_y=690)
    pose = dict(x=-1.7, py=0.5, yaw=80, bend=-28, turn=-44, tilt=-4, nod=-8,
                rl=(2, 88, 0, 84), ll=(0, 86, -6, 88), rf=(0, -50), lf=(0, -50),
                la=("ik", "g", (0.6, 0.14, -1.15), (0.6, 0.3, -1)), ra=("ik", "g", (-0.6, 0.14, -1.1), (-0.6, 0.3, -1)))
    return sc_park(cam) + figs(cam, [pose])


@card(41, "Chin rest", "S Se T Caf s",
      "Sit side-on at a table, elbow on the top and chin resting on the hand, other forearm flat on the table.",
      "Shoot from the side at table height. Leave open space in front of the face.",
      alt="Mannequin seated side-on at a café table with chin resting on one hand.")
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


@card(42, "Stair climb", "S Wa F Ste b",
      "Climb the steps away from the camera and glance back over one shoulder mid-step.",
      "Stand at the bottom, keep the camera level and place the climber in the upper half of the frame.",
      alt="Mannequin climbing wide steps away from the camera, head turned back.")
def k42():   # stair climb
    cam = Cam(s=72, D=14, hc=4.4, feet_y=745)
    o, zf, rise = sc_stairs(cam)
    pose = dict(x=0.2, z=zf(2) - 0.9, py=5.45, yaw=180, twist=-26, turn=-64, bend=6,
                ll=("ik", "w", (-0.25, 3 * rise + 0.17, zf(3) - 0.55), (0, 0.2, 1)),
                rl=("ik", "w", (0.62, 2 * rise + 0.17, zf(2) - 0.5), (0, 0.2, 1)),
                la=(5, 16, 2, 30), ra=(5, -14, 2, -4))
    return o + figs(cam, [pose], shadow=False)


@card(43, "Dock sit", "S Se F Wat b",
      "Sit at the end of the dock with legs over the edge, hands planted behind, head tipped to one side.",
      "Centre the dock so its edges lead to the sitter. Keep the horizon level.",
      alt="Mannequin seen from behind sitting at the end of a wooden dock over water.")
def k43():   # dock sit
    cam = Cam(s=74, D=13, hc=3.4, feet_y=650)
    zend = -1.2
    pose = dict(x=0.5, z=zend + 0.45, py=0.5, yaw=180, bend=-14, tilt=6, turn=-14,
                ll=(8, 90, 0, 0), rl=(8, 90, 0, 0),
                la=("ik", "g", (0.8, 0.14, -0.75), (0.6, 0.3, -1)), ra=("ik", "g", (-0.8, 0.14, -0.7), (-0.6, 0.3, -1)))
    J = solve(pose)
    J["noshins"] = True
    return sc_pier(cam, zend) + figs(cam, [J])


@card(44, "Rail recline", "S Le F Wat f",
      "Lean back on the rail with both elbows hooked over it, one foot crossed in front, chin turned aside.",
      "Shoot square to the rail so it runs level behind the waist. Leave space above the head.",
      alt="Mannequin leaning back against a waterfront railing with both elbows on the rail.")
def k44():   # rail recline
    cam = Cam(**FULL)
    zr = -0.62
    pose = dict(x=0, yaw=8, bend=-11, turn=-16, hip=-4,
                rl=(-5, 9, -4, 9), ll=(-2, 14, -9, 4), lf=(12, 30),
                la=("ik", "w", (1.95, 4.2, -0.3), lambda J: V(1.15, 4.36, zr) - J["sl"]),
                ra=("ik", "w", (-1.85, 4.2, -0.3), lambda J: V(-1.05, 4.36, zr) - J["sr"]))
    return sc_water_x(cam, zr) + figs(cam, [pose], zclip=zr)


@card(45, "Headshot turn", "S St C Stu f",
      "Turn the shoulders about 45 degrees away, then bring the face back to the lens with a slight head tilt.",
      "Crop at mid-chest with a little space above the head. Camera at eye level, focus on the nearer eye.",
      alt="Head-and-shoulders view of a mannequin with shoulders angled away and face toward the camera.")
def k45():   # headshot turn
    cam = cam_tq(top=140, s=300, hc=6.6, D=6)
    pose = dict(x=0.05, yaw=34, turn=-30, tilt=4, nod=2)
    return bg_plain("#DDD8D0", "#EAE6DF") + figs(cam, [pose], shadow=False)


@card(46, "One knee", "S Cr F Fie f",
      "Kneel on one knee, rest a hand on the raised knee and put the other hand on the hip.",
      "Lower the camera to the kneeler's chest height and leave some ground visible in front.",
      alt="Mannequin kneeling on one knee in a field with a hand on the raised knee.")
def k46():   # one knee
    cam = Cam(s=92, D=12, hc=2.8, feet_y=700)
    pose = kneel(x=0, yaw=-22, turn=14, nod=-6, bend=6)
    return sc_field(cam) + figs(cam, [pose])


@card(47, "Beach run", "S Ac F Bea s",
      "Run across the frame with a high front knee and bent arms pumping.",
      "Shoot side-on in burst mode, pan with the runner and leave space ahead of them.",
      alt="Mannequin seen side-on running along a beach, both feet off the ground.")
def k47():   # beach run
    cam = Cam(s=66, D=15, hc=4.4, feet_y=712)
    pose = dict(x=-0.2, py=4.35, yaw=76, bend=12, turn=-8,
                rl=(0, 58, 0, -18), rf=(4, 20), ll=(0, -24, 0, -98), lf=(4, 60),
                la=(6, 42, -4, 132), ra=(6, -46, 2, 44))
    return sc_beach(cam) + figs(cam, [pose])


@card(48, "Rock sit", "S Se W Vie s",
      "Sit on a rock side-on to the camera, feet down, one hand on the knee, looking out at the view.",
      "Go wide with the sitter small in the frame and facing into the open side.",
      alt="Small mannequin sitting side-on on a rock, facing layered mountains.")
def k48():   # rock sit
    cam = Cam(s=46, D=22, hc=4.4, feet_y=654)
    rock = box(cam, 1.25, 3.1, 0, 1.7, -0.85, 0.85, "#B7B2A8", "#9E998F", "#A9A49A")
    pose = sit(x=2.15, yaw=-84, bend=-4, turn=4,
               la=("ik", lambda J: J["kl"] + V(0.3, 0.36, 0)), ra=("ik", "g", (-0.2, 1.84, -0.75), (-0.5, 0.2, -1)))
    return sc_view(cam) + figs(cam, [pose], extra=rock)


@card(49, "Elbows on the grass", "S Ly F Par f",
      "Lie on your front propped on both elbows, hands forward, feet kicked up behind.",
      "Put the camera almost on the ground at the subject's eye level, a few steps in front.",
      alt="Mannequin lying on its front on grass, propped on its elbows with feet kicked up.")
def k49():   # elbows on the grass
    cam = Cam(s=120, D=9, hc=1.7, feet_y=640)
    pose = dict(x=0.1, z=-2.3, py=0.5, yaw=-14, bend=70, nod=-62, turn=6, who="a",
                ll=(8, -90, 6, -150), rl=(8, -90, 8, -128), lf=(0, 0), rf=(0, 0),
                la=("ik", "g", (0.35, 0.16, 2.75), (0.9, -0.6, 0.3)), ra=("ik", "g", (-0.2, 0.16, 2.8), (-0.9, -0.6, 0.3)))
    return sc_park(cam) + figs(cam, [pose])


@card(50, "Coffee walk", "S Wa T Str f",
      "Walk toward the camera with a cup at chest height, other hand at the pocket, eyes off to one side.",
      "Crop at mid-thigh and shoot a burst as they approach.",
      alt="Mannequin cropped at the thigh walking toward the camera holding a cup.")
def k50():   # coffee walk
    cam = cam_tq()
    pose = walk(1, x=0, yaw=6, turn=-18, tilt=-2, la=POCKET(1),
                ra=("ik", "c", (-0.42, 1.5, 0.78), (-0.6, -1, 0)))
    J = solve(pose)
    cup = small_cup(cam, J["hdr"] + V(0, -0.1, 0.05), z=float(J["hdr"][2]) + 0.3)
    return sc_street(cam, stripes=False) + figs(cam, [J], extra=[cup], shadow=False)


@card(51, "Hero stance", "S St F Fie f",
      "Feet wider than the shoulders, both hands on the hips, chin lifted.",
      "Shoot from knee height so the figure rises against the sky.",
      alt="Mannequin standing with feet apart and hands on hips, seen from a low camera.")
def k51():   # hero stance
    cam = Cam(s=82, D=12, hc=1.5, feet_y=744)
    pose = dict(x=0, yaw=-6, nod=-10, ll=(11, 0, 9, 0), rl=(11, 0, 9, 0), la=HIP(1), ra=HIP(-1))
    return sc_field(cam) + figs(cam, [pose])


@card(52, "Cuff check", "S St U Str f",
      "Bring one hand across to the other wrist at waist level and look down at it.",
      "Crop just below the hands. Works best as a candid while they really adjust a cuff or watch.",
      alt="Waist-up mannequin looking down with hands together at the waist.")
def k52():   # cuff check
    cam = cam_waist(s=170)
    pose = dict(x=0, yaw=-14, nod=24, turn=12, tilt=3, sh=2,
                ra=("ik", "c", (0.12, 1.02, 0.55), (-0.8, -0.6, 0.2)), la=("ik", "c", (-0.12, 1.1, 0.6), (0.8, -0.6, 0.2)))
    return sc_street(cam, stripes=False) + figs(cam, [pose], shadow=False)
