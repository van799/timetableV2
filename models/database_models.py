import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, UUID, Text

from sqlalchemy.orm import relationship, DeclarativeBase


class CommonBase(DeclarativeBase):
    # postgres
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # sqlite
    id = Column(
        'id',
        String(length=128),
        default=lambda: str(uuid.uuid4()),
        primary_key=True)
    deleted = Column(Boolean, default=False)


class Users(CommonBase):
    __tablename__ = "users"

    username = Column(String(100), unique=True)
    hashed_password = Column(String(100), nullable=False)


class Event(CommonBase):
    __tablename__ = 'event'

    title = Column(String(100), unique=True)
    timetable = relationship("TimeTable")


class TimeTable(CommonBase):
    __tablename__ = 'timetable'

    start = Column(String(100))
    end = Column(String(100))
    title_id = Column(Text, ForeignKey("event.id"), nullable=True)
