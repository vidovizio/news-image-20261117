"""Build the original 17 November 2026 world-news front page."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
PAPER = "#F3EBD9"
INK = "#171A1D"
RED = "#9D2928"
BLUE = "#7294A5"
PALE_BLUE = "#D9E5E5"
RULE = "#B9AE9B"
WHITE = "#FFFDF7"
ROOT = Path(__file__).resolve().parent

image = Image.new("RGB", (SIZE, SIZE), PAPER)
draw = ImageDraw.Draw(image)


def font(size: int, serif: bool = False, regular: bool = False) -> ImageFont.FreeTypeFont:
    if serif:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    elif regular:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    return ImageFont.truetype(path, size)


def text(x: int, y: int, value: str, size: int, color: str = INK,
         serif: bool = False, regular: bool = False) -> None:
    draw.text((x, y), value, font=font(size, serif, regular), fill=color)


def wrapped(x: int, y: int, value: str, width: int, size: int,
            color: str = INK, leading: int = 4, regular: bool = False) -> int:
    face = font(size, regular=regular)
    words = value.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and draw.textlength(candidate, font=face) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    for row, item in enumerate(lines):
        draw.text((x, y + row * (size + leading)), item, font=face, fill=color)
    return y + len(lines) * (size + leading)


def panel(box: tuple[int, int, int, int], fill: str = WHITE) -> None:
    draw.rounded_rectangle(box, radius=8, fill=fill, outline=RULE, width=2)


def right_card(y: int, tag: str, title: str, body: str,
               report: str | None = None) -> None:
    x, w, h = 610, 376, 146
    panel((x, y, x + w, y + h))
    text(x + 14, y + 10, tag, 15, RED)
    title_end = wrapped(x + 14, y + 32, title, w - 28, 19, INK, 1)
    body_y = max(y + 72, title_end + 5)
    if report:
        wrapped(x + 14, body_y, body, w - 28, 16, INK, 2)
        draw.rounded_rectangle((x + 12, y + 114, x + w - 12, y + 140),
                               radius=5, fill="#FFF6F0", outline=RED, width=2)
        text(x + 20, y + 119, report, 14, RED)
    else:
        wrapped(x + 14, body_y, body, w - 28, 16, INK, 2)


# Restrained newsprint texture and the masthead.
for y in range(16, 1000, 24):
    draw.line((28, y, 996, y), fill="#F0E7D5", width=1)
text(38, 22, "THE WORLD  /  TUESDAY EDITION", 16, RED)
text(36, 42, "WORLD NEWS", 62, INK, serif=True)
text(40, 119, "TUESDAY 17 NOVEMBER 2026", 22, INK)
draw.line((38, 155, 986, 155), fill=INK, width=3)

# Lead story and the broken Kerch crossing.
panel((38, 174, 594, 636))
text(54, 185, "LEAD  •  UKRAINE–CRIMEA", 17, RED)
text(52, 209, "KERCH BRIDGE HIT", 37, INK, serif=True)
draw.line((57, 252, 574, 252), fill=RULE, width=2)
text(64, 261, "BLACK SEA", 14, INK)
text(476, 261, "CRIMEA", 14, INK)

# Distant shoreline and water give the bridge a clear setting.
draw.rectangle((55, 292, 577, 437), fill=PALE_BLUE)
draw.polygon([(55, 316), (106, 305), (156, 315), (204, 299), (249, 313),
              (298, 307), (350, 318), (402, 303), (458, 314), (514, 300),
              (577, 312), (577, 327), (55, 327)], fill="#C5D5D4")
draw.rectangle((55, 327, 577, 437), fill=BLUE)
for y in (347, 372, 398, 422):
    draw.arc((50, y - 10, 178, y + 12), 5, 170, fill="#D9E6E3", width=3)
    draw.arc((212, y - 10, 347, y + 12), 5, 170, fill="#D9E6E3", width=3)
    draw.arc((378, y - 10, 510, y + 12), 5, 170, fill="#D9E6E3", width=3)

deck_y = 341
left_pylon, right_pylon = 203, 430
for end_x, end_y in ((58, 337), (155, 337), (246, 337), (278, 345)):
    draw.line((left_pylon, 309, end_x, end_y), fill=INK, width=2)
for end_x, end_y in ((367, 345), (388, 337), (477, 337), (570, 337)):
    draw.line((right_pylon, 309, end_x, end_y), fill=INK, width=2)
for px in (left_pylon, right_pylon):
    draw.polygon([(px - 10, deck_y), (px - 6, 285), (px + 6, 285),
                  (px + 10, deck_y)], fill=INK)
    draw.line((px - 23, 309, px + 23, 309), fill=INK, width=5)

# The deck has two visibly separated, downward-tilted broken ends.
draw.line((58, 337, 155, 337), fill=INK, width=10)
draw.line((155, 337, 202, deck_y), fill=INK, width=10)
draw.line((202, deck_y, 246, 337), fill=INK, width=10)
draw.line((246, 337, 278, 345), fill=INK, width=10)
draw.line((278, 345, 285, 352), fill=INK, width=10)
draw.line((359, 352, 367, 345), fill=INK, width=10)
draw.line((367, 345, 388, 337), fill=INK, width=10)
draw.line((388, 337, 430, deck_y), fill=INK, width=10)
draw.line((430, deck_y, 477, 337), fill=INK, width=10)
draw.line((477, 337, 570, 337), fill=INK, width=10)

draw.line((278, 339, 287, 351), fill=RED, width=5)
draw.line((366, 339, 357, 351), fill=RED, width=5)

text(54, 449, "A road span collapsed after a Ukrainian strike.", 17)
text(54, 477, 'ZELENSKYY: “UNPRECEDENTED OPERATION”', 16, RED)
wrapped(54, 507, "Russia hit Kyiv’s North and South bridges over the Dnipro in response.",
        520, 17, INK, 3)

# Three concise regional briefs.
right_card(174, "ASIA  •  MANILA", "TRUMP AT ASEAN; TRADE DEAL",
           "Joint trade statement signed with Thailand; talks with Xi & Putin due 19 Nov.")
right_card(332, "GULF  •  IRAN–U.S.", "MINES & CARRIER",
           "Two tankers hit mines; USS Theodore Roosevelt arrived.",
           "UNCONFIRMED: reported “dirty bomb”")
right_card(490, "EUROPE  •  MIGRATION", "RWANDA RETURN HUB",
           "Germany, Denmark, Austria, Greece & Netherlands plan a joint hub.")

# Bottom row: the day's additional regional and technology stories.
bottom_y, bottom_h, box_w = 652, 148, 304
bottom_cards = [
    (38, "JAPAN  •  AIRSPACE", "FIGHTER JETS SCRAMBLED",
     "Tokyo reacted after two suspected Russian aircraft violated its airspace."),
    (360, "UK + GAZA", "SANCTIONS ON 8 FIRMS",
     "UK curbs settlement builders; 3 allies join call to open Gaza crossings."),
    (682, "TECH  •  TRADE", "U.S. CHIPS / CHINA",
     "Commerce moves to license advanced AI chips for data centres that may serve China."),
]
for x, tag, title, body in bottom_cards:
    panel((x, bottom_y, x + box_w, bottom_y + bottom_h))
    text(x + 13, bottom_y + 10, tag, 15, RED)
    title_end = wrapped(x + 13, bottom_y + 33, title, box_w - 26, 19, INK, 1)
    wrapped(x + 13, max(bottom_y + 70, title_end + 4), body,
            box_w - 26, 16, INK, 2)

# Business and defense headlines get a high-contrast closing band.
draw.rectangle((38, 812, 986, 959), fill=INK)
text(54, 827, "MORE  /  JPMORGAN OUTAGE", 16, "#F3B7A9")
text(54, 851, "SOFTWARE BUG, NOT CYBERATTACK", 24, WHITE)
draw.line((54, 886, 969, 886), fill="#66686A", width=1)
text(54, 901, "NVIDIA  •  earnings after close", 18, WHITE)
text(54, 927, "PENTAGON  •  audit failed 9th year", 18, WHITE)

# A clean imprint closes the page.
draw.line((38, 972, 986, 972), fill=INK, width=2)
text(40, 980, "17 NOV 2026", 14, INK)
text(306, 980, "SOURCES: BBC  •  REUTERS  •  AP  •  AL JAZEERA", 13, INK)
text(879, 980, "WORLD BRIEF", 14, RED)

image.save(ROOT / "entry.png", format="PNG", optimize=True)
