import csv
import io
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models import LogEntry, Alert

import logging

logger = logging.getLogger(__name__)

class LogService:
    def __init__(self, db: Session):
        self.db = db

    def ingest_log(self, log_data: dict) -> LogEntry:
        log_entry = LogEntry(**log_data)
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)
        logger.info("Log entry created", extra={"log_id": log_entry.id})
        return log_entry

    def get_logs(self, skip: int = 0, limit: int = 100) -> List[LogEntry]:
        logs = (
            self.db.query(LogEntry)
            .order_by(LogEntry.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        logger.debug("Fetched logs", extra={"count": len(logs)})
        return logs

    def get_alerts(self, skip: int = 0, limit: int = 100) -> List[Alert]:
        alerts = (
            self.db.query(Alert)
            .order_by(Alert.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        logger.debug("Fetched alerts", extra={"count": len(alerts)})
        return alerts

    def delete_log(self, log_id: int) -> Optional[LogEntry]:
        log_entry = self.db.query(LogEntry).filter(LogEntry.id == log_id).first()
        if not log_entry:
            logger.warning("Log entry not found", extra={"log_id": log_id})
            return None

        self.db.delete(log_entry)
        self.db.commit()
        logger.info("Log entry deleted", extra={"log_id": log_id})
        return log_entry

    def generate_report(self, skip: int = 0, limit: int = 100) -> dict:
        logs = self.get_logs(skip=skip, limit=limit)
        report = {
            "logs": logs,
            "generated_at": datetime.utcnow(),
        }
        logger.debug("Generated report", extra={"log_count": len(logs)})
        return report

    def generate_csv_report(self, skip: int = 0, limit: int = 100) -> str:
        logs = self.get_logs(skip=skip, limit=limit)
        buffer = io.StringIO()
        fieldnames = ["id", "timestamp", "level", "message"]
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        writer.writeheader()
        for entry in logs:
            writer.writerow(
                {
                    "id": entry.id,
                    "timestamp": entry.timestamp.isoformat() if entry.timestamp else "",
                    "level": entry.level,
                    "message": entry.message,
                }
            )
        logger.debug("Generated CSV report", extra={"log_count": len(logs)})
        return buffer.getvalue()