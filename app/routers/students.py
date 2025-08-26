from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import models
from schemas import StudentCreate, StudentUpdate, StudentOut
from deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[StudentOut])
def list_students(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Student).filter(models.Student.owner_id == current_user.id).all()

@router.post("/", response_model=StudentOut, status_code=201)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    student = models.Student(
        first_name=student_in.first_name,
        last_name=student_in.last_name,
        index_number=student_in.index_number,
        program=student_in.program,
        level=student_in.level,
        owner_id=current_user.id,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == student_id, models.Student.owner_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, student_in: StudentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == student_id, models.Student.owner_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.first_name = student_in.first_name
    student.last_name = student_in.last_name
    student.index_number = student_in.index_number
    student.program = student_in.program
    student.level = student_in.level

    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == student_id, models.Student.owner_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None
