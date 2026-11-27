#!/usr/bin/env python3
"""Render entry.png for the news-image-20261126 bounty.

A one-page broadsheet that sums up the world news of Thursday 26 November
2026 in six illustrated panels. Everything is drawn from scratch with Pillow
primitives -- no photographs, no copied artwork, no network. Run it with:

    python3 draw.py

It writes entry.png (1024x1024) next to this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (250, 246, 236)
INK = (26, 26, 24)
TEAL = (13, 59, 70)
AMBER = (214, 164, 41)
RUST = (178, 58, 32)
SLATE = (96, 98, 94)
CARD = (255, 255, 255)
EDGE = (206, 198, 178)
EMBER = (232, 126, 26)
SOFT = (238, 233, 219)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, fnt, width):
    """Split text into lines no wider than width (greedy, word by word)."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, lines, fnt, colour, gap):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=colour)
        y += gap
    return y


def star(d, cx, cy, r, colour):
    pts = []
    for i in range(16):
        a = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=colour)


def pic_missile(d, cx, cy, s, col):
    """A tower block hit by a falling missile, with a blast star."""
    d.rectangle([cx - s * 0.55, cy - s * 0.35, cx - s * 0.05, cy + s * 0.7],
                fill=col)
    d.rectangle([cx + s * 0.1, cy - s * 0.05, cx + s * 0.6, cy + s * 0.7],
                fill=col)
    for wy in (-0.15, 0.15, 0.45):
        d.rectangle([cx - s * 0.45, cy + s * wy, cx - s * 0.15, cy + s * wy + 6],
                    fill=PAPER)
        d.rectangle([cx + s * 0.2, cy + s * wy, cx + s * 0.5, cy + s * wy + 6],
                    fill=PAPER)
    d.polygon([(cx + s * 0.75, cy - s * 1.05), (cx + s * 0.95, cy - s * 0.55),
               (cx + s * 0.55, cy - s * 0.55)], fill=col)
    d.line([(cx + s * 0.75, cy - s * 0.55), (cx + s * 0.55, cy - s * 0.1)],
           fill=EMBER, width=4)
    star(d, cx + s * 0.45, cy - s * 0.85, s * 0.34, EMBER)


def pic_refinery(d, cx, cy, s, col):
    """Refinery towers with a flame licking from the tallest stack."""
    d.rectangle([cx - s * 0.9, cy - s * 0.35, cx - s * 0.5, cy + s * 0.65],
                fill=col)
    d.rectangle([cx - s * 0.38, cy - s * 0.7, cx + s * 0.02, cy + s * 0.65],
                fill=col)
    d.rectangle([cx + s * 0.14, cy - s * 0.15, cx + s * 0.54, cy + s * 0.65],
                fill=col)
    d.polygon([(cx - s * 0.18, cy - s * 1.2), (cx + s * 0.18, cy - s * 1.2),
               (cx + s * 0.34, cy - s * 0.7), (cx - s * 0.34, cy - s * 0.7)],
              fill=EMBER)
    d.ellipse([cx + s * 0.55, cy - s * 1.05, cx + s * 0.95, cy - s * 0.65],
              fill=INK)
    d.line([(cx - s * 0.9, cy + s * 0.25), (cx + s * 0.9, cy + s * 0.25)],
           fill=col, width=4)


def pic_mine(d, cx, cy, s, col):
    """A mine shaft flooded with water, helmet and lamp above."""
    d.rectangle([cx - s * 0.5, cy - s * 0.7, cx + s * 0.5, cy + s * 0.7],
                outline=col, width=5)
    d.rectangle([cx - s * 0.5, cy + s * 0.1, cx + s * 0.5, cy + s * 0.7],
                fill=(52, 110, 138))
    for k in range(3):
        x = cx - s * 0.4 + k * s * 0.4
        d.line([(x, cy + s * 0.3), (x + s * 0.2, cy + s * 0.3)],
               fill=(255, 255, 255), width=3)
    d.arc([cx - s * 0.42, cy - s * 1.15, cx + s * 0.42, cy - s * 0.35],
          180, 360, fill=col, width=6)
    d.rectangle([cx - s * 0.06, cy - s * 1.28, cx + s * 0.06, cy - s * 1.05],
                fill=AMBER)


