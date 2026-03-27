from sqlalchemy import Column, BigInteger, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class ActivityMetric(Base):
    __tablename__ = "activity_metrics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    activity_id = Column(BigInteger, ForeignKey("activities.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    metric_name = Column(String)
    value = Column(Float)