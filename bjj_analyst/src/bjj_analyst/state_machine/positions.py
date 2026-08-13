from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class LabelConfig:
    states: tuple[str, ...]
    events: tuple[str, ...]
    position_rank: dict[str, int]
    min_state_duration_s: float
    window_length_s: float
    window_hop_s: float
    target_fps: int

    @classmethod
    def from_yaml(cls, path: Path) -> LabelConfig:
        raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
        window = raw.get("window") or {}
        return cls(
            states=tuple(raw["states"]),
            events=tuple(raw["events"]),
            position_rank={str(k): int(v) for k, v in raw["position_rank"].items()},
            min_state_duration_s=float(raw.get("min_state_duration_s", 0.8)),
            window_length_s=float(window.get("length_s", 2.0)),
            window_hop_s=float(window.get("hop_s", 0.5)),
            target_fps=int(window.get("target_fps", 20)),
        )


def rank_for(state: str, ranks: dict[str, int]) -> int:
    return int(ranks.get(state, 0))


def is_improvement(from_state: str, to_state: str, ranks: dict[str, int]) -> bool:
    """Return True if to_state ranks strictly better than from_state."""
    return rank_for(to_state, ranks) > rank_for(from_state, ranks)
