#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: 'WAITED 13 YEARS FOR GTA 6 / MEANWHILE, MY AGENT GOT PAID'.

Vice City neon-sunset scene, hand-drawn procedurally with PIL: a convertible with
Lucia driving and Jason riding shotgun, and the make.fun ghost leaning out of the
back holding its magenta star coin. No Rockstar art, no copied template.
Output: meme.png, 1080x1080.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
random.seed(6)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(BOLD, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def sparkle(d, cx, cy, r):
    """Four-pointed sparkle star (the ghost's eyes)."""
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.28
        ang = math.radians(i * 45)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(10, 10, 14))


def draw_sky(d):
    stops = [(0, (26, 11, 46)), (0.35, (90, 20, 90)), (0.55, (164, 19, 60)),
             (0.75, (255, 107, 53)), (1.0, (255, 158, 0))]
    for y in range(640):
        t = y / 639
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                tt = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
                d.line([(0, y), (W, y)], fill=lerp(stops[i][1], stops[i + 1][1], tt))
                break
    # stars in the upper sky
    for _ in range(90):
        x = random.randint(0, W - 1)
        y = random.randint(0, 300)
        r = random.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))


def draw_sun(d):
    cx, cy, r = 540, 520, 165
    for y in range(cy - r, cy + r + 1):
        dy = y - cy
        half = int(math.sqrt(max(0, r * r - dy * dy)))
        # retro slits across the lower half of the sun
        if dy > 10 and (dy - 10) % 30 < 9:
            continue
        t = (y - (cy - r)) / (2 * r)
        col = lerp((255, 214, 64), (255, 110, 0), t)
        d.line([(cx - half, y), (cx + half, y)], fill=col)


def draw_ocean(d):
    d.rectangle([0, 620, W, 720], fill=(11, 61, 92))
    # sun reflection streaks
    for _ in range(46):
        x = random.randint(430, 650)
        y = random.randint(625, 715)
        ln = random.randint(18, 70)
        d.line([(x, y), (x + ln, y)], fill=(255, 170, 60), width=3)


def draw_road(d):
    d.rectangle([0, 720, W, H], fill=(24, 24, 30))
    d.line([(0, 720), (W, 720)], fill=(255, 183, 77), width=4)
    # dashed centre line
    for x in range(20, W, 90):
        d.rectangle([x, 795, x + 48, 803], fill=(220, 220, 220))


def draw_palm(d, x, base_y, height, lean, flip=False):
    top_x = x + lean
    top_y = base_y - height
    # trunk: curved polyline
    pts = []
    for i in range(9):
        t = i / 8
        px = x + lean * t * t + (4 if flip else -4) * math.sin(t * 3)
        py = base_y - height * t
        pts.append((px, py))
    d.line(pts, fill=(13, 13, 18), width=20, joint="curve")
    # fronds: smooth quadratic-bezier arcs drooping from the crown
    for ang in (-165, -140, -115, -85, -55, -28, -2):
        a = math.radians(ang if not flip else 180 - ang)
        ex = top_x + 165 * math.cos(a)
        ey = top_y + 105 * math.sin(a) + 70
        cxp = top_x + 95 * math.cos(a)
        cyp = top_y + 55 * math.sin(a) - 30
        curve = []
        for i in range(13):
            t = i / 12
            bx = (1 - t) ** 2 * top_x + 2 * (1 - t) * t * cxp + t * t * ex
            by = (1 - t) ** 2 * top_y + 2 * (1 - t) * t * cyp + t * t * ey
            curve.append((bx, by))
        d.line(curve, fill=(13, 13, 18), width=10, joint="curve")
    # coconuts
    d.ellipse([top_x - 14, top_y - 2, top_x + 2, top_y + 14], fill=(13, 13, 18))
    d.ellipse([top_x + 2, top_y - 2, top_x + 18, top_y + 14], fill=(13, 13, 18))


