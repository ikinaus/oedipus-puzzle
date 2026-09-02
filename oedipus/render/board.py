"""Board to frame. A pure function of the state: no game loop, no stored state."""
from typing import Final

from PIL import Image

from oedipus.core.board import BLANK, Board
from oedipus.render.tiles import Style, Tile

BACKGROUND: Final[tuple[int, int, int]] = (24, 20, 16)


def render_board(board: Board, tiles: list[Tile], style: Style, gap: int = 3,
                 background: tuple[int, int, int] = BACKGROUND) -> Image.Image:
    n = len(board)
    s = tiles[0].size[0]
    side = n * s + gap * (n + 1)
    out = Image.new("RGB", (side, side), background)
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            if value == BLANK:
                continue
            out.paste(style(tiles[value - 1], value),
                      (gap + c * (s + gap), gap + r * (s + gap)))
    return out
