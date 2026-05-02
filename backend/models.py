from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    predictions = relationship("PredictionLog", back_populates="student")

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    
    # Inputs
    cgpa = Column(Float, nullable=False)
    coding_score = Column(Integer, nullable=False)
    aptitude_score = Column(Integer, nullable=False)
    communication_score = Column(Integer, nullable=False)
    skills_count = Column(Integer, nullable=False)
    projects_count = Column(Integer, nullable=False)
    internships_count = Column(Integer, nullable=False)
    backlogs = Column(Integer, nullable=False)
    
    # Outputs
    prediction_result = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    rule_override = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="predictions")
