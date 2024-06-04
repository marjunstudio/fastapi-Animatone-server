from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
# from models.composers import Composer

Base = declarative_base()

class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text, nullable=True)
    composer_id = Column(Integer, ForeignKey("composers.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    composer = relationship("Composer", backref="musics")
