#!/usr/bin/env python3
"""Render the 23 November 2026 world-news image (1024x1024 PNG) with PIL.

Run:  python3 draw.py  ->  entry.png  (check size <= 1 MiB).
The image is drawn with DejaVu (a free font) at large sizes so it stays
readable when the judge views it at ~300 px wide. Layout: navy masthead
with a globe, one lead story, five cards, navy footer.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (250, 248, 242)          # paper
INK = (22, 26, 34)
BODY = (52, 58, 68)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
TEAL = (13, 110, 110)
GOLD = (176, 124, 20)
YELLOW = (255, 214, 90)
SOFT = (210, 218, 230)
GREY = (200, 196, 186)
WHITE = (255, 255, 255)


def font(size, bold=False, serif=False):
    if serif:
        name = "LiberationSerif-Bold.ttf" if bold else "LiberationSerif-Regular.ttf"
        return ImageFont.truetype("/usr/share/fonts/truetype/liberation/" + name, size)
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((48, 24), "THE WORLD IN ONE PICTURE", font=font(48, True, serif=True), fill=WHITE)
d.text((48, 88), "MONDAY, 23 NOVEMBER 2026", font=font(30, True), fill=YELLOW)
d.text((48, 122), "SIX STORIES  •  ONE DAY", font=font(19, True), fill=SOFT)
# globe, right of masthead
cx, cy, r = 918, 74, 52
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=YELLOW, width=4)
d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=WHITE, width=3)
d.line([cx - r + 6, cy - r // 2, cx + r - 6, cy - r // 2], fill=WHITE, width=3)
d.line([cx - r + 2, cy, cx + r - 2, cy], fill=WHITE, width=3)
d.line([cx - r + 6, cy + r // 2, cx + r - 6, cy + r // 2], fill=WHITE, width=3)
d.rectangle([0, 148, W, 154], fill=RED)

# ---- lead story: COP31 ----
y = 170
d.rectangle([36, y, 988, y + 240], fill=WHITE, outline=GREY, width=2)
d.rectangle([36, y, 252, y + 34], fill=RED)
d.text((48, y + 4), "CLIMATE  •  LEAD", font=font(20, True), fill=WHITE)
d.text((48, y + 46), "COP31 climate summit ends", font=font(42, True, serif=True), fill=INK)
d.text((48, y + 94), "with no deal in Antalya", font=font(42, True, serif=True), fill=INK)
lead = ("The UN climate talks in Antalya, Turkey, collapsed after the EU and "
        "about 130 other parties rejected a draft text that left out fossil fuels.")
for i, ln in enumerate(wrap(d, lead, font(24), 920)):
    d.text((48, y + 152 + i * 31), ln, font=font(24), fill=BODY)

stories = [
    ("WAR  •  UKRAINE", RED, "Russian strike kills 10 near Kyiv",
     "A Russian strike on Dymer, north of Kyiv, killed at least 10 people."),
    ("MARKETS  •  ASIA", GOLD, "AI sell-off hits world markets",
     "Nikkei falls 5.06% and the S&P 500 3.7% as AI shares sell off."),
    ("MIDDLE EAST", TEAL, "Tankers ablaze near Hormuz",
     "Two tankers struck near Hormuz; Trump threatens Iranian vessels."),
    ("JUSTICE  •  MEXICO", NAVY, "'El Chapo Isidro' captured",
     "Mexico seizes FBI most-wanted cartel boss Isidro Meza-Flores."),
    ("SPORT  •  MOTOGP", TEAL, "Marquez wins eighth title",
     "Marc Marquez seals his eighth MotoGP title at Portimao."),
]

# ---- four stories: 2 cols x 2 rows ----
y0, ch, gap = 424, 168, 12
for i, (tag, color, head, body) in enumerate(stories[:4]):
    bx, bw = 36 + (i % 2) * (466 + 20), 466
    by = y0 + (i // 2) * (ch + gap)
    d.rectangle([bx, by, bx + bw, by + ch], fill=WHITE, outline=GREY, width=2)
    d.rectangle([bx, by, bx + bw, by + 32], fill=color)
    d.text((bx + 12, by + 5), tag, font=font(18, True), fill=WHITE)
    head_lines = wrap(d, head, font(28, True, serif=True), bw - 24)
    for j, ln in enumerate(head_lines):
        d.text((bx + 12, by + 44 + j * 34), ln, font=font(28, True, serif=True), fill=INK)
    body_y = by + 44 + len(head_lines) * 34 + 8
    for j, ln in enumerate(wrap(d, body, font(21), bw - 24)):
        d.text((bx + 12, body_y + j * 27), ln, font=font(21), fill=BODY)

# ---- bottom band: MotoGP card + "the day in numbers" panel ----
by, bh = 784, 188
tag, color, head, body = stories[4]
bx, bw = 36, 466
d.rectangle([bx, by, bx + bw, by + bh], fill=WHITE, outline=GREY, width=2)
d.rectangle([bx, by, bx + bw, by + 32], fill=color)
d.text((bx + 12, by + 5), tag, font=font(18, True), fill=WHITE)
head_lines = wrap(d, head, font(28, True, serif=True), bw - 24)
for j, ln in enumerate(head_lines):
    d.text((bx + 12, by + 44 + j * 34), ln, font=font(28, True, serif=True), fill=INK)
body_y = by + 44 + len(head_lines) * 34 + 8
for j, ln in enumerate(wrap(d, body, font(21), bw - 24)):
    d.text((bx + 12, body_y + j * 27), ln, font=font(21), fill=BODY)

px, pw = 522, 466
d.rectangle([px, by, px + pw, by + bh], fill=NAVY)
d.text((px + 16, by + 12), "THE DAY IN NUMBERS", font=font(18, True), fill=YELLOW)
stats = [("5.06%", "NIKKEI FALL"), ("3.7%", "S&P 500 FALL"),
         ("$5M", "BOUNTY ON CARTEL BOSS"), ("8TH", "MOTOGP TITLE")]
for k, (num, label) in enumerate(stats):
    sx = px + 16 + (k % 2) * 233
    sy = by + 52 + (k // 2) * 68
    d.text((sx, sy), num, font=font(34, True, serif=True), fill=WHITE)
    d.text((sx, sy + 42), label, font=font(14, True), fill=SOFT)

# ---- footer ----
d.rectangle([0, 984, W, H], fill=NAVY)
d.text((36, 993), "23 NOVEMBER 2026  •  SIX STORIES FROM AROUND THE WORLD.",
       font=font(20), fill=SOFT)

img.save("entry.png", optimize=True)
print("saved entry.png")
