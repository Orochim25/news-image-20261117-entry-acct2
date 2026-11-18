#!/usr/bin/env python3
"""Render the acct2 news front page for Tuesday 17 November 2026.
Own work, drawn with PIL from the verified facts in the brief."""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = sys.argv[1] if len(sys.argv) > 1 else "entry.png"

FDIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

# --- palette: crimson masthead, warm ivory paper, charcoal ink ---
PAPER_TOP = (250, 246, 232)
PAPER_BOT = (243, 236, 214)
CARD = (255, 253, 246)
CARD_EDGE = (198, 184, 150)
SHADOW = (210, 198, 168)
INK = (26, 24, 22)
SUB = (74, 70, 64)
CRIMSON = (122, 14, 30)
CRIMSON_D = (94, 8, 22)
GOLD = (198, 152, 46)
GOLD_L = (232, 196, 96)
NAVY = (28, 44, 78)
SEA = (214, 230, 240)
LAND = (232, 216, 178)
LAND_EDGE = (176, 152, 110)

KICK = {
    "red": (168, 24, 32), "teal": (12, 110, 108), "blue": (28, 74, 150),
    "plum": (110, 44, 120), "green": (42, 110, 52), "orange": (176, 92, 16),
    "slate": (70, 84, 104), "brown": (122, 84, 40),
}

img = Image.new("RGB", (W, H), PAPER_TOP)
d = ImageDraw.Draw(img)
# soft vertical paper gradient
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(
        int(PAPER_TOP[i] + (PAPER_BOT[i] - PAPER_TOP[i]) * t) for i in range(3)))

def text_w(s, f):
    return d.textlength(s, font=f)

