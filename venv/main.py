from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Client Tracker API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- NEW ENDPOINTS BELOW ---

# 1. Create a new client
@app.post("/clients", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    # Check if email already exists to prevent duplicates
    db_client = db.query(models.Client).filter(models.Client.email == client.email).first()
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create and save the new client
    new_client = models.Client(name=client.name, email=client.email)
    db.add(new_client)
    db.commit()
    db.refresh(new_client) # This gets the new ID from the database
    return new_client

# 2. Get all clients
@app.get("/clients", response_model=list[schemas.ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()