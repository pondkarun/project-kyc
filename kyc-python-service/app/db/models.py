from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .database import Base
import uuid
from datetime import datetime

class KYCRequest(Base):
    __tablename__ = "kyc_requests"

    kyc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Text, nullable=False)
    images = Column(JSONB)
    result = Column(JSONB)