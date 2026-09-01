from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
#import tables from connection.py

from connection import users, subjects, quizzes, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert

app = FastAPI()

# database setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserCreate(BaseModel):
    user_name: str
    email:str

class SubjectCreate(BaseModel):
    user_id: int
    topic: str
    sub_topic: str 
    short_description: str

class QuizCreate(BaseModel):
    user_id: int
    subject_id: int
    date: datetime 
    proficiency: str
    question: str 
    answer: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
async def receive_data(data: UserCreate, db: Session = Depends(get_db)):
    
    new_user = users.insert().values(user_name=data.user_name, email=data.email)
    db.execute(new_user)
    db.commit()
    
    return {
        "status": "success",
        "received_data": data,
    }

@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users_list = users.select()
    users_list = db.execute(users_list)

    rows = users_list.fetchall()

    rows_list = [row._asdict() for row in rows]

    return {
        "status": "success",
        "users_list": rows_list
    }

@app.post("/subjects/")
async def receive_data(data: SubjectCreate, db: Session = Depends(get_db)):
    new_subject = subjects.insert().values(
        user_id=data.user_id,
        topic=data.topic,
        sub_topic=data.sub_topic,
        short_description=data.short_description
    )
    db.execute(new_subject)
    db.commit()

    return {
        "status": "success",
        "received_data": data,
    }

@app.get("/subjects/")
async def get_subjects(db: Session = Depends(get_db)):
    subjects_list = subjects.select()
    subjects_list = db.execute(subjects_list)

    rows = subjects_list.fetchall()

    rows_list = [row._asdict() for row in rows]

    return {
        "status": "success",
        "subjects_list": rows_list
    }

    
    
    
