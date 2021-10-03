from pydantic import BaseModel

class Shotgun(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str

class ShotgunCotisant(Shotgun):
    vr_username: str

class ShotgunEntry(Shotgun):
    shotgun: bool

class ShotgunCotisantEntry(ShotgunCotisant):
    shotgun: bool
