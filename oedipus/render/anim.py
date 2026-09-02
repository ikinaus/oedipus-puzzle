"""Frames to an animation."""
from pathlib import Path

from PIL import Image


def save_gif(frames: list[Image.Image], path: str | Path, ms_per_move: int = 420,
             hold_first_ms: int = 900, hold_last_ms: int = 2200) -> None:
    """Write a GIF, holding the first and last frames longer.

    Without the holds the loop restarts instantly and neither the starting
    position nor the result can be seen.
    """
    if not frames:
        raise ValueError("no frames to save")
    durations = [ms_per_move] * len(frames)
    durations[0] = hold_first_ms
    durations[-1] = hold_last_ms
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)
