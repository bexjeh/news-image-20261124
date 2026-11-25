#!/usr/bin/env python3
"""WORLD NEWS ATLAS — 24 November 2026.

Draws one 1024x1024 PNG that sums up Tuesday 24 November 2026 in
36 verified stories: a lead story, two top stories, and six regional
sections (Americas, Europe, Middle East, Africa, Asia-Pacific,
Money & Science). Every story was checked against a source dated
24 November 2026.

Stdlib + Pillow only. No network, no clock, no secrets.
Writes entry.png into MAKEFUN_OUTPUT_DIR (fallback ".").
Deterministic: the same bytes on every run.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
BG = (10, 17, 34)          # deep navy, near-black
PANEL = (17, 28, 51)       # card navy
PANEL_LINE = (46, 74, 122)  # panel outline
MAP_BG = (13, 24, 48)      # map band
LAND = (38, 62, 105)       # continent fill
LAND_LINE = (74, 110, 168)  # continent outline
WHITE = (245, 247, 250)
MUTED = (168, 182, 204)
GOLD = (242, 183, 5)
GOLD_DARK = (201, 148, 0)
RED = (242, 92, 84)
BLUE = (74, 144, 226)
TEAL = (26, 188, 156)
GREEN = (46, 204, 113)
PURPLE = (155, 89, 182)
ORANGE = (233, 164, 38)

SECTIONS = [
    ("AMERICAS", RED, [
        ("WASHINGTON", "Trump pardons turkeys Freedom & Feathers",
         "At the White House the president spares two birds and touts a rebuild of the 57-year-old air traffic control system."),
        ("WASHINGTON", "Trump gives Giuliani Medal of Freedom",
         "The nation's highest civilian honour goes to the former New York mayor at a White House ceremony."),
        ("NEW YORK", "US stocks mixed as Huang rally fades",
         "Nasdaq and S&P 500 give back Monday's gains as traders digest Trump's push to restore Jensen Huang at Nvidia."),
        ("WASHINGTON", "US consumer confidence roars back",
         "The Conference Board's November index jumps, while home-price growth holds steady in September."),
        ("CARTAGENA", "Gunmen hold 25 hostage in supermarket",
         "Armed men seize a store in Cartagena; five older women freed as troops deploy and the airport briefly halts landings."),
        ("SINALOA", "US drone helps capture El Chapo Isidro",
         "Mexico detains cartel boss Fausto Isidro Meza Flores after a firefight; Mexico will try him despite a US request."),
    ]),
    ("EUROPE", BLUE, [
        ("GENEVA", "Chess world title match opens",
         "Gukesh faces Sindarov in game 1 of the World Chess Championship in Geneva."),
        ("LISBON", "Portugal votes on 2027 budget",
         "Parliament decides the 2027 budget as unions strike across the country."),
        ("MUNICH", "German business mood rises again",
         "The Ifo survey shows firms brighter on conditions and expectations."),
        ("BERLIN", "Germany first into Ukraine's Delta system",
         "Berlin signs access to Kyiv's Delta battlefield management system and agrees more interceptor missiles."),
        ("LONDON", "UK sanctions Houthis and four officials",
         "Asset freezes and travel bans target the Houthi interior minister, security chief, a judge and a prosecutor."),
        ("LONDON", "UK rules out EU digital ID wallet",
         "PM Andy Burnham tells MPs: \u201cThe UK is not joining the EU digital identity wallet.\u201d"),
    ]),
    ("MIDDLE EAST", ORANGE, [
        ("RIYADH", "PIF tower hit in suspected drone attack",
         "A strike on the King Abdullah Financial District tower wounds at least 11; the PIF HQ hit for a second time in a week."),
        ("GAZA", "Israel kills Hamas security chief",
         "An air strike kills Brig. Gen. Naeem Abu Mohammed Nahel despite the ceasefire in place since October 2025."),
        ("GAZA", "Meningitis epidemic alert in Gaza",
         "272 cases in October \u2014 over eight times the normal monthly rate \u2014 as Gaza's health ministry declares an epidemic."),
        ("BAGHDAD", "Iraq orders federal control of oilfields",
         "PM Ali al-Zaidi orders Baghdad to run oilfields and crossings in Kurdish-held areas; Erbil calls it unacceptable."),
        ("ADEN", "Houthis 60 km from Aden, ready to attack",
         "Yemen's military says Houthi fighters are closing on the temporary capital after government pullbacks."),
        ("LAHJ", "Saudi strikes kill 25 in Yemen",
         "Air strikes on buses and trucks in Wadi Maabaq leave 25 dead or missing and six wounded, Saba reports."),
    ]),
    ("AFRICA", GREEN, [
        ("ITURI", "Fighting traps Ebola responders",
         "Heavy fighting near a hospital in DR Congo forces Ebola teams to take cover for over 24 hours, the WHO says."),
        ("SOUTH KIVU", "DR Congo hunts missing cargo plane",
         "Contact lost with a Cessna 208 on Sunday; rebels claim they shot it down near Minembwe and captured two pilots."),
        ("ANKARA", "Libya's Haftar visits Turkey first time",
         "Eastern Libya's commander meets President Erdogan in Ankara as ties are rebuilt; Erdogan to visit Libya in December."),
        ("TRIPOLI", "Libya demands Kyiv explain ship strikes",
         "Tripoli seeks answers after Ukrainian drones hit ships in Libyan waters, including a Russian warship at Benghazi."),
    ]),
    ("ASIA-PACIFIC", PURPLE, [
        ("JANAKPUR", "First Ayodhya\u2013Janakpur train arrives",
         "The first train from Ayodhya reaches Janakpur in Nepal, opening a new cross-border rail link."),
        ("BEIJING", "China sentences official to death for spying",
         "An official surnamed Ma is condemned for passing 35 state secrets to a foreign country for over 1m yuan."),
        ("BEIJING", "China suspends export curbs to the US",
         "Beijing extends its suspension of critical-material export curbs until January after the Shenzhen summit."),
        ("NEW DELHI", "India ranks 3rd in Asia Power Index",
         "The Lowy Institute puts India third in Asia at 40.5 points, overtaking Russia; the US leads, China second."),
        ("BHOPAL", "India women beat China 6-2 in hockey",
         "Deepika's first-quarter hat-trick powers a fourth straight win at the Women's Asian Champions Trophy."),
        ("HANOI", "Restaurant blast kills at least six",
         "An explosion at a hot-pot restaurant in Dong Da district leaves six dead and at least ten hurt; gas leak suspected."),
    ]),
    ("MONEY & SCIENCE", TEAL, [
        ("WORLDWIDE", "Beaver Supermoon peaks by the Pleiades",
         "The year's brightest full Moon \u2014 a Beaver Supermoon \u2014 shines beside the Pleiades cluster overnight."),
        ("WASHINGTON", "US blacklists Megaspeed in Nvidia case",
         "The firm at the centre of the Jensen Huang spy scandal joins the Entity List with six other firms."),
        ("CANBERRA", "Australia inflation 4.9%, RBA on alert",
         "October CPI jumps 4.9% on the year, keeping the Reserve Bank on alert for further rate rises."),
        ("CARACAS", "Venezuela reveals $237bn debt load",
         "Caracas discloses a $237 billion debt pile as the next tariff fight takes shape."),
        ("ROUND ROCK", "Dell lifts outlook to about $202bn",
         "Dell raises its revenue forecast for the third time, counting $78bn in AI server sales."),
    ]),
]

LEAD = ("NEW YORK", "Huawei guilty of trade secrets and bank fraud",
        "US jury convicts Huawei on 10 of 12 counts, incl. sanctions violations "
        "\u2014 acquits it of racketeering. Sentencing Sept 2027.")
TOP = [
    ("STRAIT OF HORMUZ", "Iran says four tankers hit mines",
     "The IRGC reports four tankers struck naval mines and caught fire; the army "
     "chief orders the strait closed further."),
    ("GULF OF FINLAND", "Ukraine strikes Russian ships at sea",
     "Kyiv hits cargo ship Sparta II in the Gulf of Finland and a corvette off "
     "Libya; Poland cites a new airspace violation."),
]

# Rough continent outlines, (lon, lat) pairs, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 18), (-100, 16), (-105, 20),
     (-110, 23), (-115, 30), (-125, 40), (-125, 48), (-135, 58),
     (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, 0), (-40, -5),
     (-35, -10), (-40, -20), (-45, -25), (-55, -35), (-65, -45),
     (-70, -55), (-73, -40), (-75, -25), (-80, -15), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 10), (51, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -25), (12, -15), (10, -5), (5, 5),
     (-5, 5), (-15, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (12, 55),
     (18, 56), (21, 59), (25, 60), (30, 62), (30, 70), (20, 70),
     (15, 68), (10, 62), (5, 58), (0, 52), (-5, 48), (-10, 44)],
    [(30, 70), (40, 68), (50, 70), (60, 70), (70, 73), (80, 73),
     (90, 75), (100, 77), (110, 76), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 66), (162, 60), (158, 52), (150, 45), (142, 42),
     (140, 38), (135, 34), (130, 33), (127, 35), (122, 38), (120, 30),
     (115, 22), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (85, 20), (80, 15), (75, 10), (70, 20), (65, 25), (60, 25),
     (55, 26), (50, 29), (45, 30), (40, 36), (35, 36), (30, 40),
     (30, 45), (35, 50), (40, 55), (35, 60), (30, 65)],
    [(113, -22), (114, -30), (115, -35), (120, -35), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (150, -25), (146, -20), (142, -15), (140, -12),
     (135, -12), (130, -13), (125, -15), (120, -20), (115, -20)],
]
PINS = [  # (lon, lat, label)
    (-74, 41, "NEW YORK"), (6, 46, "GENEVA"), (47, 25, "RIYADH"),
    (56, 27, "HORMUZ"), (116, 40, "BEIJING"), (77, 29, "NEW DELHI"),
    (0, 52, "LONDON"), (34, 32, ""),
]


def _font(size, bold=False):
    """Best available font: DejaVu, else Pillow's scalable default."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for path in ("/usr/share/fonts/truetype/dejavu/" + name,
                 "/usr/share/fonts/" + name):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def _fit(draw, text, font, max_w):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    ell = "\u2026"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=font) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def _wrap(draw, text, font, max_w, max_lines):
    """Greedy word-wrap to at most max_lines lines; ellipsis if text overflows."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if len(lines) < max_lines and cur:
        lines.append(cur)
    consumed = sum(len(line.split()) for line in lines)
    if consumed < len(words) and lines:
        lines[-1] = _fit(draw, lines[-1], font, max_w)
    return lines[:max_lines]


def _lonlat_to_xy(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (75.0 - lat) / 130.0 * (y1 - y0)
    return (x, y)


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = _font(40, bold=True)
    f_date = _font(24, bold=True)
    f_sub = _font(14, bold=True)
    f_lead = _font(22, bold=True)
    f_body = _font(13)
    f_card_h = _font(17, bold=True)
    f_card_b = _font(12)
    f_sec = _font(16, bold=True)
    f_head = _font(14, bold=True)
    f_det = _font(11)
    f_city = _font(11, bold=True)
    f_pin = _font(10, bold=True)
    f_foot = _font(11)

    # ---------------------------------------------------------------- header
    d.text((20, 8), "WORLD NEWS ATLAS", font=f_title, fill=WHITE)
    d.text((20, 52), "TUESDAY  \u00b7  24 NOVEMBER 2026  \u00b7  36 STORIES, ONE DAY",
           font=f_date, fill=GOLD)
    d.rectangle([20, 84, 1004, 88], fill=GOLD_DARK)
    d.text((20, 92), "EVERY STORY BELOW HAPPENED OR WAS FIRST REPORTED ON 24 NOVEMBER 2026",
           font=f_sub, fill=MUTED)

    # ---------------------------------------------------------------- map band
    mx0, my0, mx1, my1 = 20, 112, 1004, 182
    d.rectangle([mx0, my0, mx1, my1], fill=MAP_BG, outline=PANEL_LINE)
    for poly in CONTINENTS:
        pts = [_lonlat_to_xy(lon, lat, mx0 + 4, my0 + 3, mx1 - 4, my1 - 3)
               for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for i, (lon, lat, label) in enumerate(PINS):
        px, py = _lonlat_to_xy(lon, lat, mx0 + 4, my0 + 3, mx1 - 4, my1 - 3)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GOLD,
                  outline=(10, 17, 34), width=1)
        # Stagger labels above / below the pin so neighbours never collide.
        ly = py - 16 if i % 2 == 0 else py + 7
        if label:
            d.text((px + 7, ly), label, font=f_pin, fill=GOLD)

    # ---------------------------------------------------------------- lead
    ly0, ly1 = 190, 258
    d.rectangle([20, ly0, 1004, ly1], fill=PANEL, outline=PANEL_LINE)
    d.rectangle([20, ly0, 1004, ly0 + 4], fill=GOLD)
    d.text((34, ly0 + 10), "LEAD STORY  \u2014  " + LEAD[0], font=f_sub, fill=GOLD)
    d.text((34, ly0 + 28), LEAD[1], font=f_lead, fill=WHITE)
    d.text((34, ly0 + 52),
           _fit(d, LEAD[2], f_body, 936), font=f_body, fill=MUTED)

    # ---------------------------------------------------------------- top cards
    ty0, ty1 = 266, 344
    card_w = 482
    for k, (city, head, body) in enumerate(TOP):
        x0 = 20 + k * (card_w + 20)
        d.rectangle([x0, ty0, x0 + card_w, ty1], fill=PANEL,
                    outline=PANEL_LINE)
        d.rectangle([x0, ty0, x0 + card_w, ty0 + 4], fill=RED if k == 0 else BLUE)
        d.text((x0 + 14, ty0 + 10), "TOP STORY  \u2014  " + city, font=f_sub,
               fill=RED if k == 0 else BLUE)
        lines = _wrap(d, head, f_card_h, card_w - 28, 1)
        d.text((x0 + 14, ty0 + 29), lines[0], font=f_card_h, fill=WHITE)
        for i, line in enumerate(_wrap(d, body, f_card_b, card_w - 28, 2)):
            d.text((x0 + 14, ty0 + 50 + i * 15), line, font=f_card_b,
                   fill=MUTED)

    # ---------------------------------------------------------------- sections
    gx, gy = 20, 352
    cw, ch, gap = 482, 210, 20
    for idx, (name, color, stories) in enumerate(SECTIONS):
        col, row = idx % 2, idx // 2
        x0 = gx + col * (cw + gap)
        y0 = gy + row * (ch + 12)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=PANEL,
                    outline=PANEL_LINE)
        d.rectangle([x0, y0, x0 + cw, y0 + 26], fill=color)
        d.text((x0 + 12, y0 + 5), name, font=f_sec, fill=(10, 17, 34))
        d.text((x0 + cw - 12, y0 + 5), str(len(stories)) + " STORIES",
               font=f_city, fill=(10, 17, 34), anchor="ra")
        n = len(stories)
        row_h = (ch - 26) / n
        for j, (city, head, detail) in enumerate(stories):
            ry = y0 + 26 + j * row_h
            cy = ry + row_h / 2
            # number badge
            d.ellipse([x0 + 12, cy - 9, x0 + 30, cy + 9], fill=color)
            num = str(j + 1)
            tw = d.textlength(num, font=f_city)
            d.text((x0 + 21 - tw / 2, cy - 6), num, font=f_city,
                   fill=(10, 17, 34))
            tx = x0 + 40
            tw_max = cw - 52
            d.text((tx, cy - 14),
                   _fit(d, head, f_head, tw_max), font=f_head, fill=WHITE)
            d.text((tx, cy + 2),
                   _fit(d, city + " \u2014 " + detail, f_det, tw_max),
                   font=f_det, fill=MUTED)

    # ---------------------------------------------------------------- footer
    foot = ("Sources: Reuters, AP, BBC, Kyiv Independent, Conference Board, "
            "Lowy Institute, Dow Jones \u2014 all stories dated 24 Nov 2026")
    d.text((512, 1008), _fit(d, foot, f_foot, 984), font=f_foot,
           fill=MUTED, anchor="ma")
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG",
             optimize=True)


if __name__ == "__main__":
    main()
