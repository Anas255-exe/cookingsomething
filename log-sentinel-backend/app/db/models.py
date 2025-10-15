from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    level = Column(String(50), nullable=False)

    alerts = relationship("Alert", back_populates="log_entry")

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    log_entry_id = Column(Integer, ForeignKey('log_entries.id'))
    alert_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    log_entry = relationship("LogEntry", back_populates="alerts")