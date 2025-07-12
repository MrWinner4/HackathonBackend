# db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://hackathon_ff4r_user:yVkNa0z7DxhpV7Yy6QaUrQjqZ3qoKPlh@dpg-d1p5ioripnbc73fm4fm0-a.virginia-postgres.render.com/hackathon_ff4r"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
