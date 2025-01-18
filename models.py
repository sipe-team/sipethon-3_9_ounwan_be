from sqlalchemy import Column, Integer, String

from database import Base


class ForecastUser(Base):
    __tablename__ = "ForecastUser"

    id = Column(String(100), primary_key=True, index=True)
    health_score = Column(Integer)
    love_score = Column(Integer)
    money_score = Column(Integer)
    job_score = Column(Integer)
    health_desc = Column(String(1000))
    love_desc = Column(String(1000))
    money_desc = Column(String(1000))
    job_desc = Column(String(1000))
    health_cover = Column(String(1000))
    love_cover = Column(String(1000))
    money_cover = Column(String(1000))
    job_cover = Column(String(1000))