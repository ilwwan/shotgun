from sqlalchemy.orm import Session
from . import models, schemas

def get_shotgun_entry(db: Session, email: str):
    entry = db.query(models.ShotgunEntry).filter(models.ShotgunEntry.email == email).first()
    return {
        "first_name": entry.first_name,
        "last_name": entry.last_name,
        "email": entry.email,
        "phone_number": entry.phone_number,
        "shotgun": False # TODO: this
    }

def get_shotgun_entry(db: Session, vr_username: str):
    entry = db.query(models.ShotgunCotisantEntry).filter(models.ShotgunCotisantEntry.vr_username == vr_username).first()
    return {
        "vr_username": entry.vr_username,
        "first_name": entry.first_name,
        "last_name": entry.last_name,
        "email": entry.email,
        "phone_number": entry.phone_number,
        "shotgun": False # TODO: this
    }
