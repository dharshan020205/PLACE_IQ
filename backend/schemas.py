from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Feature Schema
class StudentFeatures(BaseModel):
    student_id: Optional[int] = Field(None, description="Optional ID to save the prediction")
    cgpa: float = Field(..., ge=5.5, le=9.5)
    coding_score: int = Field(..., ge=0, le=100)
    aptitude_score: int = Field(..., ge=0, le=100)
    communication_score: int = Field(..., ge=0, le=100)
    skills_count: int = Field(..., ge=1, le=10)
    projects_count: int = Field(..., ge=0, le=5)
    internships_count: int = Field(..., ge=0, le=3)
    backlogs: int = Field(..., ge=0, le=5)

class PredictionLogOut(BaseModel):
    id: int
    student_id: Optional[int]
    cgpa: float
    coding_score: int
    aptitude_score: int
    communication_score: int
    skills_count: int
    projects_count: int
    internships_count: int
    backlogs: int
    prediction_result: str
    probability: float
    rule_override: bool
    timestamp: datetime

    class Config:
        from_attributes = True

class StudentWithPredictions(StudentOut):
    predictions: List[PredictionLogOut] = []

class ReportSummary(BaseModel):
    total_students: int
    total_predictions: int
    average_probability: float
