from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.backend.core.settings import settings

DATABASE_URL = settings.DATABASE_URL

# 2. Create the Engine
engine = create_engine(DATABASE_URL)

# 3. Create the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class
Base = declarative_base()

# 5. Dependency for API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()