from fastapi import FastAPI, Depends, HTTPException
import profiling_module as profile

from db import SessionLocal, engine
import schemas, models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone, timedelta
import requests
import random
import os

models.Base.metadata.create_all(bind=engine)


SHOTGUN_COTISANT_TIME = datetime.fromtimestamp(os.environ.get("SHOTGUN_TIME", 0))
RECAPTCHA_SECRET = os.environ.get("RECAPTCHA_SECRET", None)
MAX_COTISANTS = os.environ.get("MAX_COTISANTS", 0)
MAX_EXTE = os.environ.get("MAX_EXTES", 0)
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", None)

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
    if datetime.now() < SHOTGUN_COTISANT_TIME:
        raise HTTPException(400, "Le shotgun n'est pas encore ouvert")
    # TODO : test recaptcha
    # TODO : enter shotgun into db
    db_shotgun = models.ShotgunEntry(**entry.dict())
    try:
        db.add(db_shotgun)
        db.commit()
    except IntegrityError as e:
        raise HTTPException(400, detail="Tu as déjà shotgun")
    return entry.dict()

@app.post("/shotgun-cotisant/", response_model=schemas.ShotgunCotisant)
def shotgun_cotisant(entry: schemas.ShotgunCotisant, db: Session = Depends(get_db), recaptcha_response_token: str = ""):
    # check time
    if datetime.now() < SHOTGUN_COTISANT_TIME:
        raise HTTPException(400, "Le shotgun n'est pas encore ouvert")
    # TODO : test recaptcha
    
    # Bypassing recaptcha for tests
    """if not res["success"] or res["action"] != "shotgun" or res["score"] < 0.5:
        error = res["error-codes"][0]
        raise HTTPException(403, f"La validation Recaptcha a échoué : {error}")"""
    # enter shotgun into db
    db_shotgun = models.ShotgunCotisantEntry(**entry.dict())
    try:
        db.add(db_shotgun)
        # TODO : test if cotisant (ici parce qu'on minimise les appels API)
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
