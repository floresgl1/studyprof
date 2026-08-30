from sqlalchemy import create_engine

import os 
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PASS=os.getenv("POSTGRES_PASS")
POSTGRES_USER=os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@localhost/studyprof")