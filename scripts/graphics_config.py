"""Layout definitions for session graphics generation."""

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TextRegion:
    x: int
    y: int
    width: int
    height: int
    font_file: str
    font_size: int
    min_font_size: int = 10
    color: str = "#eaeaea"
    line_spacing: float = 1.0  # Multiplier for line height
    weight: int = 400  # Font weight (400 = normal, 700 = bold)
    align: str = "left"  # "left" or "right" text alignment


@dataclass
class AvatarRegion:
    """Speaker avatar circle. x, y is top-left of bounding box."""
    x: int
    y: int
    diameter: int

    @property
    def center_x(self) -> int:
        return self.x + self.diameter // 2

    @property
    def center_y(self) -> int:
        return self.y + self.diameter // 2


@dataclass
class PanelLayout:
    """Defines positioning of text and avatar regions on canvas. No visual style."""
    name: str  # "left" or "right"
    width: int
    height: int
    track_name: TextRegion
    session_title: TextRegion
    speaker_avatar: AvatarRegion
    speaker_name: TextRegion
    schedule_info: TextRegion


@dataclass
class Theme:
    """Defines visual style: background image and text colors."""
    name: str
    session_title_color: str  # hex color for session title
    speaker_name_color: str  # hex color for speaker name
    schedule_info_color: str  # hex color for room + time


PANEL_LAYOUTS: dict[str, dict[str, PanelLayout]] = {
    "left": {
        "social": PanelLayout(
            name="left",
            width=1280,
            height=780,
            track_name=TextRegion(
                x=61,
                y=184,
                width=400,
                height=38,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=31.0,
                color="#b280ff",
            ),
            session_title=TextRegion(
                x=54,
                y=244,
                width=600,
                height=220,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=53.0,
                min_font_size=32,
                color="#eaeaea",
                line_spacing=1.2,
            ),
            speaker_avatar=AvatarRegion(
                x=54,
                y=513,
                diameter=114,
            ),
            speaker_name=TextRegion(
                x=194,
                y=552,
                width=545,
                height=35,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=28,
                min_font_size=18,
                color="#eaeaea",
                weight=500,
            ),
            schedule_info=TextRegion(
                x=236,
                y=681,
                width=400,
                height=38,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=30.5,
                min_font_size=18,
                color="#eaeaea",
                weight=800,
            ),
        ),
        "og": PanelLayout(
            name="left",
            width=1200,
            height=630,
            track_name=TextRegion(
                x=63,
                y=134,
                width=517,
                height=30,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=25.4,
                color="#b280ff",
            ),
            session_title=TextRegion(
                x=63,
                y=172,
                width=517,
                height=180,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=43.0,
                min_font_size=26,
                color="#eaeaea",
                line_spacing=1.2,
            ),
            speaker_avatar=AvatarRegion(
                x=63,
                y=386,
                diameter=91,
            ),
            speaker_name=TextRegion(
                x=171,
                y=411,
                width=409,
                height=28,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=23,
                min_font_size=14,
                color="#eaeaea",
                weight=500,
            ),
            schedule_info=TextRegion(
                x=248,
                y=527,
                width=332,
                height=30,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=34.2,
                min_font_size=14,
                color="#eaeaea",
                weight=800,
            ),
        ),
        "square": PanelLayout(
            name="left",
            width=1200,
            height=1200,
            track_name=TextRegion(
                x=108,
                y=206,
                width=400,
                height=38,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=31.0,
                color="#b280ff",
            ),
            session_title=TextRegion(
                x=108,
                y=292,
                width=714,
                height=220,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=53.0,
                min_font_size=32,
                color="#eaeaea",
                line_spacing=1.2,
            ),
            speaker_avatar=AvatarRegion(
                x=108,
                y=569,
                diameter=114,
            ),
            speaker_name=TextRegion(
                x=111,
                y=699,
                width=352,
                height=35,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=28,
                min_font_size=18,
                color="#eaeaea",
                weight=500,
                align="left",
            ),
            schedule_info=TextRegion(
                x=111,
                y=843,
                width=600,
                height=38,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=30.5,
                min_font_size=18,
                color="#eaeaea",
                weight=800,
                align="left",
            ),
        ),
    },
    "right": {
        "social": PanelLayout(
            name="right",
            width=1280,
            height=780,
            track_name=TextRegion(
                x=616,
                y=183,
                width=321,
                height=38,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=31.0,
                color="#b280ff",
            ),
            session_title=TextRegion(
                x=609,
                y=240,
                width=625,
                height=173,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=53.0,
                min_font_size=32,
                color="#eaeaea",
                line_spacing=1.2,
            ),
            speaker_avatar=AvatarRegion(
                x=609,
                y=513,
                diameter=114,
            ),
            speaker_name=TextRegion(
                x=749,
                y=552,
                width=490,
                height=35,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=28,
                min_font_size=18,
                color="#eaeaea",
                weight=500,
            ),
            schedule_info=TextRegion(
                x=788,
                y=681,
                width=450,
                height=38,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=30.5,
                min_font_size=18,
                color="#eaeaea",
                weight=800,
            ),
        ),
        "og": PanelLayout(
            name="right",
            width=1200,
            height=630,
            track_name=TextRegion(
                x=510,
                y=134,
                width=689,
                height=30,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=25.4,
                color="#b280ff",
            ),
            session_title=TextRegion(
                x=510,
                y=172,
                width=517,
                height=180,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=43.0,
                min_font_size=26,
                color="#eaeaea",
                line_spacing=1.2,
            ),
            speaker_avatar=AvatarRegion(
                x=510,
                y=386,
                diameter=91,
            ),
            speaker_name=TextRegion(
                x=619,
                y=411,
                width=580,
                height=28,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=23,
                min_font_size=14,
                color="#eaeaea",
                weight=500,
            ),
            schedule_info=TextRegion(
                x=695,
                y=527,
                width=504,
                height=30,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=32.3,
                min_font_size=14,
                color="#eaeaea",
                weight=800,
            ),
        ),
        "square": PanelLayout(
            name="right",
            width=1200,
            height=1200,
            track_name=TextRegion(
                x=339,
                y=210,
                width=400,
                height=38,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=31.0,
                color="#b280ff",
            ),
            session_title=TextRegion(
                x=339,
                y=292,
                width=637,
                height=220,
                font_file="fonts/RobotoSlab-VariableFont_wght.ttf",
                font_size=53.0,
                min_font_size=32,
                color="#eaeaea",
                line_spacing=1.2,
            ),
            speaker_avatar=AvatarRegion(
                x=858,
                y=569,
                diameter=114,
            ),
            speaker_name=TextRegion(
                x=592,
                y=699,
                width=381,
                height=35,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=28,
                min_font_size=18,
                color="#eaeaea",
                weight=500,
                align="right",
            ),
            schedule_info=TextRegion(
                x=741,
                y=843,
                width=231,
                height=38,
                font_file="fonts/PlusJakartaSans-VariableFont_wght.ttf",
                font_size=30.5,
                min_font_size=18,
                color="#eaeaea",
                weight=800,
                align="right",
            ),
        ),
    },
}

