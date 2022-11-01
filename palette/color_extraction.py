from palette import Color
from pathlib import Path
from PIL import Image, ImageDraw
import collections
import requests
import math
import json


default_limit, default_sensitivity, default_palette = 10, 30, True


def extract_colors_from_path(
    path, limit=default_limit, sensitivity=default_sensitivity, palette=default_palette
):
    return extract_colors_from_image(
        Image.open(path),
        limit,
        sensitivity,
        palette,
        filename=Path(path).stem,
    )


def extract_colors_from_image(
    image,
    limit=default_limit,
    sensitivity=default_sensitivity,
    palette=default_palette,
    filename=None,
):
    pixels = list(image.convert("RGBA").getdata())
    colors, total = _count_colors(pixels), len(pixels)
    original_color_count = len(colors)

    limit = min(limit, original_color_count)
    colors = _merge_colors(colors, sensitivity, total)[:limit]
    colors = _update_color_names(colors)

    palette_path = None
    if palette:
        palette_path = _display_palette(colors, filename or "palette")

    return {
        "colors": colors,
        "original_color_count": original_color_count,
        "palette_path": palette_path,
    }


def _display_palette(colors, filename):
    palette = Image.new("RGBA", (len(colors) * 100, 100), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(palette)

    for i, color in enumerate(colors):
        x = int(i % len(colors) * 100)
        canvas.rectangle([(x, 0), (x + 100, 100)], fill=color.rgb)

    palette.save(f"{filename}-palette.png")
    return f"{filename}-palette.png"


def _count_colors(pixels):
    frequencies = collections.defaultdict(int)
    colors = []

    for pixel in pixels:
        rgb, weight = (pixel[0], pixel[1], pixel[2]), pixel[3] / 255
        frequencies[rgb] += weight

    for rgb in frequencies:
        colors.append(
            Color(
                rgb=rgb,
                hex=_rgb_to_hex(rgb),
                weight=frequencies[rgb],
            )
        )

    return colors


def _merge_colors(colors, sensitivity, total):
    colors.sort(reverse=True)

    if sensitivity == 0:
        return colors

    for i in range(len(colors)):
        more = colors[i]

        if not more.isMerged:
            for j in range(i + 1, len(colors)):
                less = colors[j]

                if _calculate_difference(more, less) <= sensitivity:
                    more.weight += less.weight
                    less.isMerged = True

            more.percentage = (float(more.weight) / float(total)) * 100.0

    return sorted([color for color in colors if not color.isMerged], reverse=True)


def _update_color_names(colors):
    names = ""
    for color in colors:
        names += "," + color.hex[1:] if names else color.hex[1:]

    url = f"https://api.color.pizza/v1/?values={names}&noduplicates=true"
    names_response = requests.get(url)
    names = json.loads(names_response.text)["colors"]

    for i, color in enumerate(colors):
        color.name = names[i]["name"]

    return colors


def _rgb_to_hex(RGB):
    return "#%02x%02x%02x" % RGB


def _calculate_difference(x, y):
    return math.sqrt(
        (x.rgb[0] - y.rgb[0]) ** 2
        + (x.rgb[1] - y.rgb[1]) ** 2
        + (x.rgb[2] - y.rgb[2]) ** 2
    )
