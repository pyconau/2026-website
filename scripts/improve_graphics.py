#!/usr/bin/env python3
"""Iterative improvement tool for session graphics text sizing."""

import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw
from graphics_config import LAYOUTS, get_layout


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def extract_region(img: Image.Image, x: int, y: int, width: int, height: int) -> Image.Image:
    """Extract a region from an image."""
    return img.crop((x, y, x + width, y + height))


def calculate_pixel_accuracy(region1: Image.Image, region2: Image.Image) -> float:
    """Calculate pixel-by-pixel accuracy between two images.

    Returns percentage (0-100) of matching pixels.
    """
    # Ensure same size
    if region1.size != region2.size:
        region2 = region2.resize(region1.size, Image.Resampling.LANCZOS)

    # Convert to RGB
    img1_rgb = region1.convert('RGB')
    img2_rgb = region2.convert('RGB')

    # Get pixel data
    pixels1 = list(img1_rgb.getdata())
    pixels2 = list(img2_rgb.getdata())

    # Count matching pixels (within 30 units per channel)
    matching = 0
    for p1, p2 in zip(pixels1, pixels2):
        r1, g1, b1 = p1
        r2, g2, b2 = p2
        if (abs(r1 - r2) <= 30 and abs(g1 - g2) <= 30 and abs(b1 - b2) <= 30):
            matching += 1

    accuracy = (matching / len(pixels1)) * 100 if pixels1 else 0

    return accuracy




def improve_text_region(
    session_code: str,
    text_block_name: str,
    layout_name: str = "layout_1",
    max_iterations: int = 100,
) -> dict:
    """Iteratively improve a text region.

    Returns dict with 'status' ('complete', 'skipped', 'aborted') and 'font_size' if complete.
    """
    from generate_graphics import generate_graphic

    layout = get_layout(layout_name)

    # Get the text region config
    region_map = {
        "track_name": layout.track_name,
        "session_title": layout.session_title,
        "speaker_name": layout.speaker_name,
        "schedule_info": layout.schedule_info,
    }

    if text_block_name not in region_map:
        print(f"Unknown text block: {text_block_name}")
        return False

    region = region_map[text_block_name]

    # Load test image
    test_image_path = get_project_root() / "test_7JZY3E.png"
    if not test_image_path.exists():
        print(f"Test image not found: {test_image_path}")
        return {"status": "aborted"}

    test_img = Image.open(test_image_path)
    test_region = extract_region(test_img, region.x, region.y, region.width, region.height)

    print(f"\n{'='*60}")
    print(f"Improving: {text_block_name}")
    print(f"Region: x={region.x}, y={region.y}, w={region.width}, h={region.height}")
    print(f"Current font size: {region.font_size}pt")
    print(f"{'='*60}\n")

    current_font_size = region.font_size
    best_accuracy = 0
    best_font_size = current_font_size
    iterations = 0
    direction = 1  # 1 for increase, -1 for decrease
    increment = 1

    while iterations < max_iterations:
        iterations += 1

        # Generate graphic with font size override
        try:
            generate_graphic(session_code, layout_name, font_size_overrides={text_block_name: current_font_size})
        except Exception as e:
            print(f"Error generating graphic: {e}")
            return {"status": "aborted"}

        # Load generated image and extract region
        gen_image_path = get_project_root() / f"public/graphics/sessions/{session_code}-{layout_name}.png"
        if not gen_image_path.exists():
            print(f"Generated image not found: {gen_image_path}")
            return {"status": "aborted"}

        gen_img = Image.open(gen_image_path)
        gen_region = extract_region(gen_img, region.x, region.y, region.width, region.height)

        # Calculate accuracy
        accuracy = calculate_pixel_accuracy(test_region, gen_region)

        print(f"Iteration {iterations}: font_size={current_font_size}pt, accuracy={accuracy:.1f}%")

        # Track best accuracy
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_font_size = current_font_size

        # Stop if we're close enough
        if accuracy >= 85:
            print(f"\n✓ Reached {accuracy:.1f}% accuracy!")
            print(f"Final font size: {current_font_size}pt")

            # Ask for confirmation
            response = input(f"\nDoes the {text_block_name} text look correct? (y/n): ").strip().lower()
            if response == 'y':
                return {"status": "complete", "font_size": current_font_size}
            else:
                print("Continuing to refine...")
                # If user says no, try adjusting slightly
                if current_font_size > best_font_size:
                    current_font_size = best_font_size - 1
                    direction = -1
                else:
                    current_font_size = best_font_size + 1
                    direction = 1
                continue

        # Adjust font size based on accuracy trend
        if accuracy > best_accuracy * 0.9:  # Close to best
            # Fine-tune with smaller increments
            if increment > 0.5:
                increment = 0.5

        # Move in the direction that improved accuracy
        current_font_size += direction * increment

        # Bounds check
        if current_font_size < region.min_font_size:
            current_font_size = region.min_font_size
            direction = 1
        if current_font_size > 72:  # Reasonable max
            current_font_size = 72
            direction = -1

    print(f"\nReached max iterations. Best accuracy: {best_accuracy:.1f}% at {best_font_size}pt")
    response = input(f"Use this setting? (y/n): ").strip().lower()
    if response == 'y':
        return {"status": "complete", "font_size": best_font_size}

    return {"status": "skipped"}


def save_font_sizes_to_config(font_sizes: dict, layout_name: str = "layout_1") -> None:
    """Save font size changes to graphics_config.py."""
    config_path = Path(__file__).parent / "graphics_config.py"
    content = config_path.read_text()

    for text_block_name, font_size in font_sizes.items():
        # Replace font_size for this region
        pattern = rf'({text_block_name}=TextRegion\(.*?font_size=)(\d+(?:\.\d+)?)(\s*,)'
        replacement = rf'\g<1>{font_size}\g<3>'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    config_path.write_text(content)


def main():
    text_blocks = [
        "track_name",
        "session_title",
        "speaker_name",
        "schedule_info",
    ]

    session_code = "7JZY3E"
    layout_name = "layout_1"
    font_sizes = {}

    for i, text_block in enumerate(text_blocks):
        print(f"\n\n{'#'*60}")
        print(f"# {i+1}/{len(text_blocks)}: {text_block}")
        print(f"{'#'*60}")

        result = improve_text_region(session_code, text_block, layout_name)

        if result["status"] == "complete":
            print(f"✓ {text_block} complete!")
            font_sizes[text_block] = result["font_size"]
        else:
            response = input(f"Skip {text_block}? (y/n): ").strip().lower()
            if response != 'y':
                return False

    print(f"\n\n{'='*60}")
    print("✓ All text blocks improved!")
    print(f"{'='*60}\n")

    # Save updated config
    if font_sizes:
        print("Saving updated configuration...")
        save_font_sizes_to_config(font_sizes, layout_name)
        print("Configuration saved!")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
