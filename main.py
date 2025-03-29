from fastapi import FastAPI, HTTPException, Form
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()

# Load Railway PostgreSQL credentials from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not set. Add it in Railway's environment variables.")

# Set up the database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mobile = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# API to register a user
@app.post("/register")
def register_user(name: str = Form(...), mobile: str = Form(...), location: str = Form(...)):
    session = SessionLocal()
    existing_user = session.query(User).filter(User.mobile == mobile).first()
    
    if existing_user:
        session.close()
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    new_user = User(name=name, mobile=mobile, location=location)
    session.add(new_user)
    session.commit()
    session.close()
    
    return {"message": "User registered successfully!"}
