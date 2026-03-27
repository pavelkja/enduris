from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    strava_athlete_id = Column(BigInteger, unique=True, index=True)

    name = Column(String)

    access_token = Column(String)
    refresh_token = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # timestamp poslední synchronizace
    last_sync = Column(DateTime(timezone=True), nullable=True)

    # relationship na aktivity
    activities = relationship("Activity", back_populates="user")

    # hr zones ze Stravy
    hr_zones = Column(JSONB)
    #max hr v tabulce
    max_hr = Column(Integer)