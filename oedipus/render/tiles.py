"""Tile faces: where the picture of a tile comes from, and how it is dressed.

A style is any callable (tile, number) -> tile. Everything downstream takes a
style and knows nothing about what it does, so adding a look means writing one
function, not touching the renderer.
"""
import os
from collections.abc import Callable
from pathlib import Path
from typing import Final

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from PIL.Image import Resampling

type Tile = Image.Image
type Style = Callable[[Tile, int], Tile]
type AnyFont = ImageFont.FreeTypeFont | ImageFont.ImageFont

# Distributions disagree about where fonts live, so the path is searched, not
# assumed. Set OEDIPUS_FONT to override. If nothing is found, Pillow's bundled
# font is used: uglier, but rendering never fails over a missing file.
FONT_CANDIDATES: Final[tuple[str, ...]] = (
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",                 # Arch
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",     # Debian, Ubuntu
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",              # Fedora
    "/usr/share/fonts/TTF/LiberationSans-Bold.ttf",
    "/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",        # macOS
    "C:/Windows/Fonts/arialbd.ttf",                             # Windows
)


def find_font(size: int, path: str | Path | None = None) -> AnyFont:
    """A bold font of the requested size, wherever this machine keeps one."""
    for name in (path, os.environ.get("OEDIPUS_FONT"), *FONT_CANDIDATES):
        if not name:
            continue
        try:
            return ImageFont.truetype(str(name), size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def load_reference(path: str | Path, size: int) -> Image.Image:
    """The picture the solved puzzle shows, as a square."""
    return Image.open(path).convert("RGB").resize((size, size), Resampling.LANCZOS)


def cut_tiles(ref: Image.Image, n: int) -> list[Tile]:
    """Reference cut into n*n faces, indexed by tile number minus one."""
    s = ref.size[0] // n
    return [ref.crop((c * s, r * s, (c + 1) * s, (r + 1) * s))
            for r in range(n) for c in range(n)]


def style_edged(tile: Tile, number: int, bevel: int = 4) -> Tile:
    """Picture untouched, bevelled edge and a dark outline."""
    out = tile.copy()
    d = ImageDraw.Draw(out, "RGBA")
    w, h = out.size
    for i in range(bevel):
        d.line([(i, i), (w - i, i)], fill=(255, 255, 255, 130))
        d.line([(i, i), (i, h - i)], fill=(255, 255, 255, 130))
        d.line([(w - 1 - i, i), (w - 1 - i, h - i)], fill=(0, 0, 0, 130))
        d.line([(i, h - 1 - i), (w - i, h - 1 - i)], fill=(0, 0, 0, 130))
    d.rectangle([0, 0, w - 1, h - 1], outline=(35, 25, 15, 255), width=2)
    return out


def style_dim(tile: Tile, number: int, factor: float = 0.62) -> Tile:
    """Darkened picture with the tile number on top.

    The dimming is not decoration: at full brightness a light numeral is
    unreadable against the pale stone.
    """
    out = ImageEnhance.Brightness(tile).enhance(factor)
    d = ImageDraw.Draw(out)
    font = find_font(int(out.size[0] * 0.34))
    text = str(number)
    box = d.textbbox((0, 0), text, font=font)
    d.text(((out.size[0] - box[2]) / 2, (out.size[1] - box[3]) / 2 - box[1] / 2),
           text, font=font, fill=(255, 236, 190))
    return out
