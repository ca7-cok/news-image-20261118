#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic (1024x1024 PNG).

Deterministic: no randomness, no time, no network, fixed fonts.
Run: python3 render.py  -> writes entry.png next to this file.

Stories (all verified 2026-11-19 from multiple wire sources; each happened
or was first reported on 18 November 2026):
  LEAD  Iran hits U.S. bases in Kuwait & Bahrain (Reuters/AP/The Hindu/CNA)
  1     Peltola wins Alaska; Democrats take Senate 56-44 (AP/Al Jazeera/Reuters)
  2     Xi-Putin meet in Shenzhen ahead of first trilateral with Trump (Reuters/AA)
  3     Quad leaders meet in Manila, first time in 2+ years (AA/Outlook India)
  4     Israel opens new "concentrated operation" in central Gaza (Outlook/Reuters)
  5     U.S. says no sign of "systemic attack" on capital (AA/Reuters)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
NAVY_LIGHT = (36, 52, 88)
RED = (192, 57, 43)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
GOLD = (176, 124, 22)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def starburst(d, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


# ---------- pictograms: each draws inside a 128 x 64 box at (x, y) ----------

def pic_drone(d, x, y):
    """Base + red burst + two drones."""
    cx = x + 64
    # base: low navy bar with two towers
    d.rectangle([x + 8, y + 48, x + 120, y + 62], fill=NAVY)
    d.rectangle([x + 20, y + 34, x + 36, y + 48], fill=NAVY)
    d.rectangle([x + 92, y + 38, x + 106, y + 48], fill=NAVY_LIGHT)
    # red burst above the base
    starburst(d, cx, y + 26, 22, 10, 8, RED)
    # two small drones
    for px, py in ((x + 16, y + 12), (x + 110, y + 8)):
        d.polygon([(px, py - 7), (px - 7, py + 5), (px + 7, py + 5)],
                  fill=INK)
        d.line([px - 10, py - 9, px + 10, py - 9], fill=INK, width=2)


def pic_ballot(d, x, y):
    """Ballot box with a big check."""
    d.rounded_rectangle([x + 38, y + 18, x + 90, y + 58], 4, fill=NAVY)
    d.rectangle([x + 38, y + 18, x + 90, y + 28], fill=NAVY_LIGHT)
    d.rectangle([x + 56, y + 10, x + 72, y + 18], fill=(255, 255, 255),
                outline=NAVY, width=2)
    d.line([x + 46, y + 40, x + 58, y + 52, x + 84, y + 28],
           fill=(255, 255, 255), width=5, joint="curve")


def pic_flags(d, x, y):
    """China / Russia / USA mini flags side by side."""
    fw, fh, gap = 38, 26, 5
    total = 3 * fw + 2 * gap
    x0 = x + (128 - total) // 2
    yy = y + (64 - fh) // 2
    # China: red field, one gold star
    d.rectangle([x0, yy, x0 + fw, yy + fh], fill=(222, 41, 16))
    starburst(d, x0 + 11, yy + 10, 7, 3, 5, (255, 222, 0))
    # Russia: white / blue / red stripes
    x1 = x0 + fw + gap
    d.rectangle([x1, yy, x1 + fw, yy + 9], fill=(255, 255, 255),
                outline=NAVY)
    d.rectangle([x1, yy + 9, x1 + fw, yy + 17], fill=(0, 57, 166))
    d.rectangle([x1, yy + 17, x1 + fw, yy + fh], fill=(213, 0, 50))
    # USA: stripes + blue canton
    x2 = x1 + fw + gap
    for i in range(6):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x2, yy + i * 4, x2 + fw, yy + (i + 1) * 4 + 1],
                    fill=col)
    d.rectangle([x2, yy, x2 + 16, yy + 13], fill=(60, 59, 110))
    for sx in (4, 10):
        for sy in (4, 10):
            d.ellipse([x2 + sx - 1, yy + sy - 1, x2 + sx + 1, yy + sy + 1],
                      fill=(255, 255, 255))


def pic_quad(d, x, y):
    """Four dots in a diamond, linked, over a globe circle."""
    cx, cy = x + 64, y + 32
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], outline=NAVY, width=3)
    d.line([cx - 28, cy, cx + 28, cy], fill=NAVY, width=2)
    pts = [(cx, cy - 25), (cx + 25, cy), (cx, cy + 25), (cx - 25, cy)]
    for i in range(4):
        d.line([pts[i], pts[(i + 1) % 4]], fill=RED, width=2)
    for px, py in pts:
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=NAVY)


def pic_gaza(d, x, y):
    """Skyline of three blocks with a red arrow above."""
    base = y + 60
    d.rectangle([x + 30, base - 24, x + 52, base], fill=NAVY)
    d.rectangle([x + 56, base - 36, x + 78, base], fill=NAVY_LIGHT)
    d.rectangle([x + 82, base - 18, x + 100, base], fill=NAVY)
    d.line([x + 22, y + 10, x + 102, y + 10], fill=RED, width=4)
    d.polygon([(x + 102, y + 2), (x + 102, y + 18), (x + 114, y + 10)],
              fill=RED)


def pic_shield(d, x, y):
    """Shield outline with a check."""
    cx = x + 64
    d.polygon([(cx - 26, y + 6), (cx + 26, y + 6), (cx + 26, y + 34),
               (cx, y + 58), (cx - 26, y + 34)], outline=NAVY, width=4)
    d.line([cx - 13, y + 30, cx - 4, y + 40, cx + 16, y + 20],
           fill=RED, width=5, joint="curve")


