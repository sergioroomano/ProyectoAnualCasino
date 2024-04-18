from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'mysql+mysqldb://mascaro101:laquegana123@mascaro101.mysql.pythonanywhere-services.com/CasinoDB'

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Use this function to get a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()