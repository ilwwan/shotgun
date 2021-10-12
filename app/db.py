from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = "{protocol}://{user}:{password}@{host}:{port}/{db}".format(
    protocol=os.environ.get("DB_PROTOCOL", "protocol"),
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD", ""),
    port=os.environ.get("DB_PORT", "5432"),
    db=os.environ.get("DB_DATABASE", "postgres")
)

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=100, connect_args={'connect_timeout': 10})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()