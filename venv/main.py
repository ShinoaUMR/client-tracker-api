from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Client Tracker API")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully!"}