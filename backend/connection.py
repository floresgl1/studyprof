from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime

import os 
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PASS=os.getenv("POSTGRES_PASS")
POSTGRES_USER=os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@localhost/studyprof")

if not POSTGRES_USER or not POSTGRES_PASS:
    raise ValueError("POSTGRES_USER or POSTGRES_PASS is not set in the environment variables")


metadata_obj = MetaData()


users = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_name", String, nullable=False),
    Column("email", String, nullable=False)
)

subjects = Table(
    "subjects",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("topic", String),
    Column("sub_topic", String),
    Column("short_description", String)
)

quizzes = Table(
    "quizzes",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("subject_id", Integer, ForeignKey("subjects.id")),
    Column("date", DateTime),
    Column("proficiency", String),
    Column("question", String),
    Column("answer", String)
)



metadata_obj.create_all(engine)  # Create all tables defined in the metadata
