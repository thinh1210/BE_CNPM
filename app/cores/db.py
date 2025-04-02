from sqlmodel import create_engine, SQLModel
from .config import DATABASE_URL

engine= create_engine(DATABASE_URL, echo=True, future=True)

SQLModel.metadata.create_all(engine)