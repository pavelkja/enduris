from sqlalchemy import Column, BigInteger, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ActivityStream(Base):
    __tablename__ = "activity_streams"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    activity_id = Column(BigInteger, ForeignKey("activities.id"), index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    stream_type = Column(String)

    data = Column(JSONB)

    activity = relationship("Activity")


Index(
    "idx_activity_streams_activity_id",
    ActivityStream.activity_id
)