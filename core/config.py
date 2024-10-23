from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    DB_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', '123')
    DB_NAME: str = os.getenv('POSTGRES_DB', 'users')
    DB_HOST: str = os.getenv('POSTGRES_SERVER', 'localhost')
    DB_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    
    DATABASE_URL: str = f"postgresql+psycopg2://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    JWT_SECRET: str = os.getenv('JWT_SECRET', '709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60))

def get_settings() -> Settings:
    return Settings()

# Get settings instance
settings = get_settings()

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, pool_recycle=3600)

# Example: Test the connection
try:
    with engine.connect() as connection:
        # Use text() for raw SQL
        result = connection.execute(text("SELECT 1"))
        print("Connection successful:", result.fetchone())
except SQLAlchemyError as e:
    print("Error connecting to the database:", e)
