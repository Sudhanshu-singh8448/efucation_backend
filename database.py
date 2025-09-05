import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database configuration for Neon PostgreSQL
# Get connection string from environment variable for security
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/career_db')

# Validate that DATABASE_URL is set
if not DATABASE_URL or DATABASE_URL == 'postgresql://localhost:5432/career_db':
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it to your Neon PostgreSQL connection string.\n"
        "Example: export DATABASE_URL='postgresql://username:password@hostname/database?sslmode=require'"
    )

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Career Test Session Model
class CareerSession(Base):
    __tablename__ = "career_sessions"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Integer, default=0)  # 0 = in progress, 1 = completed
    current_question = Column(Integer, default=0)
    realistic_score = Column(Integer, default=0)
    investigative_score = Column(Integer, default=0)
    artistic_score = Column(Integer, default=0)
    social_score = Column(Integer, default=0)
    enterprising_score = Column(Integer, default=0)
    conventional_score = Column(Integer, default=0)

# Career Test Answers Model
class CareerAnswer(Base):
    __tablename__ = "career_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    question_number = Column(Integer)
    question_text = Column(Text)
    riasec_type = Column(String)
    answer_value = Column(Integer)  # 1-5 scale
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Database tables created successfully!")
