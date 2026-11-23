#!/usr/bin/env python3
"""make.fun entry: Sum up 23 November's world news in one image.

A program that draws a newspaper-style front page (1024x1024 PNG) with only
the Python standard library: a hand-written 5x7 bitmap font and a small PNG
encoder (zlib + struct). No network, no third-party packages, no timestamps,
so two runs write byte-identical files.

Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The grader runs it with /output as the output directory.
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- font -----
# 5x7 bitmap font, '#' = ink, '.' = paper. Uppercase, digits, punctuation.
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    "%": ["#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"],
    "$": ["..#..", ".####", "#.#.#", ".###.", "..#.#", "####.", "..#.."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "&": [".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"],
}

# ---------------------------------------------------------------- canvas ---
W, H = 1024, 1024
PAPER = (250, 248, 242)
INK = (22, 26, 34)
BODY = (52, 58, 68)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
TEAL = (13, 110, 110)
GOLD = (176, 124, 20)
YELLOW = (255, 214, 90)
WHITE = (255, 255, 255)
GREY = (200, 196, 186)
SOFT = (210, 218, 230)


class Canvas:
    def __init__(self):
        self.px = bytearray(PAPER * W * H)

    def rect(self, x, y, w, h, color):
        r, g, b = color
        for yy in range(max(0, y), min(H, y + h)):
            base = (yy * W + max(0, x)) * 3
            for xx in range(max(0, x), min(W, x + w)):
                i = (yy * W + xx) * 3
                self.px[i] = r
                self.px[i + 1] = g
                self.px[i + 2] = b

    def text(self, x, y, s, scale, color):
        for ci, ch in enumerate(s.upper()):
            glyph = FONT.get(ch, FONT[" "])
            ox = x + ci * 6 * scale
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "#":
                        self.rect(ox + col * scale, y + row * scale,
                                  scale, scale, color)

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r - 1, cy + r + 2):
            for xx in range(cx - r - 1, cx + r + 2):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if abs(d - r) <= 1.6:
                    self.rect(xx, yy, 2, 2, color)

    def chord(self, cx, cy, r, dy, color):
        half = int((r * r - dy * dy) ** 0.5)
        self.rect(cx - half, cy + dy - 1, half * 2, 2, color)

    def meridian(self, cx, cy, r, color):
        for dy in range(-r, r + 1, 2):
            half = int((r * r - dy * dy) ** 0.5) // 3
            self.rect(cx - half, cy + dy, half * 2, 2, color)

    def wrap(self, s, scale, max_w):
        lines, cur = [], ""
        for word in s.split():
            trial = (cur + " " + word).strip()
            if self.text_w(trial, scale) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def png_bytes(canvas):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter: none
        raw += canvas.px[y * stride:(y + 1) * stride]

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
            + chunk(b"IEND", b""))


# ------------------------------------------------------------------ page ---
def draw():
    c = Canvas()
    # Masthead
    c.rect(0, 0, W, 140, NAVY)
    c.text(48, 22, "THE WORLD IN ONE PICTURE", 5, WHITE)
    c.text(48, 72, "MONDAY, 23 NOVEMBER 2026", 5, YELLOW)
    c.text(48, 112, "SIX STORIES - ONE DAY", 2, SOFT)
    # small globe, right of masthead
    c.circle(918, 70, 44, YELLOW)
    c.chord(918, 70, 44, -22, WHITE)
    c.chord(918, 70, 44, 0, WHITE)
    c.chord(918, 70, 44, 22, WHITE)
    c.meridian(918, 70, 44, WHITE)
    c.rect(0, 140, W, 6, RED)

    # Lead story: COP31
    y = 156
    c.rect(36, y, 952, 232, WHITE)
    c.rect(36, y, 952, 232, WHITE)
    # border
    c.rect(36, y, 952, 2, GREY)
    c.rect(36, y + 230, 952, 2, GREY)
    c.rect(36, y, 2, 232, GREY)
    c.rect(986, y, 2, 232, GREY)
    c.rect(36, y, 280, 34, RED)
    c.text(48, y + 7, "CLIMATE - LEAD", 3, WHITE)
    c.text(48, y + 46, "COP31 CLIMATE SUMMIT ENDS", 6, INK)
    c.text(48, y + 92, "WITH NO DEAL IN ANTALYA", 6, INK)
    lead = ("THE UN CLIMATE TALKS IN ANTALYA, TURKEY, COLLAPSED AFTER THE EU AND "
            "ABOUT 130 OTHER PARTIES REJECTED A DRAFT TEXT THAT LEFT OUT FOSSIL FUELS.")
    for i, ln in enumerate(c.wrap(lead, 3, 920)):
        c.text(48, y + 148 + i * 23, ln, 3, BODY)

    # Grid stories
    stories = [
        ("WAR - UKRAINE", RED, "RUSSIAN STRIKE KILLS 10",
         "RUSSIAN STRIKE ON DYMER, NORTH OF KYIV, KILLS AT LEAST 10 PEOPLE."),
        ("MARKETS - ASIA", GOLD, "AI SELL-OFF HITS MARKETS",
         "NIKKEI FALLS 5.06% AND THE S&P 500 3.7% AS AI SHARES SELL OFF."),
        ("MIDDLE EAST", TEAL, "TANKERS ABLAZE NEAR HORMUZ",
         "TWO TANKERS STRUCK NEAR HORMUZ, TRUMP THREATENS IRANIAN VESSELS."),
        ("JUSTICE - MEXICO", NAVY, "EL CHAPO ISIDRO CAPTURED",
         "MEXICO SEIZES FBI MOST-WANTED CARTEL BOSS ISIDRO MEZA-FLORES."),
        ("SPORT - MOTOGP", TEAL, "MARQUEZ WINS EIGHTH TITLE",
         "MARC MARQUEZ SEALS HIS EIGHTH MOTOGP TITLE AT PORTIMAO."),
    ]
    y0, ch, gap = 400, 186, 12
    for i, (tag, color, head, body) in enumerate(stories):
        if i == 4:
            cx, cw = 36, 952
        else:
            cx, cw = 36 + (i % 2) * (466 + 20), 466
        cy = y0 + (i // 2) * (ch + gap)
        c.rect(cx, cy, cw, ch, WHITE)
        c.rect(cx, cy, cw, 2, GREY)
        c.rect(cx, cy + ch - 2, cw, 2, GREY)
        c.rect(cx, cy, 2, ch, GREY)
        c.rect(cx + cw - 2, cy, 2, ch, GREY)
        c.rect(cx, cy, cw, 30, color)
        c.text(cx + 12, cy + 6, tag, 3, WHITE)
        head_lines = c.wrap(head, 4, cw - 24)
        for j, ln in enumerate(head_lines):
            c.text(cx + 12, cy + 40 + j * 30, ln, 4, INK)
        body_y = cy + 40 + len(head_lines) * 30 + 12
        for j, ln in enumerate(c.wrap(body, 3, cw - 24)):
            c.text(cx + 12, body_y + j * 23, ln, 3, BODY)

    # Footer
    c.rect(0, 990, W, 34, NAVY)
    c.text(36, 999, "23 NOVEMBER 2026 - SIX STORIES FROM AROUND THE WORLD.",
           3, SOFT)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(draw())
    assert len(data) <= 1048576, "image over 1 MiB"
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
