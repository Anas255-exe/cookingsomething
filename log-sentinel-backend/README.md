# Log Sentinel Backend

Log Sentinel is a backend application built with FastAPI and SQLite, designed to manage and monitor logs efficiently. This project provides a modular structure that allows for easy maintenance and scalability.

## Features

- **Log Management**: Ingest and parse logs from various sources.
- **Alerting System**: Generate alerts based on specific log patterns or conditions.
- **Reporting**: Generate reports for log analysis and monitoring.
- **Service Status Check**: API endpoints to check the health and status of services.

## Project Structure

```
log-sentinel-backend
├── app
│   ├── main.py               # Entry point of the FastAPI application
│   ├── api                   # Module for API routes
│   │   ├── __init__.py
│   │   └── routes.py         # API endpoints for logs and alerts
│   ├── db                    # Database models and session management
│   │   ├── __init__.py
│   │   ├── models.py         # SQLAlchemy models for LogEntry and Alert
│   │   └── session.py        # Database session management
│   ├── core                  # Core application configuration
│   │   ├── __init__.py
│   │   └── config.py         # Configuration settings
│   ├── services              # Business logic and services
│   │   ├── __init__.py
│   │   └── log_service.py    # Log ingestion and parsing logic
│   ├── schemas               # Pydantic models for request/response validation
│   │   ├── __init__.py
│   │   └── log.py            # Models for log entries and alerts
│   └── utils                 # Utility functions
│       ├── __init__.py
│       └── helpers.py        # Helper functions for various tasks
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
└── alembic.ini              # Database migration configuration
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd log-sentinel-backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Configure the database connection in `app/core/config.py`.
   - Run migrations using Alembic.

## Usage

To start the FastAPI application, run:
```
uvicorn app.main:app --reload
```

You can access the API documentation at `http://localhost:8000/docs`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.