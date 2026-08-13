from __future__ import annotations

from dataclasses import dataclass

from bjj_analyst.state_machine.positions import LabelConfig, is_improvement


@dataclass(frozen=True)
class WindowPrediction:
    """One temporal-model window output (seconds refer to video time)."""

    start_s: float
    end_s: float
    state: str
    confidence: float = 1.0
    event: str = "none"
    event_confidence: float = 0.0
    bottom: str | None = None
    top: str | None = None


@dataclass(frozen=True)
class Segment:
    start_s: float
    end_s: float
    state: str
    bottom: str | None = None
    top: str | None = None


@dataclass(frozen=True)
class Event:
    t_s: float
    type: str
    by: str | None
    from_state: str | None
    to_state: str | None


@dataclass
class Timeline:
    segments: list[Segment]
    events: list[Event]


def build_timeline(preds: list[WindowPrediction], config: LabelConfig) -> Timeline:
    """Smooth window predictions into segments and collect compatible events."""
    if not preds:
        return Timeline(segments=[], events=[])

    ordered = sorted(preds, key=lambda p: p.start_s)
    segments: list[Segment] = []
    events: list[Event] = []

    cur = ordered[0]
    seg_start = cur.start_s
    seg_state = cur.state
    seg_bottom = cur.bottom
    seg_top = cur.top
    seg_end = cur.end_s

    def close_segment() -> None:
        nonlocal seg_start, seg_state, seg_bottom, seg_top, seg_end
        if seg_end - seg_start >= config.min_state_duration_s or not segments:
            segments.append(
                Segment(
                    start_s=seg_start,
                    end_s=seg_end,
                    state=seg_state,
                    bottom=seg_bottom,
                    top=seg_top,
                )
            )

    for prev, nxt in zip(ordered, ordered[1:]):
        if nxt.event != "none" and nxt.event_confidence >= 0.5:
            events.append(
                Event(
                    t_s=nxt.end_s,
                    type=nxt.event,
                    by=None,
                    from_state=prev.state,
                    to_state=nxt.state,
                )
            )

        if nxt.state == seg_state and nxt.bottom == seg_bottom and nxt.top == seg_top:
            seg_end = max(seg_end, nxt.end_s)
            continue

        # Require minimum duration before accepting a change.
        if (nxt.start_s - seg_start) < config.min_state_duration_s:
            seg_end = max(seg_end, nxt.end_s)
            continue

        close_segment()
        seg_start = nxt.start_s
        seg_state = nxt.state
        seg_bottom = nxt.bottom
        seg_top = nxt.top
        seg_end = nxt.end_s

    close_segment()
    return Timeline(segments=segments, events=events)


def aggregate_stats(timeline: Timeline, config: LabelConfig | None = None) -> dict:
    """Build MVP stats dict from a timeline."""
    time_in_state: dict[str, float] = {}
    transition_matrix: dict[str, dict[str, int]] = {}

    for seg in timeline.segments:
        time_in_state[seg.state] = time_in_state.get(seg.state, 0.0) + (seg.end_s - seg.start_s)

    for a, b in zip(timeline.segments, timeline.segments[1:]):
        transition_matrix.setdefault(a.state, {})
        transition_matrix[a.state][b.state] = transition_matrix[a.state].get(b.state, 0) + 1

    event_counts: dict[str, int] = {}
    improvements: list[dict] = []
    ranks = config.position_rank if config is not None else {}
    for ev in timeline.events:
        event_counts[ev.type] = event_counts.get(ev.type, 0) + 1
        if ev.from_state and ev.to_state and ranks and is_improvement(ev.from_state, ev.to_state, ranks):
            improvements.append(
                {
                    "t_s": ev.t_s,
                    "from": ev.from_state,
                    "to": ev.to_state,
                    "via": ev.type,
                }
            )

    return {
        "time_in_state_s": time_in_state,
        "events": event_counts,
        "position_improvements": improvements,
        "transition_matrix": transition_matrix,
    }