def pic_falling(d, cx, cy, s, col):
    """A falling arrow over shrinking bars: migration at a 29-year low."""
    for i, h in enumerate([1.0, 0.68, 0.38]):
        x = cx - s * 0.95 + i * s * 0.62
        d.rectangle([x, cy + s * 0.55 - h * s, x + s * 0.42, cy + s * 0.55],
                    fill=col)
    d.line([(cx - s * 1.0, cy - s * 0.55), (cx + s * 0.2, cy - s * 0.15),
            (cx + s * 0.95, cy - s * 0.75)], fill=RUST, width=5)
    d.polygon([(cx + s * 0.95, cy - s * 0.75), (cx + s * 0.62, cy - s * 0.72),
               (cx + s * 0.82, cy - s * 0.42)], fill=RUST)
    d.line([(cx - s * 1.05, cy + s * 0.55), (cx + s * 1.05, cy + s * 0.55)],
           fill=INK, width=4)


def pic_balloon(d, cx, cy, s, col):
    """A parade balloon tugged by the wind, rain slanting across."""
    d.ellipse([cx - s * 0.75, cy - s * 0.95, cx + s * 0.75, cy - s * 0.05],
              fill=col)
    d.polygon([(cx - s * 0.15, cy - s * 0.05), (cx + s * 0.15, cy - s * 0.05),
               (cx, cy + s * 0.4)], fill=col)
    d.line([(cx, cy + s * 0.4), (cx - s * 0.3, cy + s * 0.75)], fill=INK,
           width=3)
    d.line([(cx, cy + s * 0.4), (cx + s * 0.3, cy + s * 0.75)], fill=INK,
           width=3)
    for k in range(3):
        x = cx - s * 0.9 + k * s * 0.55
        d.line([(x, cy - s * 0.5), (x - s * 0.2, cy - s * 0.1)],
               fill=(52, 110, 138), width=3)


def pic_rubble(d, cx, cy, s, col):
    """A damaged building front with smoke rising over rubble."""
    d.polygon([(cx - s * 0.7, cy + s * 0.65), (cx - s * 0.7, cy - s * 0.35),
               (cx - s * 0.2, cy - s * 0.7), (cx + s * 0.3, cy - s * 0.45),
               (cx + s * 0.7, cy - s * 0.65), (cx + s * 0.7, cy + s * 0.65)],
              fill=col)
    d.rectangle([cx - s * 0.45, cy - s * 0.1, cx - s * 0.15, cy + s * 0.2],
                fill=PAPER)
    d.rectangle([cx + s * 0.15, cy + s * 0.05, cx + s * 0.45, cy + s * 0.35],
                fill=PAPER)
    d.ellipse([cx - s * 0.1, cy - s * 1.15, cx + s * 0.35, cy - s * 0.7],
              fill=SLATE)
    d.ellipse([cx + s * 0.3, cy - s * 1.0, cx + s * 0.7, cy - s * 0.6],
              fill=SLATE)
    d.line([(cx - s * 0.9, cy + s * 0.65), (cx + s * 0.9, cy + s * 0.65)],
           fill=INK, width=4)


ART = [pic_missile, pic_refinery, pic_mine, pic_falling, pic_balloon,
       pic_rubble]

