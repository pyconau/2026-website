#!/usr/bin/env python3
"""Generate session announcement graphics."""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from ruamel.yaml import YAML
from graphics_config import LAYOUTS, get_layout, AvatarRegion, TextRegion

AVATAR_GAP = -17  # pixels between adjacent speaker avatars (negative = overlap)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def load_session_data(session_code: str) -> dict:
    """Load session frontmatter from markdown file."""
    session_file = get_project_root() / "src/content/sessions" / f"{session_code}.md"

    if not session_file.exists():
        raise FileNotFoundError(f"Session file not found: {session_file}")

    with open(session_file) as f:
        content = f.read()

    # Parse YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        raise ValueError(f"No frontmatter found in {session_file}")

    yaml = YAML()
    metadata = yaml.load(match.group(1))

    return metadata


def load_speaker_data(speaker_code: str) -> dict:
    """Load speaker data from markdown file."""
    speaker_file = get_project_root() / "src/content/people" / f"{speaker_code}.md"

    if not speaker_file.exists():
        return {"name": "", "code": speaker_code}

    with open(speaker_file) as f:
        content = f.read()

    # Parse YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {"name": "", "code": speaker_code}

    yaml = YAML()
    metadata = yaml.load(match.group(1))

    return metadata if metadata else {"name": "", "code": speaker_code}


def format_schedule(session: dict) -> str:
    """Format room and time for display."""
    start = session.get("start")
    room = session.get("room", "")

    if isinstance(start, str):
        # Parse ISO format
        dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        time_str = dt.strftime("%A %I:%M%p").lstrip("0")
    else:
        time_str = start.strftime("%A %I:%M%p").lstrip("0") if start else ""

    # Lowercase am/pm only
    time_str = time_str.replace("AM", "am").replace("PM", "pm")

    return f"{room}, {time_str}".strip(", ")


def format_speakers(speaker_objects: list[dict]) -> str:
    """Format multiple speakers for display.

    2 speakers: "Speaker A\n& Speaker B"
    3 speakers: "Speaker A,\nSpeaker B\n& Speaker C"
    """
    if not speaker_objects:
        return ""

    names = [s.get("name", "") for s in speaker_objects if s.get("name")]
    if not names:
        return ""

    if len(names) == 1:
        return names[0]
    elif len(names) == 2:
        return f"{names[0]}\n& {names[1]}"
    elif len(names) == 3:
        return f"{names[0]},\n{names[1]}\n& {names[2]}"
    else:
        # 4+ speakers: comma-separated with & before last (fallback)
        return ", ".join(names[:-1]) + f" & {names[-1]}"


def wrap_text(text: str, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap text to fit within max_width. Preserves explicit newlines."""
    lines = []
    # First split by explicit newlines to preserve them
    for paragraph in text.split('\n'):
        current_line = ""
        for word in paragraph.split():
            test_line = current_line + (" " if current_line else "") + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]

            if line_width > max_width and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

    return lines


def get_text_line_height(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    """Get the line height for a given font."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def shrink_font_to_fit(
    text: str,
    draw: ImageDraw.ImageDraw,
    font_path: str,
    start_size: int,
    min_size: int,
    max_width: int,
    max_height: int,
    weight: int = 400,
) -> ImageFont.FreeTypeFont:
    """Find the largest font size that fits the text."""
    size = start_size

    while size >= min_size:
        font = ImageFont.truetype(font_path, size, layout_engine=ImageFont.Layout.BASIC)
        # Try to set weight via variation axis if available
        try:
            font.set_variation_by_axes([weight])
        except Exception:
            pass  # Variable font weight not supported, use default

        lines = wrap_text(text, draw, font, max_width)

        # Calculate total height
        total_height = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            total_height += bbox[3] - bbox[1]

        if total_height <= max_height:
            return font

        size -= 1

    font = ImageFont.truetype(font_path, min_size, layout_engine=ImageFont.Layout.BASIC)
    try:
        font.set_variation_by_axes([weight])
    except Exception:
        pass
    return font