THEMES: dict[str, Theme] = {
    "accent_coral": Theme(
        name="accent_coral",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
    "accent_emerald": Theme(
        name="accent_emerald",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
    "accent_lavender": Theme(
        name="accent_lavender",
        session_title_color="#eaeaea",
        speaker_name_color="#eaeaea",
        schedule_info_color="#eaeaea",
    ),
    "accent_lemon": Theme(
        name="accent_lemon",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
    "accent_lime": Theme(
        name="accent_lime",
        session_title_color="#eaeaea",
        speaker_name_color="#eaeaea",
        schedule_info_color="#eaeaea",
    ),
    "accent_violet": Theme(
        name="accent_violet",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
    "charcoal": Theme(
        name="charcoal",
        session_title_color="#eaeaea",
        speaker_name_color="#eaeaea",
        schedule_info_color="#eaeaea",
    ),
    "charcoal_lemon": Theme(
        name="charcoal_lemon",
        session_title_color="#eaeaea",
        speaker_name_color="#eaeaea",
        schedule_info_color="#eaeaea",
    ),
    "stone": Theme(
        name="stone",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
    "stone_emerald": Theme(
        name="stone_emerald",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
    "stone_lemon": Theme(
        name="stone_lemon",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
    "stone_violet": Theme(
        name="stone_violet",
        session_title_color="#282828",
        speaker_name_color="#282828",
        schedule_info_color="#282828",
    ),
}

# Valid theme + layout combinations (existence of background file)
VALID_COMBINATIONS: frozenset[tuple[str, str]] = frozenset({
    ("accent_coral", "left"), ("accent_coral", "right"),
    ("accent_emerald", "left"), ("accent_emerald", "right"),
    ("accent_lavender", "left"), ("accent_lavender", "right"),
    ("accent_lemon", "left"), ("accent_lemon", "right"),
    ("accent_lime", "left"), ("accent_lime", "right"),
    ("accent_violet", "left"), ("accent_violet", "right"),
    ("charcoal", "left"), ("charcoal", "right"),
    ("charcoal_lemon", "left"),  # charcoal_lemon_left.png
    ("stone", "left"),  # stone_left.png
    ("stone_emerald", "right"),  # stone_emerald_right.png
    ("stone_lemon", "left"),  # stone_lemon_left.png
    ("stone_violet", "right"),  # stone_violet_right.png
})

# Track → eligible themes mapping (first in list = default)
TRACK_THEMES: dict[str | None, list[str]] = {
    None: ["charcoal", "accent_coral", "accent_emerald", "accent_lavender", "accent_lemon", "accent_lime", "accent_violet", "stone", "stone_emerald", "stone_lemon", "stone_violet", "charcoal_lemon"],
    "research-software-engineering": ["accent_violet"],
    "devrel": ["accent_coral"],
    "platform-engineering": ["accent_coral"],
    "education": ["accent_lime"],
    "cybersecurity": ["accent_lavender"],
    "data-and-ai": ["accent_lemon", "charcoal_lemon"],
}

# Track → accent color for track label (independent of theme)
TRACK_ACCENTS: dict[str | None, str] = {
    "platform-engineering": "#ef553c",
    "data-and-ai": "#f2bf36",
    "cybersecurity": "#b380ff",
    "devrel": "#ef553c",
    "education": "#bdf462",
    "research-software-engineering": "#511fe5",
    None: "#511fe5",  # main conference / no track
}


def get_panel_layout(name: str, output_type: str = "social") -> PanelLayout:
    """Get a panel layout by name and output type."""
    if name not in PANEL_LAYOUTS:
        raise ValueError(f"Unknown layout: {name}. Available: {list(PANEL_LAYOUTS.keys())}")
    if output_type not in PANEL_LAYOUTS[name]:
        raise ValueError(f"Unknown output type: {output_type} for layout {name}. Available: {list(PANEL_LAYOUTS[name].keys())}")
    return PANEL_LAYOUTS[name][output_type]


def get_theme(name: str) -> Theme:
    """Get a theme by name."""
    if name not in THEMES:
        raise ValueError(f"Unknown theme: {name}. Available: {list(THEMES.keys())}")
    return THEMES[name]


def resolve_background_path(theme_name: str, layout_name: str, output_type: str = "social") -> str:
    """Returns e.g. 'layouts/social/accent_coral_left.png' or 'layouts/square/accent_coral_left.png'.

    Raises ValueError if combo invalid.
    """
    if (theme_name, layout_name) not in VALID_COMBINATIONS:
        raise ValueError(f"No background for theme={theme_name!r}, layout={layout_name!r}")
    return f"layouts/{output_type}/{theme_name}_{layout_name}.png"


def resolve_theme_and_layout(
    session_code: str,
    track: str | None,
    theme_override: str | None = None,
    layout_override: str | None = None,
) -> tuple[str, str]:
    """Deterministically pick theme + layout from session code hash.

    Eligible combos are all VALID_COMBINATIONS where theme is in TRACK_THEMES[track].
    Hash selects one combo. Overrides skip the hash but must still be a valid combo.

    Args:
        session_code: 6-char session identifier (used for deterministic hash)
        track: Track slug or None (main conference)
        theme_override: Force a specific theme (skip hash). If set with layout_override,
                       both must form a valid combo.
        layout_override: Force a specific layout (skip hash). If set with theme_override,
                        both must form a valid combo.

    Returns:
        (theme_name, layout_name) tuple

    Raises:
        ValueError: If override combo is not valid
    """
    # If both are overridden, validate and return
    if theme_override and layout_override:
        if (theme_override, layout_override) not in VALID_COMBINATIONS:
            raise ValueError(
                f"Override combo ({theme_override!r}, {layout_override!r}) is not valid"
            )
        return theme_override, layout_override

    # If only theme is overridden, constrain layout choices by valid combos
    if theme_override:
        eligible_layouts = [
            layout for (t, layout) in VALID_COMBINATIONS if t == theme_override
        ]
        if layout_override:
            if layout_override not in eligible_layouts:
                raise ValueError(
                    f"Layout {layout_override!r} not valid for theme {theme_override!r}"
                )
            return theme_override, layout_override
        if len(eligible_layouts) == 1:
            return theme_override, eligible_layouts[0]
        idx = int(hashlib.md5(session_code.encode()).hexdigest(), 16) % len(
            eligible_layouts
        )
        return theme_override, eligible_layouts[idx]

    # If only layout is overridden, constrain theme choices by eligible track themes
    if layout_override:
        eligible_themes = TRACK_THEMES.get(track, TRACK_THEMES[None])
        eligible_combos = [
            (t, l)
            for (t, l) in VALID_COMBINATIONS
            if t in eligible_themes and l == layout_override
        ]
        if not eligible_combos:
            raise ValueError(
                f"No valid theme+layout combos for track={track!r}, layout={layout_override!r}"
            )
        if len(eligible_combos) == 1:
            return eligible_combos[0]
        idx = int(hashlib.md5(session_code.encode()).hexdigest(), 16) % len(
            eligible_combos
        )
        return eligible_combos[idx]

    # No overrides: full hash-based resolution
    eligible_themes = TRACK_THEMES.get(track, TRACK_THEMES[None])
    eligible_combos = sorted(
        (theme, layout)
        for (theme, layout) in VALID_COMBINATIONS
        if theme in eligible_themes
    )

    if not eligible_combos:
        raise ValueError(f"No eligible combos for track={track!r}")

    idx = int(hashlib.md5(session_code.encode()).hexdigest(), 16) % len(
        eligible_combos
    )
    return eligible_combos[idx]
