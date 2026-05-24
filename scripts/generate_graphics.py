#!/usr/bin/env python3
"""Generate session announcement graphics."""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from ruamel.yaml import YAML
from graphics_config import (
    PANEL_LAYOUTS,
    THEMES,
    TRACK_ACCENTS,
    get_panel_layout,
    get_theme,
    resolve_background_path,
    resolve_theme_and_layout,
    AvatarRegion,
    TextRegion,
)

AVATAR_GAP = -17  # pixels between adjacent speaker avatars (negative = overlap)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def load_session_data(session_code: str) -> tuple[dict, Path]:
    """Load session frontmatter from markdown file.

    Returns:
        (metadata dict, session file path)
    """
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

    return metadata, session_file


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
    # If before Aug 1, 2026, show "Register Today!" instead of schedule
    if datetime.now() < datetime(2026, 8, 1):
        return "Register Today!"

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
        # Handle right-aligned text
        if hasattr(region, 'align') and region.align == "right":
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = region.x + region.width - line_width
        else:
            x = region.x
        draw.text((x, y), line, font=font, fill=color)
        y += line_height


def _paste_speakers_og(
    img: Image.Image,
    num_speakers: int,
    speaker_codes: list[str],
    speaker_objects: list[dict],
    panel_layout,
    layout_name: str,
) -> None:
    """Paste speaker avatars for OG layouts using fixed bounding boxes (no offsets)."""
    if num_speakers == 0:
        return

    base = panel_layout.speaker_avatar
    d = base.diameter

    # OG right: avatar right edge aligns with speaker name text box right edge, grows left
    if layout_name == "right":
        # Speaker name right edge = x + width
        text_box_right = panel_layout.speaker_name.x + panel_layout.speaker_name.width
        # First avatar's right edge at text_box_right, subsequent avatars extend leftward
        avatar_x_positions = [text_box_right - d - i * (d + AVATAR_GAP) for i in range(num_speakers)]
    else:
        # OG left: avatar grows rightward (standard)
        avatar_x_positions = [base.x + i * (d + AVATAR_GAP) for i in range(num_speakers)]

    for i in range(num_speakers):
        code = speaker_codes[i]
        speaker = speaker_objects[i]
        if speaker.get("hasAvatar"):
            avatar_path = get_project_root() / "public/images/people" / f"{code}.jpg"
        else:
            avatar_path = get_project_root() / "public/images/avatar-default.png"

        av_region = AvatarRegion(
            x=avatar_x_positions[i],
            y=base.y,
            diameter=d,
        )
        paste_avatar(img, str(avatar_path), av_region)


def _paste_speakers_social(
    img: Image.Image,
    num_speakers: int,
    speaker_codes: list[str],
    speaker_objects: list[dict],
    panel_layout,
) -> None:
    """Paste speaker avatars for social layouts with dynamic offsets for multi-speaker."""
    if num_speakers == 0:
        return

    if num_speakers == 1:
        # Single speaker: use fixed layout
        if speaker_codes:
            first_speaker = speaker_objects[0]
            if first_speaker.get("hasAvatar"):
                avatar_path = get_project_root() / "public/images/people" / f"{speaker_codes[0]}.jpg"
            else:
                avatar_path = get_project_root() / "public/images/avatar-default.png"
            paste_avatar(img, str(avatar_path), panel_layout.speaker_avatar)
    else:
        # Multi-speaker: compute avatar positions
        base = panel_layout.speaker_avatar
        d = base.diameter

        avatar_x_positions = [base.x + i * (d + AVATAR_GAP) for i in range(num_speakers)]

        for i in range(num_speakers):
            code = speaker_codes[i]
            speaker = speaker_objects[i]
            if speaker.get("hasAvatar"):
                avatar_path = get_project_root() / "public/images/people" / f"{code}.jpg"
            else:
                avatar_path = get_project_root() / "public/images/avatar-default.png"

            av_region = AvatarRegion(
                x=avatar_x_positions[i],
                y=base.y,
                diameter=d,
            )
            paste_avatar(img, str(avatar_path), av_region)


