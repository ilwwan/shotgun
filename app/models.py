from sqlalchemy import Column, Integer, String

from db import Base

class ShotgunEntry(Base):
    __tablename__ = "shotgun_entry"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)

class ShotgunCotisantEntry(Base):
    __tablename__ = "shotgun_cotisant_entry"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    vr_username = Column(String, unique=True, index=True)