def paste_avatar(img: Image.Image, avatar_path: str, region) -> None:
    """Paste speaker avatar as a circular crop with antialiased edges."""
    if not Path(avatar_path).exists():
        return

    avatar = Image.open(avatar_path).convert("RGBA")

    # Resize to fit the circle diameter
    avatar.thumbnail((region.diameter, region.diameter), Image.Resampling.LANCZOS)

    # Create circular mask with antialiasing by rendering at 2x size and downsampling
    mask_size = region.diameter * 2
    mask = Image.new("L", (mask_size, mask_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse(
        [(0, 0), (mask_size - 1, mask_size - 1)],
        fill=255,
    )
    # Downsample mask for antialiasing effect
    mask = mask.resize((region.diameter, region.diameter), Image.Resampling.LANCZOS)

    # Crop avatar to circle
    avatar_circular = Image.new("RGBA", (region.diameter, region.diameter), (0, 0, 0, 0))
    avatar_circular.paste(avatar, (0, 0))
    avatar_circular.putalpha(mask)

    # Paste onto main image
    img.paste(avatar_circular, (region.x, region.y), avatar_circular)


def draw_text(
    img: Image.Image,
    text: str,
    region,
    font_path: str,
    font_size: int,
    min_font_size: int,
    color: str,
    line_spacing: float = 1.0,
    weight: int = 400,
) -> None:
    """Draw text in a region, shrinking to fit if necessary.

    Args:
        line_spacing: Multiplier for line height (1.0 = normal, 1.2 = 20% taller)
        weight: Font weight (400 = normal, 700 = bold) for variable fonts
    """
    if not text:
        return

    draw = ImageDraw.Draw(img)

    font = shrink_font_to_fit(
        text,
        draw,
        font_path,
        font_size,
        min_font_size,
        region.width,
        region.height,
        weight=weight,
    )

    lines = wrap_text(text, draw, font, region.width)

    # Get base line height
    base_line_height = get_text_line_height(draw, "Qyg", font)
    line_height = int(base_line_height * line_spacing)

    y = region.y
    for line in lines:
        draw.text((region.x, y), line, font=font, fill=color)
        y += line_height


def generate_graphic(session_code: str, layout_name: str = "layout_2", font_size_overrides: dict = None) -> Path:
    """Generate PNG for a session.

    Args:
        font_size_overrides: Dict mapping region names to font sizes to override
    """
    layout = get_layout(layout_name)

    # Apply font size overrides if provided
    if font_size_overrides:
        if "track_name" in font_size_overrides:
            layout.track_name.font_size = font_size_overrides["track_name"]
        if "session_title" in font_size_overrides:
            layout.session_title.font_size = font_size_overrides["session_title"]
        if "speaker_name" in font_size_overrides:
            layout.speaker_name.font_size = font_size_overrides["speaker_name"]
        if "schedule_info" in font_size_overrides:
            layout.schedule_info.font_size = font_size_overrides["schedule_info"]
    output_path = get_project_root() / "public/graphics/sessions" / f"{session_code}-{layout_name}.png"
    session_file = get_project_root() / "src/content/sessions" / f"{session_code}.md"

    # Cache check: skip if output is newer than session file (unless overrides provided)
    if not font_size_overrides and output_path.exists() and output_path.stat().st_mtime > session_file.stat().st_mtime:
        print(f"  {session_code}: cached")
        return output_path

    print(f"  {session_code}: generating...")

    # Load data
    session = load_session_data(session_code)
    speaker_codes = session.get("speakers", [])
    speaker_objects = [load_speaker_data(code) for code in speaker_codes]

    # Load background (includes star and "Session Announcement" text baked in)
    bg_path = Path(__file__).parent / layout.background_file
    img = Image.open(bg_path).convert("RGB")

    # Avatars and speaker name — support 0, 1, 2, 3 speakers
    speaker_text = format_speakers(speaker_objects)
    num_speakers = min(len(speaker_codes), 3)

    if num_speakers == 0:
        # No speakers: use existing layout with empty speaker name
        speaker_name_region = layout.speaker_name
    elif num_speakers == 1:
        # Single speaker: use existing layout
        if speaker_codes:
            first_speaker = speaker_objects[0]
            if first_speaker.get("hasAvatar"):
                avatar_path = (
                    get_project_root() / "public/images/people" / f"{speaker_codes[0]}.jpg"
                )
            else:
                avatar_path = get_project_root() / "public/images/avatar-default.png"
            paste_avatar(img, str(avatar_path), layout.speaker_avatar)

        speaker_name_region = layout.speaker_name
    else:
        # Multi-speaker: compute avatar and text positions
        base = layout.speaker_avatar
        d = base.diameter

        # Paste each avatar
        for i in range(num_speakers):
            code = speaker_codes[i]
            speaker = speaker_objects[i]
            if speaker.get("hasAvatar"):
                avatar_path = get_project_root() / "public/images/people" / f"{code}.jpg"
            else:
                avatar_path = get_project_root() / "public/images/avatar-default.png"

            av_region = AvatarRegion(
                x=base.x + i * (d + AVATAR_GAP),
                y=base.y,
                diameter=d,
            )
            paste_avatar(img, str(avatar_path), av_region)

        # Compute text region geometry
        group_right = base.x + num_speakers * d + (num_speakers - 1) * AVATAR_GAP
        group_mid_y = base.y + d // 2

        # Text region: right edge anchored at same position as 1-speaker layout
        text_right = layout.speaker_name.x + layout.speaker_name.width
        # Gap between avatar group and text: 26px for 2 speakers, 16px for 3 speakers
        text_gap = 26 if num_speakers == 2 else 16
        text_x = group_right + text_gap
        text_width = text_right - text_x

        # Reduce font size for 3 speakers (narrower column)
        font_size = layout.speaker_name.font_size if num_speakers == 2 else 22

        # Measure rendered text to compute vertical centering
        measure_draw = ImageDraw.Draw(img)
        fitted_font = shrink_font_to_fit(
            speaker_text,
            measure_draw,
            str(Path(__file__).parent / layout.speaker_name.font_file),
            font_size,
            layout.speaker_name.min_font_size,
            text_width,
            d,
            weight=layout.speaker_name.weight,
        )
        lines = wrap_text(speaker_text, measure_draw, fitted_font, text_width)
        line_h = get_text_line_height(measure_draw, lines[0], fitted_font)
        total_text_h = line_h * len(lines)
        text_y = group_mid_y - total_text_h // 2

        speaker_name_region = TextRegion(
            x=text_x,
            y=text_y,
            width=text_width,
            height=d,
            font_file=layout.speaker_name.font_file,
            font_size=font_size,
            min_font_size=layout.speaker_name.min_font_size,
            color=layout.speaker_name.color,
            line_spacing=layout.speaker_name.line_spacing,
            weight=layout.speaker_name.weight,
        )

    # Draw text regions
    track_name = session.get("trackName", "")
    # Don't show "Main Conference" track
    if track_name == "Main Conference":
        track_name = ""

    draw_text(
        img,
        track_name,
        layout.track_name,
        Path(__file__).parent / layout.track_name.font_file,
        layout.track_name.font_size,
        layout.track_name.min_font_size,
        layout.track_name.color,
        weight=layout.track_name.weight,
    )

    draw_text(
        img,
        session.get("title", ""),
        layout.session_title,
        Path(__file__).parent / layout.session_title.font_file,
        layout.session_title.font_size,
        layout.session_title.min_font_size,
        layout.session_title.color,
        line_spacing=layout.session_title.line_spacing,
        weight=layout.session_title.weight,
    )

    draw_text(
        img,
        speaker_text,
        speaker_name_region,
        Path(__file__).parent / layout.speaker_name.font_file,
        speaker_name_region.font_size,
        speaker_name_region.min_font_size,
        speaker_name_region.color,
        weight=speaker_name_region.weight,
    )

    draw_text(
        img,
        format_schedule(session),
        layout.schedule_info,
        Path(__file__).parent / layout.schedule_info.font_file,
        layout.schedule_info.font_size,
        layout.schedule_info.min_font_size,
        layout.schedule_info.color,
        weight=layout.schedule_info.weight,
    )

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate session announcement graphics")
    parser.add_argument("--session", help="Generate single session by code")
    parser.add_argument("--layout", default="layout_2", help="Layout name")
    args = parser.parse_args()

    try:
        if args.session:
            generate_graphic(args.session, args.layout)
        else:
            # Generate all sessions
            sessions_dir = get_project_root() / "src/content/sessions"
            session_files = sorted(sessions_dir.glob("*.md"))

            print(f"Generating graphics for {len(session_files)} sessions...")
            for session_file in session_files:
                # Skip breaks
                if "break" in session_file.stem.lower():
                    continue
                generate_graphic(session_file.stem, args.layout)

            print("Done!")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
