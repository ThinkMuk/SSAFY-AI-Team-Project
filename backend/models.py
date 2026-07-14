from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class SigunguCode(Base):
    __tablename__ = "sigungu_codes"

    sigungu_code = Column(String, primary_key=True, index=True)  # e.g., "350"
    sido_name = Column(String, nullable=False, default="서울특별시")
    sigungu_name = Column(String, nullable=False)  # e.g., "성동구"

    places = relationship("Place", back_populates="sigungu")


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)  # e.g., "성수동"
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    sigungu_code = Column(String, ForeignKey("sigungu_codes.sigungu_code"), nullable=False)

    sigungu = relationship("SigunguCode", back_populates="places")
    posts = relationship("Post", back_populates="place")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    nickname = Column(String, nullable=False, default="익명")
    password = Column(String, nullable=False)  # hashed password
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    place = relationship("Place", back_populates="posts")
