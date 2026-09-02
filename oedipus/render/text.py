"""Board to text. Debugging only."""
from oedipus.core.board import BLANK, Board


def render_text(board: Board, blank: str = ".") -> str:
    return "\n".join(
        " ".join(blank if v == BLANK else str(v) for v in row) for row in board
    )


def render_row(boards: list[Board], labels: list[str], gap: str = "   ") -> str:
    """Several boards side by side, labelled. For comparing states."""
    blocks = [render_text(b).split("\n") for b in boards]
    width = len(blocks[0][0])
    out = [gap.join(str(x).center(width) for x in labels)]
    for r in range(len(boards[0])):
        out.append(gap.join(b[r] for b in blocks))
    return "\n".join(out)
