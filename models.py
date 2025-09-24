from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    username = Column(String)
    encrypted_password = Column(String)

class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    master_password_hash = Column(String)