def _compute_speaker_name_region_social(
    panel_layout, speaker_text: str, num_speakers: int
) -> TextRegion:
    """Compute dynamic speaker name region for social layouts (handles multi-speaker offsets)."""
    if num_speakers <= 1:
        return panel_layout.speaker_name

    # Multi-speaker: compute text region with dynamic offset
    base = panel_layout.speaker_avatar
    d = base.diameter
    group_right = base.x + num_speakers * d + (num_speakers - 1) * AVATAR_GAP
    group_mid_y = base.y + d // 2

    text_right = panel_layout.speaker_name.x + panel_layout.speaker_name.width
    text_gap = 26 if num_speakers == 2 else 16
    text_x = group_right + text_gap
    text_width = text_right - text_x

    font_size = panel_layout.speaker_name.font_size if num_speakers == 2 else 22

    # Measure rendered text to compute vertical centering
    measure_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    fitted_font = shrink_font_to_fit(
        speaker_text,
        measure_draw,
        str(Path(__file__).parent / panel_layout.speaker_name.font_file),
        font_size,
        panel_layout.speaker_name.min_font_size,
        text_width,
        d,
        weight=panel_layout.speaker_name.weight,
    )
    lines = wrap_text(speaker_text, measure_draw, fitted_font, text_width)
    line_h = get_text_line_height(measure_draw, lines[0], fitted_font)
    total_text_h = line_h * len(lines)
    text_y = group_mid_y - total_text_h // 2

    return TextRegion(
        x=text_x,
        y=text_y,
        width=text_width,
        height=d,
        font_file=panel_layout.speaker_name.font_file,
        font_size=font_size,
        min_font_size=panel_layout.speaker_name.min_font_size,
        color=panel_layout.speaker_name.color,
        line_spacing=panel_layout.speaker_name.line_spacing,
        weight=panel_layout.speaker_name.weight,
        align=panel_layout.speaker_name.align,
    )


def generate_graphic(
    session_code: str,
    panel_layout_name: str | None = None,
    theme_name: str | None = None,
    font_size_overrides: dict = None,
) -> Path:
    """Generate PNG for a session (both social and og variants).

    Args:
        session_code: Session identifier
        panel_layout_name: Explicit layout override ("left" or "right")
        theme_name: Explicit theme override
        font_size_overrides: Dict mapping region names to font sizes to override

    Returns:
        Path to the first output (social); og is generated as well
    """
    # Load data
    session, session_file = load_session_data(session_code)
    session_track = session.get("track")

    # Resolve theme + layout (fully deterministic from code hash + track)
    resolved_theme_name, resolved_layout_name = resolve_theme_and_layout(
        session_code,
        session_track,
        theme_override=theme_name or session.get("theme"),
        layout_override=panel_layout_name or session.get("graphicsLayout"),
    )

    theme = get_theme(resolved_theme_name)

    # Check cache for both output types; only generate if any missing or overridden
    output_types = ["social", "square"]
    output_paths = [
        get_project_root() / "public/graphics/sessions" / f"{session_code}-{ot}.png"
        for ot in output_types
    ]

    all_cached = (
        not font_size_overrides
        and all(
            p.exists() and p.stat().st_mtime > session_file.stat().st_mtime
            for p in output_paths
        )
    )

    if all_cached:
        print(f"  {session_code}: cached")
        return output_paths[0]

    print(f"  {session_code}: generating...")

    # Generate both output types
    for output_type in output_types:
        _generate_graphic_for_output_type(
            session_code,
            session,
            session_file,
            resolved_theme_name,
            resolved_layout_name,
            theme,
            output_type,
            font_size_overrides,
        )

    # Write metadata after both are generated
    write_graphics_metadata(session_file, resolved_layout_name, resolved_theme_name)

    return output_paths[0]