PANELS = [
    ("KYIV  ·  UKRAINE", "Missiles hit Kyiv mall",
     "Russia strikes Kyiv with ballistic missiles overnight, hitting a "
     "shopping centre and two other buildings; seven people are wounded.",
     (150, 52, 40)),
    ("BANGKOK  ·  THAILAND", "Blast at Bangkok refinery",
     "An explosion and fire at the Bangchak oil refinery injures at least "
     "seven workers and sends a column of smoke over the city.",
     (178, 58, 32)),
    ("BOGOR  ·  INDONESIA", "Flooded mine kills 13",
     "Floodwater swamps an illegal gold mine in Bogor, West Java; 13 miners "
     "are confirmed dead and 13 more are trapped underground.",
     (34, 84, 96)),
    ("UNITED KINGDOM", "Migration at 29-year low",
     "UK net migration falls to 77,000 in the year to June, the lowest "
     "since 1997, the Office for National Statistics reports.",
     (38, 96, 66)),
    ("UNITED STATES", "Parade halted by storm",
     "The Macy's Thanksgiving Day Parade is postponed by a nor'easter, "
     "the first postponement in its 100-year history; it moves to Saturday.",
     (88, 96, 44)),
    ("GAZA", "Nine killed in Gaza strikes",
     "Israeli strikes on Deir al-Balah kill nine Palestinians, the third "
     "straight night of attacks despite a year-old ceasefire.",
     (96, 72, 96)),
]

ALSO = ("Also: EU leaders clash over a \u20ac45bn loan for Ukraine  \u00b7  "
        "US proposes tariffs on 14 trading partners  \u00b7  "
        "Houthis claim a strike on Saudi Arabia's Ras Tanura refinery  \u00b7  "
        "SpaceX cleared to launch up to a million Starmind satellites")


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, PAGE_W, 112], fill=TEAL)
    d.text((512, 22), "THE WORLD IN ONE DAY", font=F(SERIF, 50),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 80), "THURSDAY  \u00b7  26 NOVEMBER 2026", font=F(BOLD, 20),
           fill=AMBER, anchor="ma")
    d.line([(0, 112), (PAGE_W, 112)], fill=AMBER, width=3)

    d.text((512, 130),
           "Six stories that defined the day \u2014 from Kyiv to Gaza",
           font=F(PLAIN, 19), fill=INK, anchor="ma")
    d.line([(24, 160), (PAGE_W - 24, 160)], fill=EDGE, width=2)

    mx, gx, gy = 24, 16, 16
    top, ph = 176, 352
    pw = (PAGE_W - 2 * mx - 2 * gx) // 3
    for i, (kick, head, summ, accent) in enumerate(PANELS):
        c, r = i % 3, i // 3
        x0 = mx + c * (pw + gx)
        y0 = top + r * (ph + gy)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=EDGE, width=2)
        d.rectangle([x0, y0, x1, y0 + 8], fill=accent)
        ix, iy = x0 + pw // 2, y0 + 92
        d.ellipse([ix - 56, iy - 56, ix + 56, iy + 56], fill=SOFT)
        ART[i](d, ix, iy, 36, accent)
        d.text((x0 + pw // 2, y0 + 168), kick, font=F(BOLD, 14),
               fill=accent, anchor="ma")
        hl = fit(d, head, F(BOLD, 23), pw - 28)
        para(d, x0 + 14, y0 + 192, hl[:2], F(BOLD, 23), INK, 28)
        sl = fit(d, summ, F(PLAIN, 15), pw - 28)
        para(d, x0 + 14, y0 + 256, sl[:4], F(PLAIN, 15), (62, 60, 54), 20)

    fy = top + 2 * ph + gy + 16
    d.line([(24, fy), (PAGE_W - 24, fy)], fill=EDGE, width=2)
    al = fit(d, ALSO, F(BOLD, 15), PAGE_W - 48)
    para(d, 24, fy + 10, al, F(BOLD, 15), INK, 20)
    d.text((512, PAGE_H - 22),
           "Drawn from wire reports of 26 November 2026  \u00b7  Reuters  \u00b7  AP",
           font=F(PLAIN, 13), fill=SLATE, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
