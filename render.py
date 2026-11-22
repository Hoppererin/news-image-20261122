#!/usr/bin/env python3
"""Draw entry.png for news-image-20261122 — "The World Today".

One image summing up Sunday 22 November 2026: 47 real stories from
7 regions, laid out as a newspaper front page. All text and geometry are
fixed — no network, no randomness, no clock — so running this script
twice writes byte-identical PNG bytes.

Python 3 + Pillow, DejaVu fonts from the system. Usage: python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (253, 253, 247)
INK = (18, 18, 18)
GREY = (96, 96, 96)
RULE = (178, 178, 168)
CARD = (255, 255, 255)
CARD_EDGE = (202, 202, 192)
LEAD_FILL = (235, 240, 247)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(draw, text, path, size, max_width, floor=10):
    """Biggest size at or under `size` that fits, else truncate with …."""
    s = size
    while s > floor:
        f = load_font(path, s)
        if draw.textlength(text, font=f) <= max_width:
            return f, text
        s -= 1
    f = load_font(path, floor)
    while text and draw.textlength(text + "…", font=f) > max_width:
        text = text[:-1]
    return f, text + "…"


def wrap_text(draw, text, f, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ------------------------------------------------------------------ content
LEAD_KICKER = "LEAD  —  THE GULF WAR WIDENS"
LEAD_HEADLINE = "Iran strikes US bases in Kuwait and Bahrain"
LEAD_DECK = ("Tehran hits Ali Al Salem air base and US assets in Bahrain "
             "as the Gulf war widens; Trump says he will seek a permanent "
             "nuclear deal with Iran. (Fox News · AP)")

BIG_STORIES = [
    ("UKRAINE", (190, 0, 0),
     "Russian missiles hit Lviv",
     "2 killed, about 10 hurt; huge blasts shake the western city. (Reuters)"),
    ("TRADE", (10, 80, 145),
     "EU and Indonesia sign deal after 10 years of talks",
     "98.5% of tariffs go; South-East Asia’s biggest economy opens up. (EU)"),
    ("CLIMATE", (0, 128, 140),
     "COP31 deadlocked over fossil fuels and finance",
     "Draft text stalls; funding row leaves the talks facing overtime. (UN News)"),
    ("DISASTER", (185, 140, 0),
     "Magnitude 6.9 quake shakes Peru’s Andes",
     "Strong tremor rattles the mountains; no damage reported at first. (USGS)"),
    ("DIPLOMACY", (110, 45, 155),
     "Trump and Xi meet in Shenzhen",
     "Leaders talk trade at APEC; Berlin presses Moscow to the table. (Reuters)"),
    ("HONG KONG", (45, 120, 48),
     "Hong Kong election committee voting begins",
     "About 5,700 voters choose the powerful committee’s members. (SCMP)"),
]

REGIONS = [
    ("NORTH AMERICA", (10, 80, 145), [
        "FBI probes suspected hack of its criminal database",
        "US declassifies new UFO footage from the Middle East",
        "Tech stock sell-off; Anthropic shares plunge",
        "New York weighs tougher e-bike battery rules after deadly fire",
        "US airlines warned of possible Al-Qaeda threat before Thanksgiving",
        "Trump: contractors must clear Congress requests with White House",
    ]),
    ("LATIN AMERICA", (195, 85, 15), [
        "Mexico arrests cartel boss “El Chapo Isidro”; Sinaloa violence kills 11",
        "Mexican drug lord on FBI’s 10 most wanted list arrested",
        "Bolsonaro in ICU with acute bowel obstruction",
        "Three Americans among four convicted in Honduras trafficking case",
    ]),
    ("EUROPE", (110, 45, 155), [
        "Drones hit Russian cargo ship in Baltic; Finland tightens security",
        "Estonia to close border with Russia; Moscow cries “Iron Curtain”",
        "Cost-of-living protests sweep across Europe",
        "Ex-Italian police chief found dead amid 1992 mafia bombing probe",
        "Russian missile and drone crash in Poland; Warsaw flags “provocation”",
        "France probes Depardieu and author over gang-rape claim",
        "EU’s Costa proposes 3% levy on big tech; France rejects it",
    ]),
    ("AFRICA", (190, 0, 0), [
        "Gambia intercepts 491 would-be irregular migrants",
        "UN: drones killed 1,600+ people in Sudan this year",
        "Ghana’s Mahama announces a $10bn investment",
        "South Africa’s Reserve Bank holds interest rates",
    ]),
    ("MIDDLE EAST", (45, 120, 48), [
        "Tanker attacked off Oman’s coast; more hit in Strait of Hormuz",
        "Iran: Qeshm Island blasts were US munitions disposal, not an attack",
        "Iran says it shot down two US drones over the Strait of Hormuz",
        "ADNOC vessel attacked in Strait of Hormuz; one crew member missing",
        "First Popular Mobilization unit leaves Jurf al-Sakhar, Iraq",
        "UNIFIL begins handing over south Lebanon to the Lebanese army",
        "UN: 1 in 4 partnered women cannot refuse sex; 1 in 3 in Arab states",
        "Iran internet bill would tie online accounts to real identities",
    ]),
    ("ASIA", (185, 140, 0), [
        "Japanese troops to train live-fire at Indian facility for first time",
        "Cyclone Akvan weakens; heavy rain hits Odisha and West Bengal",
        "Modi opens Nitish Setu bridge and Rs 34,470 crore Bihar projects",
        "India’s forex reserves fall to $705.3bn, a three-month low",
        "Nepal PM Balendra Shah scheduled to visit India",
        "India to host WorldSkills Asia 2027",
        "Magnitude 3.6 earthquake hits Assam",
        "Air India extends Jeddah flight suspension until 24 November",
    ]),
    ("OCEANIA & PACIFIC", (0, 128, 140), [
        "Air Niugini emergency landing in Philippines; all 146 survive",
        "Pat Cummins keeps Australia Test captaincy",
        "India face New Zealand in windy Wellington",
    ]),
]


# ------------------------------------------------------------------ drawing
def draw_masthead(d):
    mx = 28
    d.text((CANVAS_W / 2, 20), "THE WORLD TODAY",
           font=load_font(SERIF_BOLD, 54), fill=INK, anchor="ma")
    d.text((CANVAS_W / 2, 82),
           "SUNDAY 22 NOVEMBER 2026   ·   47 STORIES FROM 7 REGIONS",
           font=load_font(SANS, 19), fill=INK, anchor="ma")
    d.line([(mx, 114), (CANVAS_W - mx, 114)], fill=INK, width=3)
    d.line([(mx, 119), (CANVAS_W - mx, 119)], fill=INK, width=1)


def draw_lead(d):
    mx, cw = 28, CANVAS_W - 56
    top, height = 130, 96
    d.rectangle([mx, top, CANVAS_W - mx, top + height],
                fill=LEAD_FILL, outline=CARD_EDGE)
    d.rectangle([mx, top, mx + 7, top + height], fill=(190, 0, 0))
    d.text((mx + 18, top + 8), LEAD_KICKER,
           font=load_font(SANS_BOLD, 12), fill=(190, 0, 0))
    head_font, head_text = shrink_to_fit(
        d, LEAD_HEADLINE, SANS_BOLD, 24, cw - 36)
    d.text((mx + 18, top + 26), head_text, font=head_font, fill=INK)
    body_font = load_font(SANS, 14)
    y = top + 58
    for line in wrap_text(d, LEAD_DECK, body_font, cw - 36)[:2]:
        d.text((mx + 18, y), line, font=body_font, fill=GREY)
        y += 17


def draw_big_stories(d):
    mx, cw = 28, CANVAS_W - 56
    y0 = 240
    d.text((mx, y0), "THE DAY’S BIG STORIES",
           font=load_font(SANS_BOLD, 15), fill=INK)
    d.line([(mx + 218, y0 + 8), (CANVAS_W - mx, y0 + 8)], fill=RULE, width=1)
    card_w, card_h, gap = (cw - 12) // 2, 74, 12
    for i, (tag, color, headline, deck) in enumerate(BIG_STORIES):
        x = mx + (i % 2) * (card_w + gap)
        y = y0 + 26 + (i // 2) * (card_h + gap)
        d.rectangle([x, y, x + card_w, y + card_h],
                    fill=CARD, outline=CARD_EDGE)
        d.rectangle([x, y, x + 6, y + card_h], fill=color)
        d.text((x + 14, y + 6), tag, font=load_font(SANS_BOLD, 11), fill=color)
        head_font, head_text = shrink_to_fit(
            d, headline, SANS_BOLD, 16, card_w - 24)
        d.text((x + 14, y + 21), head_text, font=head_font, fill=INK)
        body_font = load_font(SANS, 12)
        y2 = y + 41
        for line in wrap_text(d, deck, body_font, card_w - 24)[:2]:
            d.text((x + 14, y2), line, font=body_font, fill=GREY)
            y2 += 14


def draw_region_column(d, regions, x, y, col_w):
    for name, color, stories in regions:
        d.rectangle([x, y + 3, x + 10, y + 13], fill=color)
        d.text((x + 16, y), "%s (%d)" % (name, len(stories)),
               font=load_font(SANS_BOLD, 13), fill=color)
        y += 19
        for story in stories:
            f, text = shrink_to_fit(d, story, SANS, 12, col_w - 20)
            d.text((x + 16, y), "•  " + text, font=f, fill=INK)
            y += 15
        y += 5
    return y


def draw_briefs(d):
    mx, cw = 28, CANVAS_W - 56
    y0 = 524
    d.text((mx, y0), "THE WORLD IN BRIEF",
           font=load_font(SANS_BOLD, 15), fill=INK)
    d.line([(mx + 196, y0 + 8), (CANVAS_W - mx, y0 + 8)], fill=RULE, width=1)
    top = y0 + 26
    col_w = (cw - 12) // 2
    left_end = draw_region_column(d, REGIONS[:4], mx, top, col_w)
    right_end = draw_region_column(d, REGIONS[4:], mx + col_w + 12, top, col_w)
    # Explainer box under the shorter (right) column.
    box_x = mx + col_w + 12
    box_y = right_end + 6
    box_h = 76
    d.rectangle([box_x, box_y, CANVAS_W - mx, box_y + box_h],
                fill=CARD, outline=CARD_EDGE)
    d.text((box_x + 14, box_y + 8), "HOW TO READ THIS PAGE",
           font=load_font(SANS_BOLD, 12), fill=INK)
    note_font = load_font(SANS, 12)
    note = ("One day, seven regions: every story on this page was "
            "reported on 21–22 November 2026.")
    y = box_y + 28
    for line in wrap_text(d, note, note_font, col_w - 28):
        d.text((box_x + 14, y), line, font=note_font, fill=GREY)
        y += 15
    d.text((box_x + 14, y),
           "Lead + 6 big stories + 40 in brief = 47 stories.",
           font=note_font, fill=GREY)
    return left_end


def draw_footer(d):
    mx = 28
    fy = CANVAS_H - 30
    d.line([(mx, fy), (CANVAS_W - mx, fy)], fill=RULE, width=1)
    d.text((CANVAS_W / 2, fy + 6),
           "THE WORLD TODAY — 22 November 2026  ·  All stories as reported 21–22 Nov 2026",
           font=load_font(SANS, 11), fill=GREY, anchor="ma")


def render():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_big_stories(d)
    draw_briefs(d)
    draw_footer(d)
    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
