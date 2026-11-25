"""3D mannequin -> SVG.

World: X right, Y up, Z toward the camera. Units are head-heights (H).
A figure facing the camera faces +Z; its LEFT side is +X (screen right).
"""
import math
import numpy as np

INK = "#2F3033"
PEOPLE = {            # lit, shade, face
    "a": ("#F7E9D2", "#DEC096", "#FFFAF0"),
    "b": ("#CDE5F7", "#9CC3E4", "#F2FAFF"),
    "c": ("#FAD4C8", "#E9A690", "#FFF4EF"),
    "d": ("#D9ECD1", "#AECDA3", "#F6FCF2"),
    "e": ("#E4DCF4", "#BCACDD", "#F9F6FF"),
}
LIGHT2D = np.array([-0.56, -0.83])            # toward the light, on screen
LDIR = np.array([0.42, -1.0, -0.36])          # direction light travels (for cast shadows)


def Rx(a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def Rz(a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def V(*a):
    return np.array(a, dtype=float)


def f(n):
    s = "%.1f" % n
    return s[:-2] if s.endswith(".0") else s


class Cam:
    """Level camera at height hc, distance D from z=0. s = px per head at z=0."""

    def __init__(self, s=68, D=15.0, hc=4.4, feet_y=700, cx=300):
        self.s, self.D, self.hc, self.cx = s, D, hc, cx
        self.f = s * D
        self.hy = feet_y - hc * s          # horizon line on screen

    def k(self, z):
        return self.f / max(self.D - z, 0.4)

    def p(self, pt):
        k = self.k(pt[2])
        return np.array([self.cx + pt[0] * k, self.hy - (pt[1] - self.hc) * k])

    def gy(self, z, y=0.0):
        return self.hy + (self.hc - y) * self.k(z)


# ------------------------------------------------------------ 2D path helpers
def circle_d(c, r):
    return "M%s %sa%s %s 0 1 1 %s 0a%s %s 0 1 1 %s 0Z" % (
        f(c[0] - r), f(c[1]), f(r), f(r), f(2 * r), f(r), f(r), f(-2 * r))


def poly_d(pts):
    area = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        area += x1 * y2 - x2 * y1
    if area < 0:
        pts = pts[::-1]
    return "M" + "L".join("%s %s" % (f(x), f(y)) for x, y in pts) + "Z"


def hull_d(c1, r1, c2, r2):
    """Outline of the convex hull of two circles as ONE closed sub-path (no inner edges)."""
    d = c2 - c1
    L = float(np.hypot(*d))
    if L <= abs(r1 - r2) + 1e-6:
        return circle_d(c1, r1) if r1 >= r2 else circle_d(c2, r2)
    u = d / L
    pr = np.array([-u[1], u[0]])
    a = (r1 - r2) / L
    b = math.sqrt(max(0.0, 1 - a * a))
    n1, n2 = u * a + pr * b, u * a - pr * b
    A, B, Cc, Dd = c1 + n1 * r1, c2 + n1 * r2, c2 + n2 * r2, c1 + n2 * r1
    return "M%s %sL%s %sA%s %s 0 %d 0 %s %sL%s %sA%s %s 0 %d 0 %s %sZ" % (
        f(A[0]), f(A[1]), f(B[0]), f(B[1]), f(r2), f(r2), 1 if a < 0 else 0, f(Cc[0]), f(Cc[1]),
        f(Dd[0]), f(Dd[1]), f(r1), f(r1), 1 if a > 0 else 0, f(A[0]), f(A[1]))


def ellipse_d(c, rx, ry, rot):
    kk = 0.5523
    pts = [(rx, 0), (rx, kk * ry), (kk * rx, ry), (0, ry), (-kk * rx, ry), (-rx, kk * ry), (-rx, 0),
           (-rx, -kk * ry), (-kk * rx, -ry), (0, -ry), (kk * rx, -ry), (rx, -kk * ry), (rx, 0)]
    cs, sn = math.cos(rot), math.sin(rot)
    P = [(c[0] + x * cs - y * sn, c[1] + x * sn + y * cs) for x, y in pts]
    d = "M%s %s" % (f(P[0][0]), f(P[0][1]))
    for i in range(1, 13, 3):
        d += "C%s %s %s %s %s %s" % tuple(f(t) for q in P[i:i + 3] for t in q)
    return d + "Z"


# ------------------------------------------------------------ primitives
class Cap:
    def __init__(self, p1, r1, p2, r2, cols, bias=0.0, shade=True):
        self.p1, self.r1, self.p2, self.r2, self.cols, self.bias, self.shade = p1, r1, p2, r2, cols, bias, shade

    def z(self):
        return (self.p1[2] + self.p2[2]) / 2 + self.bias

    def spheres(self):
        return [(self.p1, self.r1), (self.p2, self.r2)]

    def svg(self, cam, lw):
        c1, c2 = cam.p(self.p1), cam.p(self.p2)
        R1, R2 = self.r1 * cam.k(self.p1[2]), self.r2 * cam.k(self.p2[2])
        lit, shade = self.cols[0], self.cols[1]
        o = '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"></path>' % (
            hull_d(c1, R1, c2, R2), shade if self.shade else lit, INK, f(lw))
        if self.shade and min(R1, R2) > 1.5:
            q = 0.26
            o += '<path d="%s" fill="%s"></path>' % (
                hull_d(c1 + LIGHT2D * R1 * q, R1 * (1 - q), c2 + LIGHT2D * R2 * q, R2 * (1 - q)), lit)
        return o


class Ell:
    def __init__(self, c, axes, R, cols, bias=0.0, line=False, shade=True):
        self.c, self.axes, self.R, self.cols, self.bias, self.line, self.shade = c, axes, R, cols, bias, line, shade

    def z(self):
        return self.c[2] + self.bias

    def spheres(self):
        return [(self.c, float(np.mean(self.axes)))]

    def outline(self, cam):
        a, b, c = self.axes
        A = self.R @ np.diag([1 / a ** 2, 1 / b ** 2, 1 / c ** 2]) @ self.R.T
        B = A[:2, :2] - np.outer(A[:2, 2], A[2, :2]) / A[2, 2]
        w, v = np.linalg.eigh(B)
        k = cam.k(self.c[2])
        rx, ry = k / math.sqrt(w[0]), k / math.sqrt(w[1])
        rot = math.atan2(-v[1, 0], v[0, 0])
        return cam.p(self.c), rx, ry, rot, k

    def svg(self, cam, lw):
        cen, rx, ry, rot, k = self.outline(cam)
        lit, shade = self.cols[0], self.cols[1]
        o = '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"></path>' % (
            ellipse_d(cen, rx, ry, rot), shade if self.shade else lit, INK, f(lw))
        if self.shade:
            q = 0.22
            cs, sn = math.cos(rot), math.sin(rot)
            dl = np.array([LIGHT2D[0] * cs + LIGHT2D[1] * sn, -LIGHT2D[0] * sn + LIGHT2D[1] * cs])
            sc = 1 / math.sqrt((dl[0] / rx) ** 2 + (dl[1] / ry) ** 2)
            edge = LIGHT2D * sc
            o += '<path d="%s" fill="%s"></path>' % (ellipse_d(cen + edge * q, rx * (1 - q), ry * (1 - q), rot), lit)
        if self.line:
            a, b, c = self.axes
            pts = []
            for t in range(18, 163, 8):
                tr = math.radians(t)
                loc = V(0, b * math.cos(tr), c * math.sin(tr))
                n = self.R @ V(0, math.cos(tr) / b, math.sin(tr) / c)
                if n[2] > 0.12 * np.linalg.norm(n):
                    w_ = self.R @ loc
                    pts.append(cen + np.array([w_[0], -w_[1]]) * k)
            if len(pts) > 2:
                o += '<path d="M%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity="0.45"></path>' % (
                    "L".join("%s %s" % (f(x), f(y)) for x, y in pts), INK, f(max(1.0, lw * 0.55)))
        return o


class Raw:
    """Pre-projected SVG with a depth (z toward camera) for sorting props among figures."""

    def __init__(self, z, svg):
        self._z, self._svg = z, svg

    def z(self):
        return self._z

    def spheres(self):
        return []

    def svg(self, cam, lw):
        return self._svg


# ------------------------------------------------------------ skeleton
DEF = dict(x=0.0, z=0.0, yaw=0.0, hip=0.0, sh=0.0, bend=0.0, twist=0.0, turn=0.0, tilt=0.0, nod=0.0,
           la=(5, 2, 2, 8), ra=(5, 2, 2, 8), ll=(2, 0, 0, 0), rl=(2, 0, 0, 0), lf=(12, 0), rf=(12, 0),
           py=None, gy=0.0, who="a", size=1.0)


def limb_dir(sig, out, fwd):
    o, w = math.radians(out), math.radians(fwd)
    return V(sig * math.sin(o), -math.cos(o) * math.cos(w), math.cos(o) * math.sin(w))


def ik(S, T, l1, l2, pole):
    v = T - S
    d0 = float(np.linalg.norm(v)) or 1e-6
    u = v / d0
    d = min(max(d0, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-3)
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    w = pole - np.dot(pole, u) * u
    n = float(np.linalg.norm(w))
    w = w / n if n > 1e-6 else V(0, 0, 1)
    return S + u * a + w * h, S + u * d


def solve(pose):
    p = dict(DEF)
    p.update(pose)
    m = p["size"]
    Rr = Ry(p["yaw"])
    Rp = Rr @ Rz(p["hip"])
    Rc = Rr @ Ry(p["twist"]) @ Rz(p["sh"]) @ Rx(p["bend"])
    Rh = Rc @ Ry(p["turn"]) @ Rz(-p["tilt"]) @ Rx(p["nod"])
    J = {"p": p, "Rr": Rr, "Rp": Rp, "Rc": Rc, "Rh": Rh, "m": m}
    TH, SHN, UA, FA = 1.92 * m, 1.80 * m, 1.38 * m, 1.18 * m

    def frame_pt(P, fr, t):
        if callable(fr):
            return fr(J)
        t = V(*t) * (1.0 if fr == "w" else m)
        if fr == "w":
            return t
        if fr == "g":
            return V(P[0], p["gy"], P[2]) + Rr @ t
        return P + {"p": Rp, "c": Rc, "r": Rr}[fr] @ t

    def legs(P):
        low = 1e9
        for sd, sig in (("l", 1), ("r", -1)):
            spec = p[sd + "l"]
            hipj = P + Rp @ V(sig * 0.42 * m, -0.12 * m, 0)
            if spec[0] == "ik":
                T = frame_pt(P, spec[1], spec[2] if not callable(spec[1]) else None)
                pole = Rr @ V(*(spec[3] if len(spec) > 3 and spec[3] is not None else (sig * 0.15, 0.2, 1)))
                kn, an = ik(hipj, T, TH, SHN, pole)
            else:
                kn = hipj + Rp @ limb_dir(sig, spec[0], spec[1]) * TH
                an = kn + Rp @ limb_dir(sig, spec[2], spec[3]) * SHN
            toe_out, pitch = p[sd + "f"]
            flat = Rr @ Ry(sig * toe_out) @ V(0, 0, 1)
            pr = math.radians(pitch)
            fd = flat * math.cos(pr) - V(0, 1, 0) * math.sin(pr)
            heel = an - fd * 0.13 * m - V(0, 0.02 * m, 0)
            toe = an + fd * 0.52 * m - V(0, 0.045 * m, 0) * math.cos(pr)
            J["h" + sd], J["k" + sd], J["a" + sd], J["heel" + sd], J["toe" + sd] = hipj, kn, an, heel, toe
            low = min(low, heel[1] - 0.15 * m, toe[1] - 0.115 * m)
        return low

    if p["py"] is None:
        P = V(p["x"], 0, p["z"])
        low = legs(P)
        P = V(p["x"], p["gy"] - low, p["z"])
    else:
        P = V(p["x"], p["gy"] + p["py"] * m, p["z"])
    legs(P)
    J["P"] = P
    J["N"] = P + Rc @ V(0, 2.25 * m, 0)
    J["chest"] = P + Rc @ V(0, 1.50 * m, 0)
    J["head"] = J["N"] + Rc @ V(0, 0.30 * m, 0) + Rh @ V(0, 0.5 * m, 0.04 * m)
    for sd, sig in (("l", 1), ("r", -1)):
        J["s" + sd] = P + Rc @ V(sig * 0.84 * m, 2.08 * m, 0)
    for sd, sig in (("l", 1), ("r", -1)):
        spec = p[sd + "a"]
        S = J["s" + sd]
        if spec[0] == "ik":
            T = frame_pt(P, spec[1], spec[2] if not callable(spec[1]) else None)
            if len(spec) > 3 and callable(spec[3]):
                pole = spec[3](J)
            else:
                pole = Rr @ V(*(spec[3] if len(spec) > 3 and spec[3] is not None else (sig * 0.7, -0.5, -0.8)))
            el, wr = ik(S, T, UA, FA, pole)
        else:
            el = S + Rc @ limb_dir(sig, spec[0], spec[1]) * UA
            wr = el + Rc @ limb_dir(sig, spec[2], spec[3]) * FA
        d2 = (wr - el) / (np.linalg.norm(wr - el) or 1)
        J["e" + sd], J["w" + sd], J["hd" + sd] = el, wr, wr + d2 * 0.30 * m
    return J


def mirror(pose):
    q = dict(pose)
    for k_ in ("x", "yaw", "hip", "sh", "twist", "turn", "tilt"):
        if k_ in q:
            q[k_] = -q[k_]

    def flip(spec):
        if spec[0] != "ik" or callable(spec[1]):
            return spec
        t = (-spec[2][0], spec[2][1], spec[2][2])
        pole = None
        if len(spec) > 3 and spec[3] is not None:
            pole = (-spec[3][0], spec[3][1], spec[3][2])
        return ("ik", spec[1], t, pole)

    for a_, b_ in (("la", "ra"), ("ll", "rl"), ("lf", "rf")):
        va, vb = pose.get(a_), pose.get(b_)
        q.pop(a_, None)
        q.pop(b_, None)
        if vb is not None:
            q[a_] = flip(vb) if a_ != "lf" else vb
        if va is not None:
            q[b_] = flip(va) if a_ != "lf" else va
    return q


def parts(J, legs=True, shins=True):
    p, m = J["p"], J["m"]
    cols = PEOPLE[p["who"]]
    Rp, Rc, Rh, P = J["Rp"], J["Rc"], J["Rh"], J["P"]
    out = []
    out.append(Ell(P + Rp @ V(0, 0.02 * m, 0), (0.72 * m, 0.50 * m, 0.47 * m), Rp, cols, line=True))
    out.append(Cap(P + Rp @ V(0, 0.25 * m, 0), 0.48 * m, P + Rc @ V(0, 1.0 * m, 0), 0.52 * m, cols, bias=-0.12))
    out.append(Ell(J["chest"], (0.90 * m, 0.92 * m, 0.52 * m), Rc, cols, bias=0.02, line=True))
    out.append(Cap(J["N"] - Rc @ V(0, 0.06 * m, 0), 0.19 * m, J["N"] + Rc @ V(0, 0.36 * m, 0), 0.17 * m, cols, bias=-0.03))
    out.append(Ell(J["head"], (0.40 * m, 0.50 * m, 0.45 * m), Rh, cols, bias=0.03))
    # face: mask, nose, eyes -- only when turned toward the camera
    fwd = Rh @ V(0, 0, 1)
    out.append(Ell(J["head"] + Rh @ V(0, -0.03 * m, 0.36 * m), (0.29 * m, 0.36 * m, 0.11 * m), Rh,
                   (cols[2], cols[0]), bias=0.05 if fwd[2] > -0.1 else -0.5, shade=False))
    if fwd[2] > 0.25:
        for sx in (-0.13, 0.13):
            e = J["head"] + Rh @ V(sx * m, 0.05 * m, 0.475 * m)
            out.append(Cap(e, 0.035 * m, e, 0.035 * m, (INK, INK), bias=0.3, shade=False))
    for sd in ("l", "r"):
        out.append(Cap(J["s" + sd], 0.27 * m, J["s" + sd], 0.27 * m, cols, bias=0.10))
        out.append(Cap(J["s" + sd], 0.225 * m, J["e" + sd], 0.185 * m, cols, bias=0.12))
        out.append(Cap(J["e" + sd], 0.20 * m, J["e" + sd], 0.20 * m, cols, bias=0.13))
        out.append(Cap(J["e" + sd], 0.18 * m, J["w" + sd], 0.14 * m, cols, bias=0.14))
        out.append(Cap(J["w" + sd], 0.165 * m, J["hd" + sd], 0.135 * m, cols, bias=0.16))
        if not legs:
            continue
        out.append(Cap(J["h" + sd], 0.37 * m, J["k" + sd], 0.25 * m, cols, bias=0.08))
        out.append(Cap(J["k" + sd], 0.265 * m, J["k" + sd], 0.265 * m, cols, bias=0.09))
        if not shins:
            continue
        out.append(Cap(J["k" + sd], 0.24 * m, J["a" + sd], 0.155 * m, cols, bias=0.10))
        out.append(Cap(J["heel" + sd], 0.15 * m, J["toe" + sd], 0.115 * m, cols, bias=0.11))
    return out


# ------------------------------------------------------------ shadows + render
def _hull(pts):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def cast_shadow(prims, cam, gy=0.0, opacity=0.17, zclip=None):
    d = ""
    for pr in prims:
        sp = pr.spheres()
        if not sp:
            continue
        ring = []
        for c, r in sp:
            if c[1] < gy:
                continue
            g = c + LDIR * ((gy - c[1]) / LDIR[1])
            if zclip is not None and g[2] < zclip:
                g = V(g[0], g[1], zclip)
            for i in range(10):
                a = i * math.pi / 5
                ring.append((g[0] + r * math.cos(a), g[2] + r * math.sin(a)))
        h = _hull(ring)
        if len(h) < 3:
            continue
        scr = [cam.p(V(x, gy, z)) for x, z in h if cam.D - z > 1.0]
        if len(scr) >= 3:
            d += poly_d([(q[0], q[1]) for q in scr])
    if not d:
        return ""
    return '<path d="%s" fill="#20242B" opacity="%s"></path>' % (d, "%.2f" % opacity)


def render(prims, cam, lw=None):
    lw = lw or min(3.2, max(2.0, cam.s * 0.036))
    return "".join(pr.svg(cam, lw) for pr in sorted(prims, key=lambda q: q.z()))
