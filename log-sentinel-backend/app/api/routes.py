from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.log import Alert as AlertSchema
from app.schemas.log import LogEntry as LogEntrySchema
from app.schemas.log import Report as ReportSchema
from app.services.log_service import LogService


router = APIRouter()


@router.get("/logs", response_model=List[LogEntrySchema])
def get_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = LogService(db)
    return service.get_logs(skip=skip, limit=limit)


@router.get("/alerts", response_model=List[AlertSchema])
def get_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = LogService(db)
    return service.get_alerts(skip=skip, limit=limit)


@router.get("/reports", response_model=ReportSchema)
def generate_report(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = LogService(db)
    report_data = service.generate_report(skip=skip, limit=limit)
    return ReportSchema.model_validate(report_data)


@router.get("/report/csv")
def generate_report_csv(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = LogService(db)
    csv_content = service.generate_csv_report(skip=skip, limit=limit)
    headers = {"Content-Disposition": "attachment; filename=log_report.csv"}
    return StreamingResponse(iter([csv_content]), media_type="text/csv", headers=headers)


@router.get("/status")
def check_status():
    return {"status": "running"}