# Log Sentinel Backend

A portable FastAPI + SQLAlchemy + SQLite backend for collecting logs, retrieving alerts, and generating reports. Designed to run locally, in Codespaces, or in containers with minimal setup.

## Features

- Log and alert retrieval endpoints (`/logs`, `/alerts`)
- CSV report generation (`/report/csv`)
- Health endpoint (`/status`)
- Async benchmark tool and simple demo client

## Project Structure

```
log-sentinel-backend
├── app/
│   ├── main.py            # FastAPI app and startup
│   ├── api/routes.py      # API endpoints
│   ├── db/models.py       # SQLAlchemy models (LogEntry, Alert)
│   ├── db/session.py      # Engine, SessionLocal, Base, create_db_and_tables()
│   ├── core/config.py     # Settings via pydantic-settings
│   ├── schemas/log.py     # Pydantic schemas (from_attributes=True)
│   └── services/log_service.py  # Data access and report helpers
├── benchmark.py           # Async benchmark for endpoints
├── demo.py                # Tiny client hitting core endpoints
├── requirements.txt       # Dependencies
└── tests/                 # pytest tests (sample)
```

## Setup (Linux/macOS/Windows/Codespaces)

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API docs: http://127.0.0.1:8000/docs
- DB file: `logs.db` (SQLite, created on first run)

## Configuration

Values come from environment variables (via `pydantic-settings`). Defaults are reasonable for local use.

- `DATABASE_URL` (default: `sqlite:///./logs.db`)
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`

Create a `.env` alongside the app for overrides:

```
DATABASE_URL=sqlite:///./logs.db
```

## Endpoints (summary)

- `GET /status` – health check
- `GET /logs` – list logs (pagination via `skip`, `limit`)
- `GET /alerts` – list alerts (pagination via `skip`, `limit`)
- `GET /report/csv` – stream CSV of logs (id, timestamp, level, message)

## Demo client

```
python demo.py
```

Prints status, logs, alerts, and CSV output.

## Benchmark

Measure latency and throughput per endpoint:

```
python benchmark.py --runs 50 --concurrency 5
```

Output example:

```
/status      count= 50 conc= 5 latency_mean=7.35ms latency_p95=11.99ms throughput=600.6 req/s
/logs        count= 50 conc= 5 latency_mean=12.83ms latency_p95=22.61ms throughput=365.9 req/s
/alerts      count= 50 conc= 5 latency_mean=14.00ms latency_p95=20.33ms throughput=330.2 req/s
/report/csv  count= 50 conc= 5 latency_mean=15.56ms latency_p95=22.14ms throughput=300.3 req/s
```

Flags:

- `--base-url` (default: http://127.0.0.1:8000)
- `--runs` total requests per endpoint
- `--concurrency` concurrent requests
- `--endpoints` custom list (e.g., `--endpoints /logs /alerts`)

## Testing

```
pytest
```

Place tests in `tests/` with filenames like `test_*.py`.

## Portability notes

- Pure Python + SQLite → works on Linux/macOS/Windows and in Codespaces.
- To use Postgres/MySQL, set `DATABASE_URL` accordingly and install the driver (e.g., `psycopg` or `mysqlclient`).
- For containers, bind to `0.0.0.0` and mount a volume for `logs.db` to persist data.

## Troubleshooting

- `ModuleNotFoundError: fastapi` → `pip install -r requirements.txt`
- `No module named 'app'` → run commands from the `log-sentinel-backend` directory
- SQLite threading error → we configure `check_same_thread=False` for SQLite in dev

---

MIT License