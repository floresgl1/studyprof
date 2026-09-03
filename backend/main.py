from fastapi import FastAPI, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import fitz
import os 
from openai import OpenAI

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY"),
)
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

def extract_text(file_bytes):

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += (page.get_text())

    doc.close()
    return text 

def generate_question(text):
    # define Nebius API structure and generate system prompt
    response = client.chat.completions.create(
        model="Nemotron-3.5-Lightning",
        messages=[
            {"role": "system", "content": "You are an expert educator and quiz designer. Your task is to generate high-quality, accurate quizzes with clear answers based on the provided topic, text, or source material.\n\nFollow these strict rules:\n1. Role & Tone: Maintain a neutral, professional, and clear academic tone. Avoid ambiguous or trick questions.\n2. Structure: Return the response in a json format with fields, proficiency, question, answer. \n3. Formats: \n   - Provide a mix of multiple-choice questions (MCQs), true/false, or short answer as requested.\n   - For MCQs, provide exactly four options labeled A, B, C, and D, with only one correct choice and three plausible distractors.\n4. Example output:[{"proficiency": "...", "question": "...", "answer": "..."}]"},
            {"role": "user", "content": text},
        ]
    )
    return response.choices[0].message.content



@app.post("/users/")
async def receive_users(data: UserCreate, db: Session = Depends(get_db)):
    
    new_user = users.insert().values(
    user_name=data.user_name, 
    email=data.email
    )
    db.execute(new_user)
    db.commit()
    
    return {
        "status": "success",
        "received_users": data,
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
async def receive_subjects(data: SubjectCreate, db: Session = Depends(get_db)):
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
        "received_subjects": data,
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


@app.post("/quizzes/")
async def receive_quizzes(data: QuizCreate, db: Session = Depends(get_db)):
    new_quiz = quizzes.insert().values(
        user_id=data.user_id,
        subject_id=data.subject_id,
        date=data.date,
        proficiency=data.proficiency,
        question=data.question,
        answer=data.answer
    )
    db.execute(new_quiz)
    db.commit()

    return {
        "status": "success",
        "received_quizzes": data,
    }

@app.get("/quizzes/")
async def get_quizzes(db: Session = Depends(get_db)):
    quizzes_list = quizzes.select()
    quizzes_list = db.execute(quizzes_list)

    rows = quizzes_list.fetchall()

    rows_list = [row._asdict() for row in rows]

    return {
        "status": "success",
        "quizzes_list": rows_list
    }
    

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    content = extract_text(content)
    return {
        "filename": file.filename,
        "content": content
    }
    
    