def wrap(s, f, maxw):
    """Greedy word wrap to maxw pixels; returns list of lines."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(s, f, maxw, maxlines):
    """Wrap text; if it exceeds maxlines, shrink font one step at a time."""
    size = f.size
    while size > 8:
        f2 = type(f)(FDIR + f.path.split("/")[-1], size) if hasattr(f, "path") else f
        lines = wrap(s, f2, maxw)
        if len(lines) <= maxlines:
            return lines, f2
        size -= 1
    return wrap(s, f2, maxw)[:maxlines], f2

def card(x, y, w, h, fill=CARD, edge=CARD_EDGE):
    d.rectangle([x + 2, y + 3, x + w + 2, y + h + 3], fill=SHADOW)
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=edge, width=1)

def badge(cx, cy, r, n, fill=CRIMSON, fg=(255, 255, 255)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=2)
    f = SANS_B(r + 2 if r < 12 else r)
    t = str(n)
    d.text((cx - text_w(t, f) / 2, cy - f.size / 2 - 1), t, font=f, fill=fg)

def rule(x, y, w, color=GOLD, width=2):
    d.line([(x, y), (x + w, y)], fill=color, width=width)

def kicker(x, y, label, color):
    f = SANS_B(11)
    d.text((x, y), label, font=f, fill=color)

# --- small icons (drawn, 40x40 box at bx,by) ---
def icon_jet(bx, by, col=(40, 48, 64)):
    d.polygon([(bx + 6, by + 22), (bx + 34, by + 12), (bx + 30, by + 20),
               (bx + 36, by + 24), (bx + 30, by + 26), (bx + 20, by + 28),
               (bx + 12, by + 34), (bx + 10, by + 28), (bx + 4, by + 26)], fill=col)
    d.ellipse([bx + 30, by + 4, bx + 37, by + 11], fill=(168, 24, 32))

def icon_house(bx, by):
    d.polygon([(bx + 6, by + 20), (bx + 20, by + 6), (bx + 34, by + 20)], fill=(122, 84, 40))
    d.rectangle([bx + 10, by + 20, bx + 30, by + 34], fill=(176, 140, 96))
    d.rectangle([bx + 17, by + 24, bx + 23, by + 34], fill=(60, 48, 36))

def icon_chart(bx, by):
    d.rectangle([bx + 6, by + 6, bx + 34, by + 34], outline=(42, 110, 52), width=2)
    d.line([(bx + 9, by + 28), (bx + 16, by + 20), (bx + 22, by + 23), (bx + 31, by + 11)],
           fill=(42, 110, 52), width=3)
    d.polygon([(bx + 27, by + 11), (bx + 33, by + 11), (bx + 31, by + 17)], fill=(42, 110, 52))

def icon_ballot(bx, by):
    d.rectangle([bx + 8, by + 6, bx + 32, by + 34], fill=(110, 44, 120))
    d.rectangle([bx + 12, by + 12, bx + 28, by + 18], fill=(255, 255, 255))
    d.line([(bx + 12, by + 28), (bx + 17, by + 33), (bx + 28, by + 21)],
           fill=(255, 255, 255), width=3)

def icon_scales(bx, by):
    d.line([(bx + 20, by + 6), (bx + 20, by + 32)], fill=(110, 84, 20), width=3)
    d.line([(bx + 8, by + 10), (bx + 32, by + 10)], fill=(110, 84, 20), width=3)
    d.polygon([(bx + 4, by + 18), (bx + 12, by + 18), (bx + 8, by + 26)], fill=(150, 120, 40))
    d.polygon([(bx + 28, by + 18), (bx + 36, by + 18), (bx + 32, by + 26)], fill=(150, 120, 40))

def icon_robot(bx, by):
    d.rectangle([bx + 12, by + 10, bx + 28, by + 30], fill=(70, 84, 104))
    d.rectangle([bx + 8, by + 4, bx + 32, by + 12], fill=(90, 104, 124))
    d.ellipse([bx + 15, by + 14, bx + 19, by + 18], fill=(232, 196, 96))
    d.ellipse([bx + 22, by + 14, bx + 26, by + 18], fill=(232, 196, 96))
    d.line([(bx + 14, by + 24), (bx + 26, by + 24)], fill=(255, 255, 255), width=2)
    d.line([(bx + 12, by + 16), (bx + 6, by + 26)], fill=(70, 84, 104), width=3)
    d.line([(bx + 28, by + 16), (bx + 34, by + 26)], fill=(70, 84, 104), width=3)

def icon_mountain(bx, by):
    d.polygon([(bx + 4, by + 32), (bx + 16, by + 12), (bx + 26, by + 32)], fill=(176, 140, 96))
    d.polygon([(bx + 16, by + 32), (bx + 28, by + 18), (bx + 36, by + 32)], fill=(140, 104, 64))
    d.ellipse([bx + 26, by + 4, bx + 34, by + 12], fill=(232, 196, 96))

def icon_court(bx, by):
    d.polygon([(bx + 6, by + 12), (bx + 20, by + 4), (bx + 34, by + 12)], fill=(122, 96, 40))
    for px in (10, 18, 26):
        d.rectangle([bx + px, by + 14, bx + px + 3, by + 26], fill=(122, 96, 40))
    d.rectangle([bx + 6, by + 28, bx + 34, by + 32], fill=(122, 96, 40))

def icon_shield(bx, by):
    d.polygon([(bx + 20, by + 4), (bx + 32, by + 10), (bx + 32, by + 22),
               (bx + 20, by + 34), (bx + 8, by + 22), (bx + 8, by + 10)], fill=(28, 74, 150))
    d.text((bx + 15, by + 12), "!", font=SANS_B(16), fill=(255, 255, 255))

def icon_chip(bx, by):
    d.rectangle([bx + 10, by + 10, bx + 30, by + 30], fill=(28, 74, 150))
    d.rectangle([bx + 16, by + 16, bx + 24, by + 24], fill=(214, 230, 240))
    for px in (14, 20, 26):
        d.line([(bx + px, by + 4), (bx + px, by + 10)], fill=(28, 74, 150), width=2)
        d.line([(bx + px, by + 30), (bx + px, by + 36)], fill=(28, 74, 150), width=2)

def icon_fence(bx, by):
    for px in (8, 14, 20, 26, 32):
        d.line([(bx + px, by + 6), (bx + px, by + 34)], fill=(70, 84, 104), width=2)
    d.line([(bx + 4, by + 14), (bx + 36, by + 14)], fill=(70, 84, 104), width=2)
    d.line([(bx + 4, by + 26), (bx + 36, by + 26)], fill=(70, 84, 104), width=2)
    d.line([(bx + 10, by + 12), (bx + 30, by + 32)], fill=(168, 24, 32), width=3)
    d.line([(bx + 30, by + 12), (bx + 10, by + 32)], fill=(168, 24, 32), width=3)

def icon_ledger(bx, by):
    d.rectangle([bx + 8, by + 6, bx + 30, by + 34], outline=(122, 14, 30), width=2)
    for i, yy in enumerate((12, 18, 24)):
        d.line([(bx + 12, by + yy), (bx + 26, by + yy)], fill=(122, 14, 30), width=2)
    d.ellipse([bx + 24, by + 24, bx + 36, by + 36], outline=(168, 24, 32), width=2)
    d.line([(bx + 33, by + 33), (bx + 38, by + 38)], fill=(168, 24, 32), width=2)

# ================= MASTHEAD =================
d.rectangle([0, 0, W, 118], fill=CRIMSON)
d.rectangle([0, 0, W, 6], fill=CRIMSON_D)
d.text((14, 12), "THE DAY IN WORLD NEWS", font=SANS_B(13), fill=GOLD_L)
d.text((W - 14 - text_w("22 STORIES \u00b7 4 CONTINENTS \u00b7 ONE DAY", SANS_B(13)), 12),
       "22 STORIES \u00b7 4 CONTINENTS \u00b7 ONE DAY", font=SANS_B(13), fill=(255, 255, 255))
f_date = SERIF_B(52)
d.text((14, 38), "Tuesday 17 November 2026", font=f_date, fill=(255, 255, 255))
# continent legend, bottom-right of the band
legend = [("N. America", (232, 90, 80)), ("Europe", (110, 170, 235)),
          ("Africa", (120, 200, 120)), ("Asia", (232, 196, 96))]
lx = W - 14
ly = 96
for name, col in reversed(legend):
    tw = text_w(name, SANS(11))
    d.ellipse([lx - tw - 14, ly + 2, lx - tw - 6, ly + 10], fill=col)
    d.text((lx - tw, ly), name, font=SANS(11), fill=(255, 255, 255))
    lx -= tw + 26
rule(0, 118, W, GOLD, 4)
d.line([(0, 123), (W, 123)], fill=CRIMSON_D, width=1)

# ================= HERO BANNERS =================
def banner_bridge(x, y, w, h):
    # sky + sea
    for i in range(h):
        t = i / h
        col = tuple(int((196, 214, 228)[j] + ((232, 196, 120)[j] - (196, 214, 228)[j]) * t) for j in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=col)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(36, 84, 128))
    for wx in range(0, w, 26):
        d.arc([x + wx, y + h - 24, x + wx + 24, y + h - 10], 180, 360, fill=(220, 235, 245), width=2)
    # bridge deck with a collapsed middle span
    deck_y = y + h - 52
    d.rectangle([x + 6, deck_y, x + w - 6, deck_y + 7], fill=(90, 88, 84))
    d.line([(x + 6, deck_y), (x + w - 6, deck_y)], fill=(60, 58, 54), width=2)
    # red arch
    d.arc([x + 20, deck_y - 34, x + w - 20, deck_y + 26], 180, 360, fill=(168, 24, 32), width=5)
    # collapsed span: tilted segment falling into the sea
    cx0 = x + w // 2 - 34
    d.polygon([(cx0, deck_y), (cx0 + 30, deck_y + 2), (cx0 + 44, deck_y + 26), (cx0 + 14, deck_y + 24)],
              fill=(110, 106, 100))
    d.rectangle([x + w // 2 - 40, deck_y, x + w // 2 + 40, deck_y + 7], fill=(36, 84, 128))
    # smoke plumes
    for sx, sy, r in ((x + w // 2 - 46, deck_y - 22, 12), (x + w // 2 - 30, deck_y - 36, 15),
                      (x + w // 2 - 12, deck_y - 48, 13), (x + w // 2 + 8, deck_y - 58, 11)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(96, 96, 96))
        d.ellipse([sx - r + 4, sy - r + 4, sx + r - 2, sy + r - 2], fill=(128, 128, 128))
    # explosion burst
    ex, ey = x + w // 2 - 20, deck_y - 8
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        d.line([(ex, ey), (ex + 16 * math.cos(a), ey + 16 * math.sin(a))], fill=(232, 160, 40), width=3)
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(240, 200, 60))

def banner_summit(x, y, w, h):
    for i in range(h):
        t = i / h
        col = tuple(int((250, 214, 150)[j] + ((168, 190, 220)[j] - (250, 214, 150)[j]) * t) for j in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=col)
    # skyline
    base = y + h - 30
    for bx, bw, bh in ((8, 34, 34), (48, 26, 52), (80, 40, 30), (126, 30, 58),
                       (162, 36, 40), (204, 28, 48), (238, 34, 30), (278, 30, 44)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(96, 104, 124))
        for wy in range(base - bh + 6, base - 4, 10):
            for wx in range(bx + 5, bx + bw - 4, 9):
                d.rectangle([x + wx, wy, x + wx + 4, wy + 5], fill=(232, 196, 96))
    d.rectangle([x, base, x + w, y + h], fill=(122, 14, 30))
    d.rectangle([x, base, x + w, base + 4], fill=(198, 152, 46))
    # gold APEC ribbon
    d.rectangle([x + w // 2 - 52, y + 8, x + w // 2 + 52, y + 28], fill=(198, 152, 46))
    d.text((x + w // 2 - text_w("APEC 2026", SANS_B(13)) / 2, y + 10), "APEC 2026",
           font=SANS_B(13), fill=(94, 8, 22))
    # three flags on poles
    def flag(fx, kind, label):
        d.line([(fx, y + 34), (fx, base)], fill=(60, 50, 40), width=3)
        fw, fh = 62, 34
        if kind == "us":
            for s in range(7):
                d.rectangle([fx, y + 34 + s * 5, fx + fw, y + 34 + s * 5 + 5],
                            fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, y + 34, fx + 26, y + 34 + 20], fill=(28, 44, 98))
            for sx in (6, 14, 22):
                for sy in (38, 46):
                    d.ellipse([fx + sx, y + sy, fx + sx + 3, y + sy + 3], fill=(255, 255, 255))
        elif kind == "cn":
            d.rectangle([fx, y + 34, fx + fw, y + 34 + fh], fill=(222, 40, 30))
            d.ellipse([fx + 8, y + 40, fx + 18, y + 50], fill=(255, 220, 60))
            for sx, sy in ((26, 40), (34, 44), (34, 52), (26, 56)):
                d.ellipse([fx + sx, y + sy, fx + sx + 4, y + sy + 4], fill=(255, 220, 60))
        else:
            d.rectangle([fx, y + 34, fx + fw, y + 34 + 12], fill=(255, 255, 255))
            d.rectangle([fx, y + 34 + 12, fx + fw, y + 34 + 23], fill=(0, 60, 160))
            d.rectangle([fx, y + 34 + 23, fx + fw, y + 34 + 34], fill=(210, 30, 30))
        lf = SANS_B(10)
        d.text((fx + fw / 2 - text_w(label, lf) / 2, base + 8), label, font=lf, fill=(255, 255, 255))
    flag(x + 22, "us", "TRUMP")
    flag(x + w // 2 - 8, "cn", "XI")
    flag(x + w - 84, "ru", "PUTIN")

def banner_radar(x, y, w, h):
    for i in range(h):
        t = i / h
        col = tuple(int((30, 44, 70)[j] + ((90, 110, 150)[j] - (30, 44, 70)[j]) * t) for j in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=col)
    # moon
    d.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(232, 220, 170))
    d.ellipse([x + w - 46, y + 16, x + w - 34, y + 28], fill=(210, 196, 150))
    # radar dish (half-disc + sweep lines)
    rx, ry = x + 62, y + h - 8
    d.pieslice([rx - 52, ry - 52, rx + 52, ry + 52], 180, 360, fill=(214, 226, 238))
    d.pieslice([rx - 52, ry - 52, rx + 52, ry + 52], 180, 360, outline=(90, 104, 124), width=2)
    d.line([(rx, ry), (rx - 34, ry - 38)], fill=(90, 104, 124), width=2)
    d.line([(rx, ry), (rx + 4, ry - 48)], fill=(90, 104, 124), width=2)
    d.rectangle([rx - 5, ry - 4, rx + 5, y + h], fill=(70, 84, 104))
    # drone swarm + interception bursts
    drones = [(150, 22), (196, 40), (238, 18), (268, 44), (210, 62)]
    for dx, dy in drones:
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=(20, 20, 24))
        d.line([(x + dx - 10, y + dy), (x + dx + 10, y + dy)], fill=(20, 20, 24), width=2)
        d.line([(x + dx, y + dy - 6), (x + dx, y + dy + 6)], fill=(20, 20, 24), width=2)
    import math
    for bx, by in ((176, 30), (252, 30)):
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([(x + bx, y + by), (x + bx + 12 * math.cos(a), y + by + 12 * math.sin(a))],
                   fill=(240, 200, 60), width=2)
        d.ellipse([x + bx - 4, y + by - 4, x + bx + 4, y + by + 4], fill=(255, 220, 90))
    # dashed tracking line
    for i in range(0, 120, 12):
        d.line([(x + 120 + i, y + 58), (x + 126 + i, y + 58)], fill=(232, 196, 96), width=2)

# ================= HERO CARDS =================
HEROES = [
    (1, "UKRAINE WAR", KICK["red"], "Ukraine strikes Crimean Bridge for a second day",
     "A section of the road bridge collapses; Zelenskyy hails an \u2018unprecedented operation\u2019. Russia hits Kyiv bridges.",
     banner_bridge),
    (2, "DIPLOMACY \u00b7 APEC", KICK["blue"], "Trump, Xi and Putin to hold first three-way summit",
     "Trilateral meeting confirmed for Thursday in Shenzhen; denuclearisation, Iran, Ukraine and trade on the agenda.",
     banner_summit),
    (3, "IRAN WAR", KICK["plum"], "Iran fires drones at a US radar in Bahrain",
     "Tehran says it hit the Sheikh Isa radar; Bahrain says all drones were intercepted, no damage.",
     banner_radar),
]
HX = [10, 348, 686]
HW = 328
HY, HH = 132, 210
for (num, kick_label, kc, head, sub, banner), hx in zip(HEROES, HX):
    card(hx, HY, HW, HH)
    banner(hx + 1, HY + 1, HW - 2, 96)
    badge(hx + 16, HY + 16, 11, num)
    kicker(hx + 12, HY + 106, kick_label, kc)
    hl, hf = fit_lines(head, SERIF_B(20), HW - 24, 2)
    yy = HY + 124
    for ln in hl:
        d.text((hx + 12, yy), ln, font=hf, fill=INK)
        yy += hf.size + 2
    sl = wrap(sub, SANS(11), HW - 24)
    yy += 2
    for ln in sl[:3]:
        d.text((hx + 12, yy), ln, font=SANS(11), fill=SUB)
        yy += 14

# ================= GRID 4-15 (3 cols x 4 rows) =================
GRID = [
    (4, "CANADA \u00b7 CHINA", KICK["green"], "Xi and Carney agree new tariff cuts",
     "China cuts duties on C$400m of pork and seafood; Canada extends steel relief.", icon_chart),
    (5, "EUROPE \u00b7 MIGRATION", KICK["brown"], "Five EU states plan a migrant return hub in Rwanda",
     "First transfers in 2027; rights groups object.", icon_house),
    (6, "JAPAN \u00b7 AIRSPACE", KICK["red"], "Suspected Russian jets enter Japanese airspace",
     "Tokyo scrambles fighters and protests.", icon_jet),
    (7, "UNITED KINGDOM \u00b7 WEST BANK", KICK["blue"], "UK sanctions eight settlement builders",
     "Freezes target West Bank builders and a group accused of blocking Gaza aid.", icon_fence),
    (8, "ISRAEL \u00b7 POLITICS", KICK["plum"], "Netanyahu faces inquiry calls over election-day arrests",
     "His office is alleged to have tipped police against Arab party workers.", icon_ballot),
    (9, "GLOBAL \u00b7 ARMS", KICK["teal"], "Geneva talks on \u2018killer robots\u2019 open",
     "Delegates of 128 states meet at the UN in Geneva to weigh a treaty banning lethal autonomous weapons.", icon_robot),
    (10, "YEMEN \u00b7 WAR", KICK["orange"], "Houthis advance as Yemeni forces retreat to defend Aden",
     "Forces pull back from the Red Sea coast to defend Aden.", icon_mountain),
    (11, "FRANCE \u00b7 COURTS", KICK["brown"], "Depardieu drops appeal and accepts assault conviction",
     "Actor withdraws his challenge to a sexual assault conviction in a Paris court.", icon_court),
    (12, "UNITED STATES \u00b7 SECURITY", KICK["plum"], "US officials say Iran weighs a \u2018dirty bomb\u2019 plot",
     "US intelligence says Iran is developing plans to target Trump aides; the claim is unconfirmed.", icon_shield),
    (13, "ASIA \u00b7 TECHNOLOGY", KICK["teal"], "US moves to close AI chip loophole",
     "Commerce acts to stop China renting US computing power.", icon_chip),
    (14, "EUROPE", KICK["blue"], "Estonia to shut Russia border",
     "Crossings close 1 December after a foiled bomb plot on a drone plant.", icon_fence),
    (15, "UNITED STATES", KICK["red"], "Pentagon fails audit for ninth year",
     "$4.8 trillion in assets could not be verified.", icon_ledger),
]
GX = [10, 348, 686]
GW, GH = 328, 90
GY = 350
for i, (num, kick_label, kc, head, sub, icon) in enumerate(GRID):
    gx = GX[i % 3]
    gy = GY + (i // 3) * (GH + 8)
    card(gx, gy, GW, GH)
    badge(gx + 14, gy + 14, 10, num)
    d.text((gx + 30, gy + 8), kick_label, font=SANS_B(10), fill=kc)
    icon(gx + GW - 44, gy + 28)
    hl, hf = fit_lines(head, SANS_B(14), GW - 24 - 48, 2)
    yy = gy + 26
    for ln in hl:
        d.text((gx + 12, yy), ln, font=hf, fill=INK)
        yy += hf.size + 2
    sl = wrap(sub, SANS(10), GW - 24 - 48)
    yy += 1
    for ln in sl[:2]:
        d.text((gx + 12, yy), ln, font=SANS(10), fill=SUB)
        yy += 13

# ================= MAP + BRIEFS =================
MY = 722
MH = 238
# map panel
card(10, MY, 400, MH)
d.text((22, MY + 8), "WHERE IT HAPPENED", font=SANS_B(13), fill=INK)
d.text((22, MY + 26), "numbered dots = stories 1\u201315", font=SANS(10), fill=SUB)
mx0, my0, mw, mh = 18, MY + 46, 384, 182
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=SEA, outline=(160, 180, 200), width=1)

def proj(lon, lat):
    return (mx0 + (lon + 170) / 360 * mw, my0 + (75 - lat) / 130 * mh)

# simplified continents (lon, lat) polygons
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-82, 66), (-76, 62),
     (-65, 60), (-60, 52), (-55, 47), (-65, 44), (-70, 42), (-75, 35), (-80, 26),
     (-84, 30), (-90, 21), (-97, 26), (-105, 22), (-110, 24), (-117, 32), (-125, 40),
     (-124, 48), (-130, 55), (-150, 60), (-165, 60)],
    # South America
    [(-78, 8), (-72, 11), (-62, 9), (-52, 5), (-44, -3), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20), (-78, -5)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 2), (40, -10), (36, -18), (32, -28), (20, -35),
     (12, -18), (9, -1), (-8, 4)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (5, 53), (8, 57), (18, 56), (21, 55),
     (24, 59), (28, 62), (30, 70), (45, 68), (60, 69), (75, 73), (95, 76), (110, 74),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 58), (158, 52),
     (142, 50), (140, 40), (135, 34), (127, 34), (122, 30), (120, 22), (110, 20),
     (105, 10), (100, 8), (97, 16), (92, 21), (88, 22), (80, 13), (76, 8), (72, 20),
     (66, 25), (60, 25), (56, 26), (52, 28), (48, 29), (44, 29), (40, 31), (35, 36),
     (30, 36), (26, 38), (22, 37), (19, 42), (12, 44), (8, 44), (3, 43), (0, 40),
     (-2, 37), (-9, 37)],
    # Australia
    [(113, -22), (122, -14), (132, -12), (142, -11), (146, -19), (150, -22),
     (153, -27), (150, -37), (140, -38), (132, -32), (124, -33), (115, -35), (113, -26)],
    # UK + Japan hints
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 52), (-1, 50)],
    [(130, 31), (132, 34), (136, 35), (140, 38), (142, 42), (144, 44), (141, 45), (138, 39), (134, 34)],
]
for poly in CONTINENTS:
    pts = [proj(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND, outline=LAND_EDGE)

# story dots: (num, lon, lat) — positions nudged so no two dots overlap
DOTS = [
    (1, 38, 47), (2, 97, 23), (3, 52, 28),
    (4, 130, 39), (5, 30, -2), (6, 139, 36),
    (7, 30, 33), (8, 38, 30), (9, 2, 48),
    (10, 43, 13), (11, 8, 44), (12, -85, 30),
    (13, -100, 45), (14, 24, 60), (15, -70, 44),
]
drawn = []
for num, lon, lat in DOTS:
    px, py = proj(lon, lat)
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(168, 24, 32),
              outline=(255, 255, 255), width=2)
    f = SANS_B(10)
    t = str(num)
    d.text((px - text_w(t, f) / 2, py - 6), t, font=f, fill=(255, 255, 255))
    drawn.append((num, px, py))

# briefs panel
BX = 426
d.text((BX, MY + 8), "ALSO ON TUESDAY 17 NOVEMBER", font=SANS_B(13), fill=INK)
rule(BX, MY + 28, 1024 - BX - 10, CRIMSON, 2)
BRIEFS = [
    (16, "Gaza", "UK, Australia, Canada and Italy urge Israel to open Gaza crossings."),
    (17, "Hormuz", "Third US carrier, USS Theodore Roosevelt, joins the Gulf force."),
    (18, "Trump", "Arrives in Manila for the ASEAN summit before his China meetings."),
    (19, "Microsoft", "Explains last week\u2019s global outage \u2014 a latent defect knocked out 80% of servers."),
    (20, "White House", "Orders every federal agency to get its approval before any employee testifies to Congress."),
    (21, "Health", "Thirteen babies born with measles in the US as cases reach their highest total since 1991."),
    (22, "Fuel", "US petrol averages $3.78 a gallon, down about 20 cents in a week."),
]
by = MY + 38
for num, tag, txt in BRIEFS:
    badge(BX + 10, by + 9, 10, num, fill=(28, 74, 150))
    lines = wrap(f"{tag}: {txt}", SANS(11), 1024 - BX - 44)
    yy = by
    for ln in lines[:2]:
        d.text((BX + 26, yy), ln, font=SANS(11), fill=INK)
        yy += 14
    by = yy + 6

# ================= FOOTER =================
rule(10, 972, 1004, CRIMSON_D, 2)
d.text((10, 980), "Every story happened or was first reported on Tuesday 17 November 2026. Disputed claims are attributed.",
       font=SANS(11), fill=SUB)
d.text((10, 996), "Sources: Reuters \u00b7 Al Jazeera \u00b7 CNN \u00b7 NPR \u00b7 AP. Original drawings.",
       font=SANS(11), fill=SUB)

img.save(OUT, "PNG")
print("wrote", OUT)
