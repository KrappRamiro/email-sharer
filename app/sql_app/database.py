from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# * Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
# But once we create an instance of the SessionLocal class, this instance will be the actual database session.
# We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Now we will use the function declarative_base() that returns a class.
# Later we will inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base()