def _generate_graphic_for_output_type(
    session_code: str,
    session: dict,
    session_file: Path,
    resolved_theme_name: str,
    resolved_layout_name: str,
    theme,
    output_type: str,
    font_size_overrides: dict | None,
) -> None:
    """Generate PNG for a specific output type (social or square)."""
    session_track = session.get("track")

    # Load config for this output type
    panel_layout = get_panel_layout(resolved_layout_name, output_type)

    # Apply font size overrides if provided
    if font_size_overrides:
        if "track_name" in font_size_overrides:
            panel_layout.track_name.font_size = font_size_overrides["track_name"]
        if "session_title" in font_size_overrides:
            panel_layout.session_title.font_size = font_size_overrides["session_title"]
        if "speaker_name" in font_size_overrides:
            panel_layout.speaker_name.font_size = font_size_overrides["speaker_name"]
        if "schedule_info" in font_size_overrides:
            panel_layout.schedule_info.font_size = font_size_overrides["schedule_info"]

    output_path = (
        get_project_root()
        / "public/graphics/sessions"
        / f"{session_code}-{output_type}.png"
    )

    # Load speaker data
    speaker_codes = session.get("speakers", [])
    speaker_objects = [load_speaker_data(code) for code in speaker_codes]

    # Load background image
    bg_path = Path(__file__).parent / resolve_background_path(
        resolved_theme_name, resolved_layout_name, output_type
    )
    img = Image.open(bg_path).convert("RGB")

    # Avatars and speaker name — support 0, 1, 2, 3 speakers
    speaker_text = format_speakers(speaker_objects)
    num_speakers = min(len(speaker_codes), 3)

    # Square layouts use fixed bounding boxes; social layouts calculate offsets for multi-speaker
    if output_type == "square":
        # OG: use fixed layout for all speaker counts
        _paste_speakers_og(
            img, num_speakers, speaker_codes, speaker_objects, panel_layout, resolved_layout_name
        )
        speaker_name_region = panel_layout.speaker_name
    else:
        # Social: calculate dynamic offsets for multi-speaker
        _paste_speakers_social(
            img, num_speakers, speaker_codes, speaker_objects, panel_layout
        )
        speaker_name_region = _compute_speaker_name_region_social(
            panel_layout, speaker_text, num_speakers
        )

    # Draw text regions
    track_name = session.get("trackName", "")
    # Don't show "Main Conference" track
    if track_name == "Main Conference":
        track_name = ""

    # Track accent color from track mapping (independent of theme)
    track_accent_color = TRACK_ACCENTS.get(session_track, TRACK_ACCENTS[None])

    draw_text(
        img,
        track_name,
        panel_layout.track_name,
        Path(__file__).parent / panel_layout.track_name.font_file,
        panel_layout.track_name.font_size,
        panel_layout.track_name.min_font_size,
        track_accent_color,
        weight=panel_layout.track_name.weight,
    )

    draw_text(
        img,
        session.get("title", ""),
        panel_layout.session_title,
        Path(__file__).parent / panel_layout.session_title.font_file,
        panel_layout.session_title.font_size,
        panel_layout.session_title.min_font_size,
        theme.session_title_color,
        line_spacing=panel_layout.session_title.line_spacing,
        weight=panel_layout.session_title.weight,
    )

    draw_text(
        img,
        speaker_text,
        speaker_name_region,
        Path(__file__).parent / panel_layout.speaker_name.font_file,
        speaker_name_region.font_size,
        speaker_name_region.min_font_size,
        theme.speaker_name_color,
        weight=speaker_name_region.weight,
    )

    draw_text(
        img,
        format_schedule(session),
        panel_layout.schedule_info,
        Path(__file__).parent / panel_layout.schedule_info.font_file,
        panel_layout.schedule_info.font_size,
        panel_layout.schedule_info.min_font_size,
        theme.schedule_info_color,
        weight=panel_layout.schedule_info.weight,
    )

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")


def write_graphics_metadata(
    session_file: Path, layout_name: str, theme_name: str
) -> None:
    """Update session frontmatter with resolved graphics layout + theme.

    Uses round-trip YAML to preserve formatting.
    """
    with open(session_file) as f:
        content = f.read()

    # Parse frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    frontmatter = yaml.load(match.group(1))

    # Update fields
    if frontmatter is None:
        frontmatter = {}
    frontmatter["graphicsLayout"] = layout_name
    frontmatter["theme"] = theme_name

    # Write back
    from io import StringIO

    fp = StringIO()
    yaml.dump(frontmatter, fp)
    new_frontmatter = fp.getvalue()

    new_content = f"---\n{new_frontmatter}---\n{match.group(2)}"

    with open(session_file, "w") as f:
        f.write(new_content)


def main():
    parser = argparse.ArgumentParser(description="Generate session announcement graphics")
    parser.add_argument("--session", help="Generate single session by code")
    parser.add_argument(
        "--layout", default=None, help="Panel layout: left, right (overrides auto-selection)"
    )
    parser.add_argument(
        "--theme", default=None, help="Theme name (overrides track default)"
    )
    args = parser.parse_args()

    try:
        if args.session:
            generate_graphic(args.session, args.layout, args.theme)
        else:
            # Generate all sessions
            sessions_dir = get_project_root() / "src/content/sessions"
            session_files = sorted(sessions_dir.glob("*.md"))

            print(f"Generating graphics for {len(session_files)} sessions...")
            for session_file in session_files:
                # Skip breaks
                if "break" in session_file.stem.lower():
                    continue
                generate_graphic(session_file.stem, args.layout, args.theme)

            print("Done!")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
