from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# SQLite needs check_same_thread=False for multithreaded dev server
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

# PostgreSQL note:
# - For PostgreSQL, set DATABASE_URL like:
#   postgresql+psycopg2://user:password@host:5432/dbname
# - No special connect_args needed for PostgreSQL.
engine = create_engine(settings.database_url, echo=False, future=True, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
