from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class LogEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    timestamp: datetime
    level: str
    message: str


class Alert(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    log_entry_id: int
    alert_type: str
    description: Optional[str] = None
    created_at: datetime


class Report(BaseModel):
    logs: List[LogEntry]
    generated_at: datetime = Field(default_factory=datetime.utcnow)