from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from urllib.parse import quote_plus

# Database configuration
server = 'DESKTOP-8HO87CF\\MAHESH'
database = 'LOGIN'
id = 'sa'
password = 'Mahesh@divya'
drivers = 'SQL Server'

# URL encode the password
encoded_password = quote_plus(password)

# Create the database URL
database_url = f'mssql+pyodbc://{id}:{encoded_password}@{server}/{database}?driver={drivers}'

# Create the SQLAlchemy engine
engine = create_engine(database_url)

# Initialize the base class for declarative models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    phone_number = Column(String)
    email = Column(String, unique=True)


# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(database_url):
    engine = create_engine(database_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone_number: str
    email: str


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
