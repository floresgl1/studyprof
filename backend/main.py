from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
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
    
    
    
