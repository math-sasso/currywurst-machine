import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Path.mkdir(Path.cwd() / "app/data", exist_ok=True, parents=True)

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///"
    + "/code/app/data/"
    + os.getenv("DATABASE_NAME", "currywurst_machine.db")
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()
