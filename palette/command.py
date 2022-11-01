from palette import (
    extract_colors_from_path,
    default_limit,
    default_sensitivity,
    default_palette,
)
import argparse
import time


def main():
    parser = argparse.ArgumentParser(
        description="palette is a tool for extracting colors from an image"
    )
    parser.add_argument("path", type=str, help="path to image file")
    parser.add_argument(
        "-l",
        type=int,
        default=default_limit,
        help="maximum number of colors to extract (default: {})".format(default_limit),
    )
    parser.add_argument(
        "-s",
        type=int,
        default=default_sensitivity,
        help="color merging sensitivity on a scale of 0 to 100 for clearer results (default: {})".format(
            default_sensitivity
        ),
    )
    parser.add_argument(
        "-p",
        type=bool,
        default=default_palette,
        help="create a color palette (default: {})".format(default_palette),
    )

    args = parser.parse_args()

    print("Image: {}".format(args.path))
    print("Maximum number of colors: {}".format(args.l))
    print("Color sensitivity: {}".format(args.s))
    print("Create palette: {}".format(args.p))
    print()
    print("Extracting...")
    print()

    results = extract_colors_from_path(args.path, args.l, args.s, args.p)
    colors = results["colors"]
    original_color_count = results["original_color_count"]
    palette_path = results["palette_path"]

    timestamp = time.strftime("%I:%M %p, %m/%d/%Y", time.localtime())
    print("Color extraction completed at: {}".format(timestamp))

    if palette_path:
        print("Palette created as {}".format(palette_path))

    total_percentages = 0
    for i, color in enumerate(colors):
        total_percentages += color.percentage

        if color.percentage >= 0.01:
            percentage = "{:.2f}".format(color.percentage)
            print(
                f"{i+1:>3}. {percentage:>6}% : RGB {str(color.rgb):15}, HEX {color.hex:7}, Name {color.name}"
            )

    if total_percentages < 100 and original_color_count < args.l:
        print(
            "{:>2s}Remaining ~{:.2f}% is transparency".format(
                "", 100 - total_percentages
            )
        )
