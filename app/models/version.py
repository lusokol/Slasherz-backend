from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database import Base

class DataPackVersion(Base):
    __tablename__ = "datapack_version"

    version = Column(String, primary_key=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
    