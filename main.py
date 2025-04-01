from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:kyTYqlZQCCFLPKhzLGEtkLwOtPiQOMZH@tramway.proxy.rlwy.net:23726/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobile = Column(String, unique=True, index=True)
    location = Column(String)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    mobile: str
    location: str

@app.post("/register")
def register_user(user: UserCreate):
    session = SessionLocal()
    new_user = User(name=user.name, mobile=user.mobile, location=user.location)
    session.add(new_user)
    session.commit()
    session.close()
    return {"message": "User registered successfully"}
