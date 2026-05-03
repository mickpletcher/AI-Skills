#!/usr/bin/env python3
"""
GitHub Social Preview Image Generator
Produces a 1280x640 JPEG under 1 MB from repository metadata.

Usage:
    python generate_preview.py \
        --title "My Project" \
        --subtitle "A tool that does something useful" \
        --tags "python,automation,cli" \
        --language "Python" \
        --output "github-social-preview.jpg"
"""

import argparse
import json
import os
import sys
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")

CANVAS_W = 1280
CANVAS_H = 640
MAX_BYTES = 1_000_000  # 1 MB

CONFIG_PATH = Path(__file__).parent.parent / "templates" / "design_config.json"


def load_config() -> Dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def load_font(path: Optional[str], size: int):
    if path and os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass

    system_candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFCompact.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in system_candidates:
        if os.path.exists(candidate):
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue

    return ImageFont.load_default()


def draw_rounded_rect(draw: ImageDraw.Draw, xy: Tuple, radius: int, fill: Tuple, outline: Optional[Tuple] = None, outline_width: int = 1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=outline_width)


def wrap_text(text: str, font, max_width: int, draw: ImageDraw.Draw) -> List[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_github_mark(draw: ImageDraw.Draw, x: int, y: int, size: int, color: tuple):
    """Draw a simplified GitHub Octocat-style circle mark as a stand-in logo."""
    draw.ellipse([x, y, x + size, y + size], fill=color)
    inner = size // 4
    draw.ellipse(
        [x + inner, y + inner, x + size - inner, y + size - inner],
        fill=None,
        outline=(13, 17, 23),
        width=max(2, size // 16),
    )
    arm_w = max(2, size // 10)
    cx = x + size // 2
    cy = y + size // 2
    draw.line([(cx - size // 4, cy + size // 8), (cx - size // 4, cy + size // 3)], fill=(13, 17, 23), width=arm_w)
    draw.line([(cx + size // 4, cy + size // 8), (cx + size // 4, cy + size // 3)], fill=(13, 17, 23), width=arm_w)


LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#2b7489",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Ruby": "#701516",
    "Java": "#b07219",
    "C#": "#178600",
    "C++": "#f34b7d",
    "C": "#555555",
    "Shell": "#89e051",
    "PowerShell": "#012456",
    "Kotlin": "#A97BFF",
    "Swift": "#ffac45",
    "PHP": "#4F5D95",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Dart": "#00B4AB",
    "Scala": "#c22d40",
    "Haskell": "#5e5086",
    "Elixir": "#6e4a7e",
    "R": "#198CE7",
}


def generate_image(
    title: str,
    subtitle: str,
    tags: List[str],
    language: Optional[str],
    config: Dict,
    width: int = CANVAS_W,
    height: int = CANVAS_H,
) -> Image.Image:
    colors = config.get("colors", {})
    bg_start = hex_to_rgb(colors.get("bg_start", "#0d1117"))
    bg_end = hex_to_rgb(colors.get("bg_end", "#161b22"))
    text_primary = hex_to_rgb(colors.get("text_primary", "#e6edf3"))
    text_secondary = hex_to_rgb(colors.get("text_secondary", "#8b949e"))
    tag_bg = hex_to_rgb(colors.get("tag_bg", "#21262d"))
    tag_border = hex_to_rgb(colors.get("tag_border", "#30363d"))
    tag_text = hex_to_rgb(colors.get("tag_text", "#58a6ff"))
    _mc = hex_to_rgb(colors.get("mark_color", "#30363d"))
    mark_color = (_mc[0], _mc[1], _mc[2], 180)

    img = Image.new("RGB", (width, height), bg_start)
    draw = ImageDraw.Draw(img)

    # Background gradient (horizontal, left to right)
    for x in range(width):
        r = int(bg_start[0] + (bg_end[0] - bg_start[0]) * x / width)
        g = int(bg_start[1] + (bg_end[1] - bg_start[1]) * x / width)
        b = int(bg_start[2] + (bg_end[2] - bg_start[2]) * x / width)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))

    # Subtle top accent line
    accent_color = hex_to_rgb(colors.get("accent", "#58a6ff"))
    draw.rectangle([0, 0, width, 4], fill=accent_color)

    fonts_cfg = config.get("fonts", {})
    title_size = int(fonts_cfg.get("title_size", 72) * (width / CANVAS_W))
    subtitle_size = int(fonts_cfg.get("subtitle_size", 36) * (width / CANVAS_W))
    tag_size = int(fonts_cfg.get("tag_size", 28) * (width / CANVAS_W))
    font_path = fonts_cfg.get("font_path")

    title_font = load_font(font_path, title_size)
    subtitle_font = load_font(font_path, subtitle_size)
    tag_font = load_font(font_path, tag_size)

    padding = int(80 * (width / CANVAS_W))
    mark_size = int(48 * (width / CANVAS_W))

    # GitHub mark watermark top-left
    mark_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    mark_draw = ImageDraw.Draw(mark_img)
    draw_github_mark(mark_draw, padding, padding, mark_size, mark_color)
    img = img.convert("RGBA")
    img.alpha_composite(mark_img)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Content vertical layout
    content_top = padding + mark_size + int(32 * (height / CANVAS_H))
    content_left = padding
    max_text_width = width - padding * 2

    # Title
    title_lines = wrap_text(title, title_font, max_text_width, draw)
    title_line_height = title_size + int(8 * (height / CANVAS_H))
    y = content_top
    for line in title_lines[:2]:
        draw.text((content_left, y), line, font=title_font, fill=text_primary)
        y += title_line_height

    y += int(16 * (height / CANVAS_H))

    # Subtitle
    if subtitle:
        sub_lines = wrap_text(subtitle, subtitle_font, max_text_width, draw)
        sub_line_height = subtitle_size + int(6 * (height / CANVAS_H))
        for line in sub_lines[:2]:
            draw.text((content_left, y), line, font=subtitle_font, fill=text_secondary)
            y += sub_line_height

    # Tag pills — anchored to bottom-left
    if tags:
        tag_y = height - padding - int(tag_size * 1.8)
        tag_x = content_left
        tag_h = int(tag_size * 1.6)
        tag_padding_x = int(tag_size * 0.6)
        tag_gap = int(12 * (width / CANVAS_W))
        corner_r = int(tag_h * 0.35)

        for tag in tags[:5]:
            bbox = draw.textbbox((0, 0), tag, font=tag_font)
            tag_w = (bbox[2] - bbox[0]) + tag_padding_x * 2
            if tag_x + tag_w > width - padding:
                break
            draw_rounded_rect(
                draw,
                (tag_x, tag_y, tag_x + tag_w, tag_y + tag_h),
                radius=corner_r,
                fill=tag_bg,
                outline=tag_border,
                outline_width=1,
            )
            text_y = tag_y + (tag_h - (bbox[3] - bbox[1])) // 2
            draw.text((tag_x + tag_padding_x, text_y), tag, font=tag_font, fill=tag_text)
            tag_x += tag_w + tag_gap

    # Language badge bottom-right
    if language:
        lang_color_hex = LANGUAGE_COLORS.get(language, "#8b949e")
        lang_color = hex_to_rgb(lang_color_hex)
        lang_font = load_font(font_path, tag_size)
        lang_bbox = draw.textbbox((0, 0), language, font=lang_font)
        lang_text_w = lang_bbox[2] - lang_bbox[0]
        lang_text_h = lang_bbox[3] - lang_bbox[1]
        dot_r = int(tag_size * 0.35)
        dot_gap = int(8 * (width / CANVAS_W))
        total_w = dot_r * 2 + dot_gap + lang_text_w
        bx = width - padding - total_w
        by = height - padding - lang_text_h - int(4 * (height / CANVAS_H))
        draw.ellipse([bx, by + (lang_text_h - dot_r * 2) // 2, bx + dot_r * 2, by + (lang_text_h - dot_r * 2) // 2 + dot_r * 2], fill=lang_color)
        draw.text((bx + dot_r * 2 + dot_gap, by), language, font=lang_font, fill=text_secondary)

    return img


def export_jpeg(img: Image.Image, output_path: str, quality: int = 92) -> int:
    img.save(output_path, format="JPEG", quality=quality, optimize=True)
    return os.path.getsize(output_path)


def compress_to_limit(img: Image.Image, output_path: str) -> Tuple[int, int]:
    """Try decreasing quality levels, then scale down if needed. Returns (file_size, quality_used)."""
    quality_steps = [92, 85, 75, 65, 55]

    for q in quality_steps:
        size = export_jpeg(img, output_path, quality=q)
        if size < MAX_BYTES:
            return size, q

    # Scale canvas down 10% and retry from q=92
    w, h = img.size
    scaled = img.resize((int(w * 0.9), int(h * 0.9)), Image.LANCZOS)
    for q in quality_steps:
        size = export_jpeg(scaled, output_path, quality=q)
        if size < MAX_BYTES:
            return size, q

    # Last resort: save at lowest quality without checking
    size = export_jpeg(scaled, output_path, quality=40)
    return size, 40


def main():
    parser = argparse.ArgumentParser(description="Generate a GitHub social preview image.")
    parser.add_argument("--title", required=True, help="Repository name / display title")
    parser.add_argument("--subtitle", default="", help="Repository description or short tagline")
    parser.add_argument("--tags", default="", help="Comma-separated topic tags (up to 5)")
    parser.add_argument("--language", default="", help="Primary programming language")
    parser.add_argument("--output", default="github-social-preview.jpg", help="Output file path")
    args = parser.parse_args()

    config = load_config()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
    language = args.language.strip() or None

    print(f"Generating preview for: {args.title}")

    img = generate_image(
        title=args.title,
        subtitle=args.subtitle,
        tags=tags,
        language=language,
        config=config,
    )

    output_path = args.output
    initial_size = export_jpeg(img, output_path, quality=92)

    if initial_size >= MAX_BYTES:
        print(f"Initial size {initial_size:,} bytes exceeds 1 MB — recompressing...")
        final_size, quality_used = compress_to_limit(img, output_path)
    else:
        final_size = initial_size
        quality_used = 92

    size_kb = final_size / 1024
    print(f"Output: {output_path}")
    print(f"Size:   {size_kb:.1f} KB (quality {quality_used})")
    print(f"Dims:   {CANVAS_W}x{CANVAS_H}")

    if final_size >= MAX_BYTES:
        print(f"WARNING: Could not compress below 1 MB. Final size: {final_size:,} bytes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
