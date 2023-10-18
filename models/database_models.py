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


class TimeTable(CommonBase):
    __tablename__ = 'timetable'

    type_duty = Column(String(100))
    data = Column(String(100))
    user_id = Column(Text, ForeignKey("users.id"), nullable=False)
    user = relationship('Users')
