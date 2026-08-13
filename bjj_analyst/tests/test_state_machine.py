from pathlib import Path

from bjj_analyst.state_machine import LabelConfig, WindowPrediction, aggregate_stats, build_timeline, is_improvement


ROOT = Path(__file__).resolve().parents[1]
LABELS = ROOT / "configs" / "labels_nogi.yaml"


def test_closed_guard_to_mount_is_improvement():
    cfg = LabelConfig.from_yaml(LABELS)
    assert is_improvement("closed_guard", "mount", cfg.position_rank)
    assert not is_improvement("mount", "open_guard", cfg.position_rank)


def test_build_timeline_smooths_short_flicker():
    cfg = LabelConfig.from_yaml(LABELS)
    preds = [
        WindowPrediction(0.0, 2.0, "closed_guard"),
        WindowPrediction(0.5, 2.5, "closed_guard"),
        WindowPrediction(1.0, 3.0, "mount"),
        WindowPrediction(2.0, 4.0, "closed_guard"),
        WindowPrediction(4.0, 6.0, "closed_guard"),
        WindowPrediction(6.0, 8.0, "mount", event="sweep", event_confidence=0.9),
        WindowPrediction(6.5, 8.5, "mount"),
        WindowPrediction(8.0, 10.0, "mount"),
    ]
    timeline = build_timeline(preds, cfg)
    assert timeline.segments
    assert timeline.segments[0].state == "closed_guard"
    assert any(s.state == "mount" for s in timeline.segments)
    assert any(e.type == "sweep" for e in timeline.events)


def test_aggregate_stats_sums_durations():
    cfg = LabelConfig.from_yaml(LABELS)
    preds = [
        WindowPrediction(0.0, 3.0, "closed_guard"),
        WindowPrediction(1.0, 4.0, "closed_guard"),
        WindowPrediction(3.0, 6.0, "mount"),
        WindowPrediction(4.0, 7.0, "mount"),
        WindowPrediction(6.0, 9.0, "mount"),
    ]
    timeline = build_timeline(preds, cfg)
    stats = aggregate_stats(timeline)
    assert stats["time_in_state_s"]["closed_guard"] > 0
    assert stats["time_in_state_s"]["mount"] > 0
