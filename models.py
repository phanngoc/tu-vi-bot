import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, Enum, ForeignKey, Date, Time, TIMESTAMP, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    uuid = Column(String, nullable=True) 
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Zodiac(Base):
    __tablename__ = 'zodiac'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)

class Star(Base):
    __tablename__ = 'stars'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(String(50))
    element = Column(String(50))
    description = Column(Text)
    sub_type = Column(String(50), nullable=True)  # thêm column "loại phụ tinh"

class CanChiType(enum.Enum):
    ThienCan = "Thiên Can"
    DiaChi = "Địa Chi"

class CanChi(Base):
    __tablename__ = 'can_chi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(CanChiType), nullable=False)
    name = Column(String(50), nullable=False)
    element = Column(String(50))
    description = Column(Text)

class MasterData(Base):
    __tablename__ = 'master_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    can_chi_id = Column(Integer, ForeignKey('can_chi.id'), nullable=False)
    zodiac_id = Column(Integer, ForeignKey('zodiac.id'), nullable=False)
    star_id = Column(Integer, ForeignKey('stars.id'), nullable=False)
    rule = Column(Text)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    birth_hour = Column(Time)
    gender = Column(Enum('Nam', 'Nữ', name='gender'))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

class UserZodiac(Base):
    __tablename__ = 'user_zodiac'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    zodiac_id = Column(Integer, ForeignKey('zodiac.id'), nullable=False)
    star_id = Column(Integer, ForeignKey('stars.id'), nullable=False)


# Create an engine and a session
engine = create_engine('sqlite:///tuvi.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