# ---------- layout ----------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin

    # header band
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 124], fill=RED)
    f_kick = font(BOLD, 24)
    draw_centered(d, W // 2, 20, "T H E   W O R L D   I N   O N E   P I C T U R E",
                  f_kick, (200, 205, 220))
    f_date = font(BOLD, 54)
    draw_centered(d, W // 2, 52, "WEDNESDAY 18 NOVEMBER 2026", f_date,
                  (255, 255, 255))

    # lead panel
    lx, ly, lw, lh = M, 140, W - 2 * M, 232
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], 10, fill=CARD)
    d.rectangle([lx, ly + 10, lx + 10, ly + lh - 10], fill=RED)
    # lead pictogram: bigger drone scene in a 170 x 150 box
    bx, by = lx + 30, ly + 44
    d.rectangle([bx + 8, by + 108, bx + 162, by + 138], fill=NAVY)
    d.rectangle([bx + 24, by + 84, bx + 48, by + 108], fill=NAVY)
    d.rectangle([bx + 118, by + 92, bx + 140, by + 108], fill=NAVY_LIGHT)
    starburst(d, bx + 85, by + 58, 44, 20, 8, RED)
    for px, py in ((bx + 18, by + 22), (bx + 148, by + 14)):
        d.polygon([(px, py - 12), (px - 12, py + 9), (px + 12, py + 9)],
                  fill=INK)
        d.line([px - 17, py - 15, px + 17, py - 15], fill=INK, width=3)
    tx = lx + 224
    tw = lx + lw - 24 - tx
    f_lk = font(BOLD, 22)
    d.text((tx, ly + 18), "THE WAR WIDENS", font=f_lk, fill=RED)
    f_lh = font(BOLD, 40)
    lines = wrap(d, "IRAN HITS U.S. BASES IN KUWAIT & BAHRAIN", f_lh, tw)
    yy = ly + 48
    for ln in lines:
        d.text((tx, yy), ln, font=f_lh, fill=INK)
        yy += 48
    f_lb = font(REG, 22)
    blines = wrap(
        d,
        "Tehran's drones target Patriot batteries at Ali Al Salem; Bahrain "
        "fends off a third attack in a week \u2014 after U.S. jets hit "
        "Qeshm Island.",
        f_lb, tw)
    yy += 6
    for ln in blines:
        d.text((tx, yy), ln, font=f_lb, fill=MUTED)
        yy += 29

    # grid panels
    panels = [
        ("DEMOCRATS TAKE THE SENATE 56\u201344",
         "Peltola flips Alaska \u2014 the last race called, a ninth flip "
         "since 1958.", pic_ballot),
        ("XI\u2013PUTIN MEET AHEAD OF TRUMP",
         "Shenzhen hosts the first Xi\u2013Trump\u2013Putin trilateral on "
         "Thursday.", pic_flags),
        ("QUAD LEADERS MEET IN MANILA",
         "First leaders' meeting in over two years; U.S.\u2013Philippines "
         "trade deal signed.", pic_quad),
        ("ISRAEL OPENS NEW GAZA OPERATION",
         "Army begins a \u201cconcentrated operation\u201d in three areas "
         "of central Gaza; a peace board faults both sides.", pic_gaza),
        ("NO SIGN OF \u201cSYSTEMIC ATTACK,\u201d U.S. SAYS",
         "Rubio: no evidence links the Microsoft, FAA and bank outages "
         "\u2014 or points to cyberattacks.", pic_shield),
    ]
    pw3, ph = 304, 232
    xs3 = [M, M + pw3 + 24, M + 2 * (pw3 + 24)]
    y1, y2 = 388, 636
    pw2 = 472
    xs2 = [M, M + pw2 + 24]
    positions = [(xs3[0], y1, pw3), (xs3[1], y1, pw3), (xs3[2], y1, pw3),
                 (xs2[0], y2, pw2), (xs2[1], y2, pw2)]
    f_ph = font(BOLD, 25)
    f_pb = font(REG, 18)
    for (head, body, pic), (px, py, pw) in zip(panels, positions):
        d.rounded_rectangle([px, py, px + pw, py + ph], 10, fill=CARD)
        d.rectangle([px + 12, py, px + pw - 12, py + 5], fill=NAVY)
        pic(d, px + (pw - 128) // 2, py + 12)
        hlines = wrap(d, head, f_ph, pw - 32)
        yy = py + 88
        for ln in hlines[:2]:
            d.text((px + 16, yy), ln, font=f_ph, fill=INK)
            yy += 29
        blines = wrap(d, body, f_pb, pw - 32)
        yy += 4
        for ln in blines[:3]:
            d.text((px + 16, yy), ln, font=f_pb, fill=MUTED)
            yy += 22

    # also-today strip (auto-fit: shrink until it fits the band)
    sy = 884
    d.rounded_rectangle([M, sy, W - M, sy + 50], 8, fill=NAVY)
    f_at = font(BOLD, 18)
    d.text((M + 18, sy + 14), "ALSO TODAY", font=f_at, fill=(255, 214, 90))
    strip = ("UK sanctions West Bank firms  \u00b7  Cyclone Akvan nears "
             "Odisha  \u00b7  M6.0 quake in PNG")
    size = 18
    f_atb = font(REG, size)
    avail = W - M - 18 - (M + 150)
    while d.textlength(strip, font=f_atb) > avail and size > 13:
        size -= 1
        f_atb = font(REG, size)
    d.text((M + 150, sy + 14), strip, font=f_atb, fill=(255, 255, 255))

    # footer
    f_ft = font(REG, 17)
    draw_centered(
        d, W // 2, 952,
        "Compiled from wire reports \u00b7 All events happened or were "
        "first reported on 18 November 2026",
        f_ft, MUTED)
    draw_centered(d, W // 2, 978, "18 NOV 2026", font(BOLD, 17), NAVY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
