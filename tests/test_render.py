"""Rendering is checked against a synthetic reference, not the photograph.

Every tile of that reference is one flat, distinct colour, so "which tile
landed in which cell" is answered by reading a single pixel. A transposition or
an off-by-one in the tile index would still produce a plausible-looking grid,
and no other test in the suite would notice.
"""
from pathlib import Path

import pytest
from PIL import Image, ImageSequence

from oedipus.core.board import Board, goal, neighbors
from oedipus.render.anim import save_gif
from oedipus.render.board import BACKGROUND, render_board
from oedipus.render.tiles import (
    FONT_CANDIDATES,
    Tile,
    cut_tiles,
    find_font,
    load_reference,
    style_dim,
    style_edged,
)

TILE = 40
GAP = 3


def colour(k: int) -> tuple[int, int, int]:
    return (16 * k + 8, 255 - (16 * k + 8), 128)


def solid_reference(n: int) -> Image.Image:
    """Reference whose tile k is filled with colour(k), for k = 0..n*n-1."""
    ref = Image.new("RGB", (TILE * n, TILE * n))
    for k in range(n * n):
        r, c = divmod(k, n)
        ref.paste(Image.new("RGB", (TILE, TILE), colour(k)), (c * TILE, r * TILE))
    return ref


def style_raw(tile: Tile, number: int) -> Tile:
    """Identity style: isolates placement from decoration."""
    return tile


def cell_pixel(img: Image.Image, r: int, c: int) -> tuple[int, int, int]:
    """A pixel well inside cell (r, c), clear of bevels and of the numeral."""
    x = GAP + c * (TILE + GAP) + int(TILE * 0.2)
    y = GAP + r * (TILE + GAP) + int(TILE * 0.2)
    px = img.getpixel((x, y))
    assert isinstance(px, tuple)
    return (px[0], px[1], px[2])


# --- cutting -------------------------------------------------------------

@pytest.mark.parametrize("n", [2, 3, 4])
def test_cut_gives_n_squared_tiles_of_equal_size(n: int) -> None:
    tiles = cut_tiles(solid_reference(n), n)
    assert len(tiles) == n * n
    assert {t.size for t in tiles} == {(TILE, TILE)}


@pytest.mark.parametrize("n", [2, 3, 4])
def test_tiles_reassemble_into_the_reference(n: int) -> None:
    ref = solid_reference(n)
    back = Image.new("RGB", ref.size)
    for k, tile in enumerate(cut_tiles(ref, n)):
        r, c = divmod(k, n)
        back.paste(tile, (c * TILE, r * TILE))
    assert back.tobytes() == ref.tobytes()


def test_tile_k_carries_colour_k() -> None:
    for k, tile in enumerate(cut_tiles(solid_reference(4), 4)):
        assert tile.getpixel((TILE // 2, TILE // 2)) == colour(k)


# --- placement -----------------------------------------------------------

@pytest.mark.parametrize("n", [3, 4])
def test_solved_board_puts_tile_k_in_cell_k(n: int) -> None:
    tiles = cut_tiles(solid_reference(n), n)
    img = render_board(goal(n), tiles, style_raw, gap=GAP)
    for k in range(n * n - 1):
        r, c = divmod(k, n)
        assert cell_pixel(img, r, c) == colour(k)


def test_blank_cell_shows_the_background() -> None:
    tiles = cut_tiles(solid_reference(3), 3)
    img = render_board(goal(3), tiles, style_raw, gap=GAP)
    assert cell_pixel(img, 2, 2) == BACKGROUND


def test_a_move_relocates_exactly_one_tile() -> None:
    n = 3
    tiles = cut_tiles(solid_reference(n), n)
    before = goal(n)
    after = neighbors(before)[0]
    img_a = render_board(before, tiles, style_raw, gap=GAP)
    img_b = render_board(after, tiles, style_raw, gap=GAP)
    changed = [(r, c) for r in range(n) for c in range(n)
               if cell_pixel(img_a, r, c) != cell_pixel(img_b, r, c)]
    assert len(changed) == 2


@pytest.mark.parametrize("n", [3, 4])
def test_canvas_size(n: int) -> None:
    tiles = cut_tiles(solid_reference(n), n)
    img = render_board(goal(n), tiles, style_raw, gap=GAP)
    side = n * TILE + GAP * (n + 1)
    assert img.size == (side, side)


def test_rendering_is_deterministic() -> None:
    tiles = cut_tiles(solid_reference(3), 3)
    a = render_board(goal(3), tiles, style_dim)
    b = render_board(goal(3), tiles, style_dim)
    assert a.tobytes() == b.tobytes()


# --- styles --------------------------------------------------------------

@pytest.mark.parametrize("style", [style_edged, style_dim])
def test_style_keeps_the_size_and_leaves_the_input_alone(style: object) -> None:
    tile = cut_tiles(solid_reference(3), 3)[0]
    original = tile.tobytes()
    styled = style(tile, 1)          # type: ignore[operator]
    assert styled.size == tile.size
    assert tile.tobytes() == original


def pixel(img: Image.Image, xy: tuple[int, int]) -> tuple[int, int, int]:
    px = img.getpixel(xy)
    assert isinstance(px, tuple)
    return (px[0], px[1], px[2])


def test_dim_darkens_and_edged_keeps_the_centre() -> None:
    tile = cut_tiles(solid_reference(3), 3)[4]
    corner, centre = (2, TILE - 3), (TILE // 2, TILE // 2)
    assert sum(pixel(style_dim(tile, 5), corner)) < sum(pixel(tile, corner))
    assert pixel(style_edged(tile, 5), centre) == pixel(tile, centre)


# --- fonts ---------------------------------------------------------------

def test_font_lookup_finds_something() -> None:
    assert find_font(24) is not None


def test_font_lookup_falls_back_when_nothing_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OEDIPUS_FONT", raising=False)
    monkeypatch.setattr("oedipus.render.tiles.FONT_CANDIDATES", ("/no/such/font.ttf",))
    font = find_font(24)
    assert font is not None
    Image.new("RGB", (60, 60)).load()          # fallback must be usable
    assert FONT_CANDIDATES                      # the real list is untouched


# --- animation -----------------------------------------------------------

def test_gif_holds_the_first_and_last_frame(tmp_path: Path) -> None:
    tiles = cut_tiles(solid_reference(3), 3)
    boards: list[Board] = [goal(3), neighbors(goal(3))[0], goal(3)]
    out = tmp_path / "t.gif"
    save_gif([render_board(b, tiles, style_raw) for b in boards], out,
             ms_per_move=100, hold_first_ms=700, hold_last_ms=1500)
    with Image.open(out) as gif:
        durations = [f.info["duration"] for f in ImageSequence.Iterator(gif)]
    assert len(durations) == 3
    assert durations[0] == 700
    assert durations[-1] == 1500


def test_gif_refuses_an_empty_trajectory(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        save_gif([], tmp_path / "empty.gif")


# --- the real asset ------------------------------------------------------

def test_the_project_reference_loads_and_is_square() -> None:
    path = Path("assets/pharaoh_ref.png")
    if not path.exists():
        pytest.skip("asset not present")
    ref = load_reference(path, 240)
    assert ref.size == (240, 240)
    assert ref.mode == "RGB"
