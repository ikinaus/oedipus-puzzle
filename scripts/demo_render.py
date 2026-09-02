"""Render the solved board at both sizes, in both styles.

Run from the repository root:  python scripts/demo_render.py
"""
from pathlib import Path

from oedipus.core.board import goal
from oedipus.render.board import render_board
from oedipus.render.text import render_text
from oedipus.render.tiles import cut_tiles, load_reference, style_dim, style_edged

REF = Path("assets/pharaoh_ref.png")
OUT = Path("data")
TILE = 110


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for n in (3, 4):
        tiles = cut_tiles(load_reference(REF, TILE * n), n)
        for name, style in (("edged", style_edged), ("dim", style_dim)):
            path = OUT / f"board_{n}x{n}_{name}.png"
            render_board(goal(n), tiles, style).save(path)
            print(f"wrote {path}")
    print()
    print(render_text(goal(3)))


if __name__ == "__main__":
    main()
