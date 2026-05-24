"""Layout definitions for session graphics generation."""

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
class Layout:
    name: str
    width: int
    height: int
    background_file: str
    track_name: TextRegion
    session_title: TextRegion
    speaker_avatar: AvatarRegion
    speaker_name: TextRegion
    schedule_info: TextRegion
    track_colors: dict[str, str]


LAYOUTS = {
    "layout_1": Layout(
        name="layout_1",
        width=1280,
        height=780,
        background_file="layouts/layout_1_background.png",
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
        track_colors={
            "platform-engineering": "#b280ff",
            "data-and-ai": "#F2BF36",
            "cybersecurity": "#8B5CF6",
            "devrel": "#EF553C",
            "education": "#bdf462",
            "research-software-engineering": "#511FE5",
        },
    ),
    "layout_2": Layout(
        name="layout_2",
        width=1280,
        height=780,
        background_file="layouts/layout_2_background.png",
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
        track_colors={
            "platform-engineering": "#b280ff",
            "data-and-ai": "#F2BF36",
            "cybersecurity": "#8B5CF6",
            "devrel": "#EF553C",
            "education": "#bdf462",
            "research-software-engineering": "#511FE5",
        },
    ),
}


def get_layout(name: str) -> Layout:
    """Get a layout by name."""
    if name not in LAYOUTS:
        raise ValueError(f"Unknown layout: {name}. Available: {list(LAYOUTS.keys())}")
    return LAYOUTS[name]
