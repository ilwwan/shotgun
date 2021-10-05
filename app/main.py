from fastapi import FastAPI, Depends, HTTPException
import profiling_module as profile

from db import SessionLocal, engine
import schemas, models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone, timedelta
import requests
import random

models.Base.metadata.create_all(bind=engine)


SHOTGUN_COTISANT_TIME = datetime(2021, 9, 30, 12, 00)
RECAPTCHA_SECRET = "6LejcaQcAAAAAGpcX6D3rubls6xMcAOhERpiLZAJ"
MAX_COTISANTS = 1
MAX_EXTE = 400

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shotgun/", response_model=schemas.Shotgun)
def shotgun(entry: schemas.Shotgun, db: Session = Depends(get_db), recaptcha_response_token: str = ""):
    # TODO : check time
    # TODO : test recaptcha
    # TODO : enter shotgun into db
    return entry.dict()

@app.post("/shotgun-cotisant/", response_model=schemas.ShotgunCotisant)
def shotgun_cotisant(entry: schemas.ShotgunCotisant, db: Session = Depends(get_db), recaptcha_response_token: str = ""):
    # profiling
    # with profile.profiled():
    # Randomly reject requests
    if random.getrandbits(1):
        raise HTTPException(429, "Retry later")
    # check time
    if datetime.now() < SHOTGUN_COTISANT_TIME:
        raise HTTPException(400, "Le shotgun n'est pas encore ouvert")
    # TODO : test recaptcha
    params = {
        "secret": RECAPTCHA_SECRET,
        "response": recaptcha_response_token
    }
    res = requests.post("https://www.google.com/recaptcha/api/siteverify", data=params).json()
    # Bypassing recaptcha for tests
    """if not res["success"] or res["action"] != "shotgun" or res["score"] < 0.5:
        error = res["error-codes"][0]
        raise HTTPException(403, f"La validation Recaptcha a échoué : {error}")"""
    # TODO : test if cotisant
    # enter shotgun into db
    db_shotgun = models.ShotgunCotisantEntry(**entry.dict())
    try:
        db.add(db_shotgun)
        db.commit()
    except IntegrityError as e:
        raise HTTPException(400, detail="Tu as déjà shotgun")
    return entry.dict()

@app.get("/shotgun/{email}", response_model=schemas.ShotgunEntry)
def get_shotgun_entry(email: str, db: Session = Depends(get_db)):
    entry = db.query(models.ShotgunEntry).filter(models.ShotgunEntry.email == email).first()
    if entry == None:
        raise HTTPException(404, "Tu n'as pas shotgun")
    return {
        "first_name": entry.first_name,
        "last_name": entry.last_name,
        "email": entry.email,
        "phone_number": entry.phone_number,
        "shotgun": entry.id <= MAX_EXTE
    }

@app.get("/shotgun-cotisant/{vr_username}", response_model=schemas.ShotgunCotisantEntry)
def get_shotgun_cotisant_entry(vr_username: str, db: Session = Depends(get_db)):
    entry = db.query(models.ShotgunCotisantEntry).filter(models.ShotgunCotisantEntry.vr_username == vr_username).first()
    if entry == None:
        raise HTTPException(404, "Tu n'as pas shotgun")
    return {
        "vr_username": entry.vr_username,
        "first_name": entry.first_name,
        "last_name": entry.last_name,
        "email": entry.email,
        "phone_number": entry.phone_number,
        "shotgun": entry.id <= MAX_COTISANTS
    }