def draw_ghost(d, cx, cy, s):
    """make.fun ghost, worked into the scene in the back of the convertible.

    White body, thick black outline, two black four-pointed sparkle eyes,
    one round little hand, holding a magenta coin with a white star.
    s = body width in px.
    """
    w, h = s, int(s * 1.25)
    x0, y0 = cx - w // 2, cy - h // 2
    # body outline (black, slightly larger) then white body
    def body_path(dx, dy, fill):
        # rounded top + wavy bottom
        pts = []
        steps = 24
        for i in range(steps + 1):
            a = math.pi + i * math.pi / steps  # left to right over the top
            pts.append((cx + dx + (w // 2) * math.cos(a),
                        y0 + dy + h * 0.42 + (h * 0.42) * math.sin(a)))
        # wavy hem: 3 waves along the bottom, right to left (the arc ended
        # on the right side, so the hem must run back to the left)
        hem_y = y0 + dy + h
        pts.append((x0 + dx + w, hem_y))
        for i in range(2, -1, -1):
            seg = w / 3
            bx = x0 + dx + i * seg
            pts.append((bx + seg * 0.75, hem_y - 18))
            pts.append((bx + seg * 0.5, hem_y))
            pts.append((bx + seg * 0.25, hem_y - 18))
        pts.append((x0 + dx, hem_y))
        d.polygon(pts, fill=fill)
    body_path(0, 0, (10, 10, 14))
    # redraw white body slightly inset so the black shows as an outline
    def body_inner():
        pts = []
        steps = 24
        iw, ih = w - 14, h - 12
        ix0, iy0 = x0 + 7, y0 + 6
        for i in range(steps + 1):
            a = math.pi + i * math.pi / steps
            pts.append((cx + (iw // 2) * math.cos(a),
                        iy0 + ih * 0.42 + (ih * 0.42) * math.sin(a)))
        hem_y = iy0 + ih
        pts.append((ix0 + iw, hem_y))
        for i in range(2, -1, -1):
            seg = iw / 3
            bx = ix0 + i * seg
            pts.append((bx + seg * 0.75, hem_y - 16))
            pts.append((bx + seg * 0.5, hem_y))
            pts.append((bx + seg * 0.25, hem_y - 16))
        pts.append((ix0, hem_y))
        d.polygon(pts, fill=(255, 255, 255))
    body_inner()
    # eyes: two black sparkles
    ey = y0 + int(h * 0.38)
    sparkle(d, cx - int(w * 0.20), ey, 17)
    sparkle(d, cx + int(w * 0.20), ey, 17)
    # little round hand + magenta coin with white star, raised on the right
    hx, hy = cx + int(w * 0.52), y0 + int(h * 0.30)
    d.ellipse([hx - 26, hy - 26, hx + 26, hy + 26], fill=(255, 255, 255),
              outline=(10, 10, 14), width=5)
    # arm from body to the hand
    d.line([(cx + int(w * 0.30), y0 + int(h * 0.55)), (hx - 10, hy + 14)],
           fill=(255, 255, 255), width=22)
    # coin above the hand
    coin_cx, coin_cy, cr = hx + 6, hy - 52, 34
    d.ellipse([coin_cx - cr, coin_cy - cr, coin_cx + cr, coin_cy + cr],
              fill=(226, 0, 122), outline=(10, 10, 14), width=5)
    d.polygon(star_points(coin_cx, coin_cy, 22, 9), fill=(255, 255, 255))


def draw_car(d):
    # ---- convertible, facing right, hot pink ----
    body = (235, 845, 855, 925)
    # body main block
    d.rounded_rectangle(body, radius=26, fill=(255, 46, 136), outline=(10, 10, 14), width=6)
    # hood slope (front, right)
    d.polygon([(640, 845), (855, 845), (855, 885), (640, 885)],
              fill=(255, 46, 136), outline=(10, 10, 14))
    # cabin opening (dark interior)
    d.rounded_rectangle([385, 800, 620, 850], radius=14, fill=(16, 16, 22),
                        outline=(10, 10, 14), width=5)
    # windshield
    d.polygon([(618, 848), (648, 788), (668, 788), (645, 848)], fill=(140, 210, 235),
              outline=(10, 10, 14))
    # door line + handle
    d.line([(520, 855), (520, 915)], fill=(10, 10, 14), width=4)
    d.rounded_rectangle([545, 868, 590, 878], radius=5, fill=(10, 10, 14))
    # headlight + taillight
    d.ellipse([828, 862, 852, 880], fill=(255, 240, 150), outline=(10, 10, 14), width=3)
    d.rectangle([238, 862, 252, 880], fill=(255, 40, 40), outline=(10, 10, 14), width=3)
    # "make.fun" bumper sticker on the trunk lid, worked into the scene
    d.rectangle([252, 848, 378, 864], fill=(255, 255, 255), outline=(10, 10, 14), width=3)
    d.text((315, 856), "make.fun", font=font(13), fill=(10, 10, 14), anchor="mm")
    # wheels
    for wx in (335, 745):
        d.ellipse([wx - 52, 878, wx + 52, 982], fill=(12, 12, 16), outline=(10, 10, 14), width=5)
        d.ellipse([wx - 24, 906, wx + 24, 954], fill=(200, 200, 210), outline=(10, 10, 14), width=4)
        d.ellipse([wx - 8, 922, wx + 8, 938], fill=(10, 10, 14))
    # ---- people in the cabin ----
    # Jason, passenger (left): cap sits on top of the head, brim at the forehead
    d.rounded_rectangle([440, 822, 500, 852], radius=12, fill=(20, 90, 110))
    d.ellipse([448, 778, 492, 822], fill=(232, 184, 145))  # head
    d.pieslice([446, 764, 494, 790], 180, 360, fill=(30, 30, 38))  # cap
    d.rectangle([444, 784, 496, 791], fill=(30, 30, 38))  # cap brim
    # Lucia, driver (right): long dark hair + pink top
    d.rounded_rectangle([545, 822, 605, 852], radius=12, fill=(255, 120, 180))
    d.ellipse([553, 776, 597, 820], fill=(232, 184, 145))  # head
    d.polygon([(550, 782), (548, 830), (566, 830), (560, 786)], fill=(25, 20, 28))  # hair L
    d.polygon([(600, 782), (602, 830), (586, 830), (592, 786)], fill=(25, 20, 28))  # hair R
    d.pieslice([550, 770, 600, 796], 180, 360, fill=(25, 20, 28))  # hair top


def draw_text(d, text, y, size, stroke=8):
    f = font(size)
    d.text((W // 2, y), text, font=f, fill=(255, 255, 255),
           stroke_width=stroke, stroke_fill=(10, 10, 14), anchor="ma")


def draw_text_fit(d, text, y, size, max_width, stroke=6):
    """One line, shrunk until it fits max_width (never clipped at the edges)."""
    f = font(size)
    while f.getlength(text) > max_width and size > 20:
        size -= 2
        f = font(size)
    d.text((W // 2, y), text, font=f, fill=(255, 255, 255),
           stroke_width=stroke, stroke_fill=(10, 10, 14), anchor="ma")


def main():
    img = Image.new("RGB", (W, H), (26, 11, 46))
    d = ImageDraw.Draw(img)
    draw_sky(d)
    draw_sun(d)
    draw_ocean(d)
    draw_road(d)
    draw_palm(d, 95, 730, 330, 60)
    draw_palm(d, 990, 730, 300, -55, flip=True)
    # the make.fun ghost first, so the car body hides its hem: it sits in the back
    draw_ghost(d, 315, 760, 170)
    draw_car(d)
    # caption, big and readable at 480 px
    draw_text(d, "WAITED 13 YEARS", 46, 88, stroke=9)
    draw_text(d, "FOR GTA 6", 140, 88, stroke=9)
    draw_text_fit(d, "MEANWHILE, MY AGENT GOT PAID", 992, 62, 1020, stroke=6)
    img.save("meme.png")
    img.resize((480, 480), Image.LANCZOS).save("meme-480.png")
    print("saved meme.png + meme-480.png")


if __name__ == "__main__":
    main()
