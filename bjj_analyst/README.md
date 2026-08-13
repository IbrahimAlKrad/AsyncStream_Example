# BJJ Analyst (No-Gi CLI)

Offline-Pipeline: No-Gi-Video → Pose → temporale Erkennung → State Machine → Stats/Timeline → LLM-Report.

## Start hier

1. Lies den Architektur-Leitfaden: [ARCHITECTURE.md](./ARCHITECTURE.md)
2. Python 3.11+ Umgebung anlegen
3. Paket editierbar installieren und CLI prüfen:

```bash
cd bjj_analyst
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
bjj-analyst --help
```

## MVP-Befehl (Zielbild)

```bash
bjj-analyst analyze match.mp4 --out runs/match01 --meta meta.json
```

Aktuell: CLI-Gerüst + State-Machine-Stub. Perception/ML folgen der Reihenfolge in `ARCHITECTURE.md` §6.

## Scope

- CLI, offline, No-Gi
- Kein Live, keine Web-UI im MVP
