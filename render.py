from PIL import Image, ImageDraw, ImageFont


W = H = 1024
PAPER = "#f4f0e6"
INK = "#17191d"
RED = "#b52a22"
BLUE = "#285a78"
GOLD = "#c3a24c"
PALE = "#e3ddd0"

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_text(draw, text, box_width, start_size, min_size, path=BOLD):
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= box_width:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, text, width, fnt):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = word if not line else line + " " + word
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, xy, text, width, size, fill=INK, path=BOLD, spacing=3, max_lines=None):
    fnt = fit_text(draw, text, width, size, max(12, size - 12), path)
    lines = wrap(draw, text, width, fnt)
    if max_lines:
        lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, y, color=INK, width=3):
    draw.rectangle((24, y, W - 24, y + width), fill=color)


def panel(draw, box, label, headline, body, accent=BLUE):
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill="#fbfaf5", outline=INK, width=3)
    draw.rectangle((x1, y1, x1 + 9, y2), fill=accent)
    text_block(draw, (x1 + 22, y1 + 14), label.upper(), x2 - x1 - 35, 20, RED, BOLD)
    text_block(draw, (x1 + 22, y1 + 43), headline, x2 - x1 - 35, 29, INK, BOLD, 1, 3)
    text_block(draw, (x1 + 22, y2 - 62), body, x2 - x1 - 35, 18, INK, SANS, 1, 3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle((24, 18, 1000, 21), fill=RED)
    text_block(draw, (24, 34), "THE WORLD  /  TUESDAY EDITION", 430, 22, RED, BOLD)
    masthead = fit_text(draw, "WORLD NEWS", 720, 58, 46, SERIF)
    draw.text((W // 2, 62), "WORLD NEWS", font=masthead, fill=INK, anchor="mt")
    date_f = font(BOLD, 31)
    draw.text((512, 121), "TUESDAY 17 NOVEMBER 2026", font=date_f, fill=INK, anchor="mt")
    rule(draw, 150, INK, 5)

    # Lead
    lx, ly, lw, lh = 24, 166, 594, 478
    draw.rectangle((lx, ly, lx + lw, ly + lh), fill="#faf9f4", outline=INK, width=4)
    draw.rectangle((lx, ly, lx + lw, ly + 9), fill=RED)
    text_block(draw, (lx + 22, ly + 21), "LEAD  •  UKRAINE–CRIMEA", lw - 44, 23, RED, BOLD)
    lead_f = fit_text(draw, "KERCH BRIDGE HIT", lw - 44, 50, 38, SERIF)
    draw.text((lx + 22, ly + 57), "KERCH BRIDGE HIT", font=lead_f, fill=INK)

    # Bridge illustration
    deck_y = ly + 222
    tower_top = ly + 137
    left_tower = lx + 177
    right_tower = lx + 417
    road_left = lx + 28
    road_right = lx + lw - 28
    gap_left = lx + 267
    gap_right = lx + 327

    # Water beneath the broken span.
    for y, start, end in (
        (ly + 268, lx + 214, lx + 380),
        (ly + 278, lx + 238, lx + 356),
    ):
        points = []
        for x in range(start, end + 1, 8):
            points.append((x, y + (4 if ((x - start) // 8) % 2 else 0)))
        draw.line(points, fill=BLUE, width=5, joint="curve")

    # Two tall pylons with fan cables on either side.
    for tower_x in (left_tower, right_tower):
        draw.line((tower_x, tower_top, tower_x, deck_y), fill=INK, width=9)
        draw.line((tower_x - 17, tower_top, tower_x + 17, tower_top), fill=INK, width=8)
        draw.line((tower_x - 15, deck_y - 8, tower_x + 15, deck_y - 8), fill=INK, width=7)
    for x in (road_left, lx + 104, lx + 143, left_tower, lx + 231, gap_left):
        draw.line((left_tower, tower_top, x, deck_y - 4), fill=INK, width=4)
    for x in (gap_right, lx + 377, right_tower, lx + 457, lx + 497, road_right):
        draw.line((right_tower, tower_top, x, deck_y - 4), fill=INK, width=4)

    # Roadway, split at the failed span; both broken ends pitch into the water.
    draw.polygon(
        [(road_left, deck_y - 5), (gap_left - 14, deck_y - 5),
         (gap_left + 1, deck_y + 7), (gap_left + 26, deck_y + 28),
         (gap_left + 18, deck_y + 33), (gap_left - 9, deck_y + 13),
         (gap_left - 27, deck_y + 5), (road_left, deck_y + 5)],
        fill=INK,
    )
    draw.polygon(
        [(gap_right + 14, deck_y - 5), (road_right, deck_y - 5),
         (road_right, deck_y + 5), (gap_right + 27, deck_y + 5),
         (gap_right + 9, deck_y + 13), (gap_right - 18, deck_y + 33),
         (gap_right - 26, deck_y + 28), (gap_right - 1, deck_y + 7)],
        fill=INK,
    )
    draw.line(
        (gap_left + 10, deck_y + 3, gap_right - 9, deck_y + 18),
        fill=RED,
        width=7,
    )
    draw.text((lx + 35, ly + 110), "BLACK SEA", font=font(BOLD, 17), fill=BLUE)
    draw.text((lx + lw - 150, ly + 110), "CRIMEA", font=font(BOLD, 17), fill=BLUE)

    # Lead copy
    text_block(draw, (lx + 22, ly + 288),
               "A road span collapsed after a Ukrainian strike.",
               lw - 44, 28, INK, BOLD, 2, 2)
    quote_f = font(SERIF, 24)
    draw.text((lx + 22, ly + 341), "Zelenskyy: “unprecedented operation”",
              font=quote_f, fill=RED)
    text_block(draw, (lx + 22, ly + 384),
               "Russia hit Kyiv’s North and South bridges over the Dnipro in response.",
               lw - 44, 22, INK, SANS, 2, 3)

    # Right rail
    right_x = 642
    panel(draw, (right_x, 166, 1000, 314),
          "ASIA  •  MANILA",
          "TRUMP AT ASEAN; TRADE DEAL",
          "Joint trade statement signed with Thailand; talks with Xi & Putin due 19 Nov.",
          BLUE)
    panel(draw, (right_x, 326, 1000, 474),
          "GULF  •  IRAN–U.S.",
          "MINES & CARRIER",
          "Two tankers hit mines; Roosevelt arrived.",
          RED)
    panel(draw, (right_x, 486, 1000, 644),
          "EUROPE  •  MIGRATION",
          "RWANDA RETURN HUB",
          "Germany, Denmark, Austria, Greece & Netherlands plan a joint Rwanda hub.",
          GOLD)

    # Bottom panels
    panel(draw, (24, 660, 320, 886),
          "JAPAN  •  AIRSPACE",
          "FIGHTER JETS SCRAMBLED",
          "Tokyo reacted after two suspected Russian aircraft violated Japan’s airspace.",
          BLUE)
    panel(draw, (348, 660, 644, 886),
          "UK + GAZA",
          "SANCTIONS ON 8 FIRMS",
          "UK curbs settlement builders; joint demand with 3 allies for Gaza crossings to open.",
          RED)
    panel(draw, (672, 660, 1000, 886),
          "TECH  •  TRADE",
          "U.S. CHIPS / CHINA",
          "Commerce moves to license advanced AI chips for data centres that may serve China.",
          GOLD)

    # Intel caveat inside the Gulf panel
    draw.rectangle((658, 442, 984, 468), fill="#f6e4df", outline=RED, width=2)
    text_block(draw, (668, 447),
               "UNCONFIRMED: reported “dirty bomb” claim.",
               306, 12, RED, BOLD, 0, 1)

    # News ticker
    draw.rectangle((24, 898, 1000, 969), fill=INK)
    ticker = font(BOLD, 16)
    draw.text((38, 910), "MORE:  JPMORGAN OUTAGE: SOFTWARE BUG, NOT CYBERATTACK",
              font=ticker, fill=PAPER)
    draw.text((38, 938), "NVIDIA  •  earnings after close  |  PENTAGON  •  audit failed 9th year",
              font=ticker, fill=PAPER)

    # Footer
    footer = font(BOLD, 16)
    draw.text((512, 995), "SOURCES: BBC  •  REUTERS  •  AP  •  AL JAZEERA",
              font=footer, fill=INK, anchor="mt")
    draw.text((24, 992), "17 NOV 2026", font=font(BOLD, 13), fill=INK)
    draw.text((1000, 992), "WORLD BRIEF", font=font(BOLD, 13), fill=INK, anchor="ra")

    img.save("/home/hatch/workspace/makefun/news-image-20261117/entry.png",
             format="PNG", optimize=True)


if __name__ == "__main__":
    main()
