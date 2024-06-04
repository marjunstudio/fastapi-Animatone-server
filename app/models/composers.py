from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.musics import Music

Base = declarative_base()

class Composer(Base):
  __tablename__ = "composers"

  id = Column(Integer, primary_key=True)
  name = Column(String(50))
  furigana = Column(String(50))
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
  musics = relationship("Music", backref="composer")

