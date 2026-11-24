#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news image.

A single deterministic render: the script reads no files, opens no
network connection and uses no random numbers, so every run writes the
same PNG bytes. The picture is an editorial front page for Monday
23 November 2026: one lead story with a chart, five supporting stories
as numbered cards, and a source line at the bottom.

Facts are the day's own, checked on 24 November 2026 against Reuters,
CNN, NPR, Channel NewsAsia and Al Jazeera:
  * Nvidia's board brings Jensen Huang back as chief executive;
    the shares jump 31% on Monday, the Nasdaq 7%.
  * Kyiv says seven naval drones sank the Russian corvette Merkury
    off Benghazi and hit a second Russian cargo ship.
  * Three Russian missiles fell in Poland on Friday; NATO holds an
    emergency meeting on Monday and will send an AWACS aircraft.
  * Indonesia confirms 24 people dead in a candy-factory fire,
    with about 30 missing.
  * Congo, the world's biggest cobalt producer, halts cobalt
    exports from 30 November.
  * Drones hit a sanctioned Russian cargo ship in the Baltic.
"""
import os

from PIL import Image as _Image
from PIL import ImageDraw as _Draw
from PIL import ImageFont as _Font

PAGE_W, PAGE_H = 1024, 1024
EDGE = 48
PAPER_RGB = (247, 244, 238)
TEXT_RGB = (17, 24, 33)
SOFT_RGB = (84, 90, 100)
DARK_RGB = (13, 38, 62)
GILT_RGB = (212, 164, 65)
ALERT_RGB = (178, 42, 38)
FAINT_RGB = (196, 188, 172)
WHITE_RGB = (255, 255, 255)
CARD_LINE_RGB = (214, 207, 192)

_FONT_DIR = "/usr/share/fonts/truetype/noto"
_FALLBACK_DIR = "/usr/share/fonts/truetype/dejavu"


def _load(name, size):
    for folder, stem in ((_FONT_DIR, name), (_FALLBACK_DIR, name)):
        try:
            return _Font.truetype(os.path.join(folder, stem), size)
        except OSError:
            continue
    raise OSError("no font for " + name)


def bold_serif(size):
    return _load("NotoSerif-Bold.ttf", size)


def plain_serif(size):
    return _load("NotoSerif-Regular.ttf", size)


def bold_sans(size):
    return _load("NotoSans-Bold.ttf", size)


def plain_sans(size):
    return _load("NotoSans-Regular.ttf", size)


# Type scale, largest first.
DATE_FONT = bold_sans(20)
TITLE_FONT = bold_serif(58)
STAND_FONT = plain_serif(21)
TAG_FONT = bold_sans(17)
LEAD_FONT = bold_serif(40)
LEAD_TEXT_FONT = plain_sans(20)
BIG_FONT = bold_sans(84)
CHART_TAG_FONT = bold_sans(16)
CHART_NUM_FONT = bold_sans(20)
LABEL_FONT = bold_sans(16)
CARD_HEAD_FONT = bold_serif(25)
CARD_TEXT_FONT = plain_sans(18)
NUM_FONT = bold_sans(34)
NUM_TAG_FONT = bold_sans(14)
SMALL_HEAD_FONT = bold_serif(22)
SMALL_TEXT_FONT = plain_sans(16)
FOOT_FONT = plain_sans(15)


def split_lines(pen, words, face, width):
    """Break a string into lines no wider than `width` pixels."""
    out = []
    current = ""
    for word in words.split():
        trial = word if not current else current + " " + word
        if pen.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def paint_lines(pen, left, top, lines, face, colour, step):
    cursor = top
    for line in lines:
        pen.text((left, cursor), line, font=face, fill=colour)
        cursor += step
    return cursor


def rule(pen, y, colour, thick=1):
    pen.line([(EDGE, y), (PAGE_W - EDGE, y)], fill=colour, width=thick)


def story_card(pen, box, accent, tag, figure, figure_tag, heading, copy,
               head_face=CARD_HEAD_FONT, text_face=CARD_TEXT_FONT):
    """One white card: tag and big figure on the top row, heading below."""
    left, top, right, bottom = box
    pen.rounded_rectangle(box, radius=10, fill=WHITE_RGB,
                          outline=CARD_LINE_RGB, width=1)
    pen.rectangle([left + 14, top, right - 14, top + 5], fill=accent)
    pen.text((left + 20, top + 18), tag, font=LABEL_FONT, fill=accent)
    pen.text((right - 20, top + 14), figure, font=NUM_FONT,
             fill=TEXT_RGB, anchor="ra")
    pen.text((right - 20, top + 52), figure_tag, font=NUM_TAG_FONT,
             fill=SOFT_RGB, anchor="ra")
    inner = right - left - 40
    head_lead = 30 if head_face is CARD_HEAD_FONT else 27
    text_lead = 24 if text_face is CARD_TEXT_FONT else 21
    after_head = paint_lines(
        pen, left + 20, top + 78,
        split_lines(pen, heading, head_face, inner),
        head_face, TEXT_RGB, head_lead)
    paint_lines(pen, left + 20, after_head + 4,
                split_lines(pen, copy, text_face, inner)[:2],
                text_face, SOFT_RGB, text_lead)


def main():
    canvas = _Image.new("RGB", (PAGE_W, PAGE_H), PAPER_RGB)
    pen = _Draw.Draw(canvas)

    # Masthead: day on the left, date on the right, then the title.
    pen.text((EDGE, 26), "MONDAY", font=DATE_FONT, fill=ALERT_RGB)
    pen.text((PAGE_W - EDGE, 26), "23 NOVEMBER 2026", font=DATE_FONT,
             fill=TEXT_RGB, anchor="ra")
    rule(pen, 58, TEXT_RGB, 2)
    pen.text((EDGE, 70), "The World, 23 November", font=TITLE_FONT,
             fill=TEXT_RGB)
    pen.text((EDGE, 138),
             "Six stories, one day — a chipmaker's comeback, a warship sunk,",
             font=STAND_FONT, fill=SOFT_RGB)
    pen.text((EDGE, 164), "and NATO called to an emergency meeting.",
             font=STAND_FONT, fill=SOFT_RGB)
    rule(pen, 198, FAINT_RGB)

    # Lead story: dark panel, headline left, chart right.
    hero = (EDGE, 214, PAGE_W - EDGE, 492)
    pen.rounded_rectangle(hero, radius=10, fill=DARK_RGB)
    pen.text((hero[0] + 28, hero[1] + 22), "MARKETS  ·  THE LEAD STORY",
             font=TAG_FONT, fill=GILT_RGB)
    pen.text((hero[0] + 28, hero[1] + 52), "Nvidia brings back",
             font=LEAD_FONT, fill=WHITE_RGB)
    pen.text((hero[0] + 28, hero[1] + 100), "Jensen Huang",
             font=LEAD_FONT, fill=WHITE_RGB)
    lead_copy = ("The board reinstates the founder as chief executive on "
                 "Monday, 11 days after he resigned, after pressure from "
                 "President Trump and senior US officials.")
    paint_lines(pen, hero[0] + 28, hero[1] + 158,
                split_lines(pen, lead_copy, LEAD_TEXT_FONT, 560),
                LEAD_TEXT_FONT, (205, 216, 228), 27)
    chart_x = hero[2] - 300
    pen.text((chart_x, hero[1] + 22), "SHARES, MONDAY", font=TAG_FONT,
             fill=(150, 170, 190))
    pen.text((chart_x, hero[1] + 52), "+31%", font=BIG_FONT, fill=GILT_RGB)
    pen.text((chart_x, hero[1] + 148), "NVIDIA, MONDAY",
             font=CHART_TAG_FONT, fill=WHITE_RGB)
    pen.rectangle([chart_x, hero[1] + 172, chart_x + 260, hero[1] + 188],
                  fill=GILT_RGB)
    pen.text((chart_x, hero[1] + 196), "Nasdaq  +7%",
             font=CHART_NUM_FONT, fill=(205, 216, 228))
    pen.rectangle([chart_x, hero[1] + 224, chart_x + 59, hero[1] + 240],
                  fill=(120, 140, 160))

    # Two wide stories.
    story_card(pen, (EDGE, 512, 500, 716), (0, 110, 110),
               "WAR AT SEA  ·  LIBYA", "7", "NAVAL DRONES",
               "Ukraine says it sank a Russian warship",
               "Kyiv says drones sank the corvette Merkury at Benghazi "
               "and hit a cargo ship.")
    story_card(pen, (524, 512, PAGE_W - EDGE, 716), ALERT_RGB,
               "NATO  ·  POLAND", "3", "MISSILES",
               "Missiles land in Poland; NATO meets",
               "Three Russian missiles fell in Poland on Friday. NATO "
               "holds an emergency meeting.")

    # Three compact stories.
    story_card(pen, (EDGE, 736, 340, 940), (146, 90, 20),
               "INDONESIA", "24", "KILLED",
               "Factory fire kills 24",
               "Indonesia confirms 24 dead; about 30 missing.",
               head_face=SMALL_HEAD_FONT, text_face=SMALL_TEXT_FONT)
    story_card(pen, (356, 736, 668, 940), (96, 48, 130),
               "AFRICA  ·  MINING", "30", "NOV · HALT",
               "Congo halts cobalt exports",
               "The top cobalt producer halts exports on 30 November.",
               head_face=SMALL_HEAD_FONT, text_face=SMALL_TEXT_FONT)
    story_card(pen, (684, 736, PAGE_W - EDGE, 940), (18, 110, 70),
               "BALTIC SEA", "1", "SHIP HIT",
               "Drones hit a Russian cargo ship",
               "A sanctioned Russian cargo ship is hit by drones.",
               head_face=SMALL_HEAD_FONT, text_face=SMALL_TEXT_FONT)

    # Footer.
    rule(pen, 962, FAINT_RGB)
    pen.text((EDGE, 974), "Reported by Reuters, CNN, NPR and others",
             font=FOOT_FONT, fill=SOFT_RGB)
    pen.text((PAGE_W - EDGE, 974), "23 NOVEMBER 2026  ·  6 STORIES",
             font=FOOT_FONT, fill=SOFT_RGB, anchor="ra")

    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    canvas.save(target, "PNG", optimize=True)
    print(target, os.path.getsize(target), canvas.size)


if __name__ == "__main__":
    main()
