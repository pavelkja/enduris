from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, BigInteger, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Activity(Base):
    __tablename__ = "activities"

    # Strava activity ID
    id = Column(BigInteger, primary_key=True, index=True)

    # user relation
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # activity info
    sport_type = Column(String, nullable=False)

    start_date = Column(DateTime, nullable=False, index=True)

    # summary stats
    distance = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)

    elevation_gain = Column(Float)

    avg_speed = Column(Float)
    max_speed = Column(Float)

    avg_hr = Column(Float)
    max_hr = Column(Float)

    has_heartrate = Column(Boolean, default=False)

    # pipeline status
    streams_imported = Column(Boolean, default=False)
    metrics_computed = Column(Boolean, default=False)

    # metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    streams_imported = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="activities")
    
    __table_args__ = (
        Index("idx_activities_user_date", "user_id", "start_date"),
    )