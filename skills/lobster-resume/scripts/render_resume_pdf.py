#!/usr/bin/env python3
"""Canvas PDF renderer for tailored resumes.

Input JSON shape:
{
  "basics": {"name": "", "headline": "", "contact": []},
  "sidebar": [{"title": "", "items": [""]}],
  "summary": "",
  "sections": [
    {"title": "", "entries": [
      {"title": "", "date": "", "bullets": [""]}
    ]}
  ]
}
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.pdfgen import canvas
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing PDF dependency: reportlab. Install with `uv pip install reportlab pypdf` "
        "or run this script with the Codex bundled workspace Python."
    ) from exc


FONT = "STSong-Light"
pdfmetrics.registerFont(UnicodeCIDFont(FONT))

PAGE_W, PAGE_H = A4
MARGIN = 12 * mm
LEFT_W = 48 * mm
GAP = 8 * mm
RIGHT_X = MARGIN + LEFT_W + GAP
RIGHT_W = PAGE_W - RIGHT_X - MARGIN
BOTTOM = 12 * mm

BLUE = colors.HexColor("#1d4ed8")
BLUE_2 = colors.HexColor("#2563eb")
LIGHT = colors.HexColor("#eef6ff")
LINE = colors.HexColor("#bfdbfe")
TEXT = colors.HexColor("#111827")
MUTED = colors.HexColor("#475569")
SOFT = colors.HexColor("#f8fafc")


@dataclass
class TypeScale:
    body: float
    small: float
    tiny: float
    section: float
    role: float
    leading: float
    bullet_leading: float


def make_scale(k: float) -> TypeScale:
    return TypeScale(
        body=8.35 * k,
        small=7.65 * k,
        tiny=7.0 * k,
        section=10.2 * k,
        role=8.8 * k,
        leading=10.8 * k,
        bullet_leading=10.2 * k,
    )


def text_width(text: str, size: float) -> float:
    return pdfmetrics.stringWidth(text, FONT, size)


def wrap(text: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    line = ""
    for ch in text:
        candidate = line + ch
        if text_width(candidate, size) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = ch
    if line:
        lines.append(line)
    return lines


class Painter:
    def __init__(self, canv: canvas.Canvas | None, scale: TypeScale):
        self.c = canv
        self.s = scale

    def text(self, x: float, y: float, value: str, size: float | None = None, color=TEXT) -> None:
        if not self.c:
            return
        self.c.setFillColor(color)
        self.c.setFont(FONT, size or self.s.body)
        self.c.drawString(x, y, value)

    def rect(self, x: float, y: float, width: float, height: float, fill, stroke=0, stroke_color=None) -> None:
        if not self.c:
            return
        self.c.setFillColor(fill)
        if stroke_color:
            self.c.setStrokeColor(stroke_color)
        self.c.rect(x, y, width, height, stroke=stroke, fill=1)

    def line(self, x1: float, y1: float, x2: float, y2: float, color=LINE, width=0.5) -> None:
        if not self.c:
            return
        self.c.setStrokeColor(color)
        self.c.setLineWidth(width)
        self.c.line(x1, y1, x2, y2)

    def wrapped(self, x: float, y: float, value: str, max_width: float, size: float | None = None, leading: float | None = None, color=TEXT) -> float:
        size = size or self.s.body
        leading = leading or self.s.leading
        for line in wrap(value, size, max_width):
            self.text(x, y, line, size, color)
            y -= leading
        return y

    def bullet(self, x: float, y: float, value: str, max_width: float) -> float:
        self.text(x, y, "•", self.s.body, BLUE_2)
        return self.wrapped(x + 7, y, value, max_width - 7, self.s.body, self.s.bullet_leading) - 1

    def section(self, x: float, y: float, title: str, width: float) -> float:
        self.text(x, y, title, self.s.section, BLUE)
        self.line(x, y - 3, x + width, y - 3, LINE, 0.55)
        return y - 12

    def role(self, x: float, y: float, title: str, date: str) -> float:
        self.text(x, y, title, self.s.role, TEXT)
        if date:
            self.text(x, y - 9.5, date, self.s.tiny, MUTED)
            return y - 20
        return y - 11


def draw_sidebar(p: Painter, data: dict[str, Any], photo: Path | None, y: float) -> float:
    x = MARGIN
    p.rect(MARGIN - 4, BOTTOM - 4, LEFT_W + 8, PAGE_H - 2 * BOTTOM + 8, SOFT)
    basics = data.get("basics", {})

    if p.c and photo and photo.exists():
        p.c.drawImage(ImageReader(str(photo)), x + 3, y - 30 * mm, width=30 * mm, height=36.5 * mm, mask="auto")
        name_x = x + 35 * mm
    else:
        name_x = x

    p.text(name_x, y - 8, basics.get("name", ""), 18.0, BLUE)
    p.wrapped(name_x, y - 22, basics.get("headline", ""), LEFT_W - (name_x - x), p.s.small, 9, MUTED)
    y -= 43 * mm if photo and photo.exists() else 23 * mm

    contact = basics.get("contact", [])
    if contact:
        y = p.section(x, y, "联系", LEFT_W)
        for item in contact:
            y = p.wrapped(x, y, str(item), LEFT_W, p.s.small, 9)
        y -= 5

    for block in data.get("sidebar", []):
        y = p.section(x, y, block.get("title", ""), LEFT_W)
        for item in block.get("items", []):
            item = str(item)
            if len(item) <= 12:
                p.rect(x, y - 2, LEFT_W, 8.5, colors.white, stroke=1, stroke_color=LINE)
                p.text(x + 2.5, y, item, p.s.tiny, TEXT)
                y -= 10.5
            else:
                y = p.wrapped(x, y, item, LEFT_W, p.s.tiny, 8.5)
                y -= 1
        y -= 5
    return y


def draw_main(p: Painter, data: dict[str, Any], y: float) -> float:
    x = RIGHT_X
    basics = data.get("basics", {})
    title = data.get("title") or f"面向 {basics.get('headline', '目标岗位')} 的定制简历"
    p.text(x, y, title, 15.2, TEXT)
    y -= 15
    if data.get("summary"):
        y = p.wrapped(x, y, data["summary"], RIGHT_W, p.s.small, 9.4, MUTED)
        y -= 5

    for section in data.get("sections", []):
        y = p.section(x, y, section.get("title", ""), RIGHT_W)
        for entry in section.get("entries", []):
            y = p.role(x, y, entry.get("title", ""), entry.get("date", ""))
            for item in entry.get("bullets", []):
                y = p.bullet(x, y, str(item), RIGHT_W)
            y -= 1
        y -= 4
    return y


def render(canv: canvas.Canvas | None, data: dict[str, Any], photo: Path | None, scale_factor: float) -> float:
    p = Painter(canv, make_scale(scale_factor))
    if canv:
        canv.setFillColor(colors.white)
        canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        p.rect(0, PAGE_H - 8 * mm, PAGE_W, 8 * mm, LIGHT)
        p.rect(0, 0, PAGE_W, 6 * mm, LIGHT)

    y0 = PAGE_H - 16 * mm
    left_y = draw_sidebar(p, data, photo, y0)
    right_y = draw_main(p, data, y0)
    return min(left_y, right_y)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a tailored resume JSON to PDF.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--photo", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)

    scale = 0.88
    for candidate in [1.0, 0.97, 0.94, 0.91, 0.88]:
        if render(None, data, args.photo, candidate) >= BOTTOM:
            scale = candidate
            break

    c = canvas.Canvas(str(args.output), pagesize=A4)
    render(c, data, args.photo, scale)
    c.save()
    print(json.dumps({"output": str(args.output), "scale": scale}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
