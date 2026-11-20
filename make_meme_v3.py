#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme v3: an OFFICIAL DOCTOR'S NOTE.

Idea (original, in the winning document-meme format — but NOT the leaders'
formats: no invoice, no library fine, no hurricane warning, no bail bond,
no toll ticket, no sheriff booking sheet):

    VICE CITY GENERAL HOSPITAL issues a doctor's note excusing EVERY GTA
    FAN from work on launch day, May 26 2026: diagnosis "VICE CITY FEVER",
    symptoms "13-year wait, 200 GB download, $70 lighter", recovery:
    NEVER. The note is signed by Dr. Ghost and stamped with the make.fun
    ghost as the hospital's official seal — the mascot worked INTO the
    document as its own seal, not pasted on as a sticker. The footer band
    delivers the pitch: MY AGENT GOT PAID ON make.fun.

Why this should beat v1/v2 (sunset scene, 61.82%): the top of the board
is all official-document memes with a GTA-6-specific joke + an agent
twist; this is that format, with a launch-day sick day — one of the
judge's own listed GTA 6 angles — as the joke, and every fact in it is
a real launch-day fact (13 years since GTA V, $70, huge download,
Leonida, Lucia).

Drawn procedurally with PIL. The ghost is drawn by make_meme.draw_ghost
(same repo, v2's function, reused here for the seal).
Output: meme-v3.png, 1080x1080, plus a 480x480 downscale for the
thumbnail check.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont

from make_meme import draw_ghost  # noqa: E402  (ghost from v2, same repo)

W = H = 1080

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

INK = (26, 26, 30)
GRAY = (110, 110, 118)
RED = (192, 57, 43)
MAGENTA = (226, 0, 122)
PAPER = (255, 255, 255)
BG = (172, 194, 204)


def f_bold(size):
    return ImageFont.truetype(BOLD, size)


def f_reg(size):
    return ImageFont.truetype(REG, size)


def f_serif(size):
    return ImageFont.truetype(SERIF, size)


def f_script(size):
    return ImageFont.truetype(SERIF_IT, size)


def text_fit(d, text, cx, y, size, max_w, fill=INK):
    """One centred line, shrunk until it fits max_w."""
    while size > 16:
        fnt = f_bold(size)
        if fnt.getlength(text) <= max_w:
            break
        size -= 2
    d.text((cx, y), text, font=f_bold(size), fill=fill, anchor="ma")


def wrap(d, text, font, max_w):
    """Greedy word wrap. Returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_cross(d, x, y, s):
    """Red cross in a rounded red square (hospital mark)."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=16, fill=RED)
    bw = s // 5
    d.rectangle([x + s // 2 - bw // 2, y + s // 6,
                 x + s // 2 + bw // 2, y + 5 * s // 6], fill=PAPER)
    d.rectangle([x + s // 6, y + s // 2 - bw // 2,
                 x + 5 * s // 6, y + s // 2 + bw // 2], fill=PAPER)


def draw_seal(size=220):
    """The make.fun ghost as an official seal: magenta disc + ghost,
    drawn straight onto one RGBA layer (the ghost's white body reads
    against the magenta disc), rotated slightly like a rubber stamp."""
    S = 300
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([14, 14, S - 14, S - 14], fill=MAGENTA + (255,),
               outline=(10, 10, 14, 255), width=7)
    ld.ellipse([28, 28, S - 28, S - 28], outline=(255, 255, 255, 220), width=3)
    # ghost drawn directly on the layer: white body on magenta, black
    # outline, sparkle eyes, raised arm holding its star coin
    draw_ghost(ld, S // 2, S // 2 + 6, 150)
    ld.ellipse([14, 14, S - 14, S - 14], outline=(10, 10, 14, 255), width=7)
    ld.ellipse([28, 28, S - 28, S - 28], outline=(255, 255, 255, 220), width=3)
    layer = layer.rotate(-12, resample=Image.BICUBIC, expand=False)
    return layer.resize((size, size), Image.LANCZOS)


def dashed_box(d, x0, y0, x1, y1, color=RED, w=3, dash=22, gap=12):
    x = x0
    while x < x1:
        d.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=w)
        d.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=w)
        x += dash + gap
    y = y0
    while y < y1:
        d.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=w)
        d.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=w)
        y += dash + gap


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- paper sheet with a soft drop shadow ----
    d.rectangle([92, 58, 1004, 1036], fill=(90, 105, 114))
    d.rectangle([80, 46, 992, 1024], fill=PAPER)
    d.rectangle([100, 66, 972, 1004], outline=INK, width=3)
    d.rectangle([110, 76, 962, 994], outline=(200, 200, 200), width=1)

    # ---- letterhead ----
    draw_cross(d, 132, 100, 88)
    d.text((246, 104), "VICE CITY GENERAL", font=f_bold(52), fill=INK)
    d.text((246, 162), "HOSPITAL  •  LEONIDA COUNTY  •  EST. 2013",
           font=f_bold(26), fill=RED)
    d.line([(132, 212), (940, 212)], fill=RED, width=4)

    # ---- title ----
    text_fit(d, "DOCTOR'S NOTE", 536, 232, 88, 820)
    d.text((536, 330), "MEDICAL EXCUSE — PLEASE EXCUSE THIS PATIENT FROM:",
           font=f_bold(26), fill=GRAY, anchor="ma")

    # ---- patient fields (5 rows x 48 px, values end well before x=940) ----
    fields = [
        ("PATIENT:", "YOU (EVERY GTA FAN)"),
        ("DATE:", "MAY 26, 2026"),
        ("DIAGNOSIS:", "VICE CITY FEVER"),
        ("SYMPTOMS:", "13-YEAR WAIT • 200 GB"),
        ("", "DOWNLOAD • $70 LIGHTER"),
    ]
    y = 380
    for label, value in fields:
        if label:
            d.text((132, y), label, font=f_bold(36), fill=RED)
        d.text((392, y), value, font=f_bold(36), fill=INK)
        y += 48

    # ---- body (3 lines, ends well above the Rx box) ----
    body = ("This patient is excused from work on account of acute "
            "GTA VI launch-day fever. Expected recovery: NEVER.")
    bf = f_serif(35)
    lines = wrap(d, body, bf, 808)
    y = 640
    for line in lines:
        d.text((132, y), line, font=bf, fill=INK)
        y += 44

    # ---- prescription box (text ends by x~700: the seal owns the right) ----
    dashed_box(d, 132, 796, 940, 884)
    d.text((152, 806), "Rx:", font=f_bold(34), fill=RED)
    d.text((232, 806), "1 × GRAND THEFT AUTO VI", font=f_bold(34), fill=INK)
    d.text((152, 848), "Take immediately. No refills.",
           font=f_bold(30), fill=INK)

    # ---- footer band: the pitch, in the document's own voice ----
    # (drawn BEFORE the seal, so the seal sits on top of it)
    d.rectangle([80, 958, 992, 1024], fill=MAGENTA)
    d.text((520, 968), "MY AGENT GOT PAID ON make.fun",
           font=f_bold(32), fill=PAPER, anchor="ma")

    # ---- signature (left) + official seal (right, overlapping the
    # prescription box's empty corner like a rubber stamp) ----
    d.text((132, 898), "Dr. Ghost, MD", font=f_script(46), fill=INK)
    d.text((470, 914), "make.fun Medical", font=f_bold(24), fill=GRAY)
    seal = draw_seal(220)
    img.paste(seal, (745, 765), seal)

    img.save("meme-v3.png")
    img.resize((480, 480), Image.LANCZOS).save("meme-v3-480.png")
    print("saved meme-v3.png + meme-v3-480.png")


if __name__ == "__main__":
    main()
