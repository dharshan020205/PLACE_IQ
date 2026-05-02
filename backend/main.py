from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import statistics

from .database import get_db, Base, engine
from .model_service import model_service
from .models import Student, PredictionLog, User
from .schemas import (
    StudentFeatures, PredictionLogOut, StudentCreate, StudentOut, 
    StudentWithPredictions, ReportSummary, Token
)
from .auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password

app = FastAPI(title="PlaceIQ API", version="1.0")

import os
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Endpoints
@app.post("/v1/auth/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/v1/auth/refresh", response_model=Token)
def refresh_token(current_user = Depends(get_current_user)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Student CRUD (Protected)
@app.post("/v1/students", response_model=StudentOut)
def create_student(student: StudentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_student = db.query(Student).filter(Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_student = Student(name=student.name, email=student.email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/v1/students/{student_id}", response_model=StudentWithPredictions)
def get_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Reports (Protected)
@app.get("/v1/reports/summary", response_model=ReportSummary)
def get_report_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    total_students = db.query(Student).count()
    total_predictions = db.query(PredictionLog).count()
    
    if total_predictions == 0:
        avg_prob = 0.0
    else:
        probs = [p.probability for p in db.query(PredictionLog.probability).all()]
        avg_prob = statistics.mean(probs)
        
    return ReportSummary(
        total_students=total_students,
        total_predictions=total_predictions,
        average_probability=round(avg_prob, 4)
    )

# Prediction Endpoint (Unprotected)
@app.get("/v1/model/info")
def get_model_info():
    return model_service.get_model_info()

@app.post("/v1/predict")
def predict_placement(features: StudentFeatures, db: Session = Depends(get_db)):
    try:
        # Perform inference
        result = model_service.predict(features.model_dump(exclude={"student_id"}))
        
        # Save to DB if student_id is provided
        if features.student_id is not None:
            student = db.query(Student).filter(Student.id == features.student_id).first()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
                
            log = PredictionLog(
                student_id=features.student_id,
                cgpa=features.cgpa,
                coding_score=features.coding_score,
                aptitude_score=features.aptitude_score,
                communication_score=features.communication_score,
                skills_count=features.skills_count,
                projects_count=features.projects_count,
                internships_count=features.internships_count,
                backlogs=features.backlogs,
                prediction_result=result["prediction"],
                probability=result["probability"],
                rule_override=result["rule_override"]
            )
            db.add(log)
            db.commit()
            
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
