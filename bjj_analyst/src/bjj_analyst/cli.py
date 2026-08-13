from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from bjj_analyst import __version__

app = typer.Typer(
    name="bjj-analyst",
    help="Offline No-Gi BJJ analysis: video → timeline/stats → report.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """BJJ Analyst CLI."""


@app.command("version")
def version() -> None:
    """Print package version."""
    typer.echo(__version__)


@app.command("analyze")
def analyze(
    video: Path = typer.Argument(..., exists=True, readable=True, help="Input match video"),
    out: Path = typer.Option(..., "--out", help="Run output directory"),
    meta: Optional[Path] = typer.Option(None, "--meta", help="Optional meta.json (athlete names, track IDs)"),
    config: Path = typer.Option(
        Path("configs/pipeline_default.yaml"),
        "--config",
        help="Pipeline YAML",
    ),
) -> None:
    """Run the full offline pipeline (stub: creates run folder + placeholder artefacts)."""
    out.mkdir(parents=True, exist_ok=True)
    (out / "debug").mkdir(exist_ok=True)

    timeline = {
        "fps": 20,
        "video": str(video),
        "meta": str(meta) if meta else None,
        "segments": [],
        "events": [],
        "status": "stub",
        "message": "Perception and temporal stages not wired yet. See ARCHITECTURE.md §6.",
    }
    stats = {
        "status": "stub",
        "athlete_a": {"time_in_state_s": {}, "events": {}, "position_improvements": []},
        "athlete_b": {"time_in_state_s": {}, "events": {}, "position_improvements": []},
        "transition_matrix": {},
    }

    _write_json(out / "timeline.json", timeline)
    _write_json(out / "stats.json", stats)
    (out / "report.md").write_text(
        "# BJJ Analyst Report (stub)\n\n"
        "Pipeline scaffolding only. Implement phases in ARCHITECTURE.md.\n",
        encoding="utf-8",
    )
    typer.echo(f"Stub run written to {out}")


@app.command("report")
def report(
    run_dir: Path = typer.Argument(..., exists=True, file_okay=False, help="Existing run directory"),
) -> None:
    """Regenerate LLM report from existing stats/timeline (stub)."""
    stats_path = run_dir / "stats.json"
    timeline_path = run_dir / "timeline.json"
    if not stats_path.exists() or not timeline_path.exists():
        raise typer.BadParameter("run directory must contain stats.json and timeline.json")
    report_path = run_dir / "report.md"
    report_path.write_text(
        "# BJJ Analyst Report (stub)\n\n"
        "LLM feedback not configured. Wire feedback/llm_report.py when ready.\n",
        encoding="utf-8",
    )
    typer.echo(f"Stub report written to {report_path}")


def _write_json(path: Path, payload: dict) -> None:
    import json

    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    app()
