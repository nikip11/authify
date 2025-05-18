from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

# Corrige el formato de la URL si es necesario (postgres:// -> postgresql://)
DATABASE_URL = os.getenv("DATABASE_URL", "").replace("postgres://", "postgresql://")

# Intenta conectar a la base de datos con reintentos
max_retries = 5
retry_count = 0
retry_delay = 5  # segundos

while retry_count < max_retries:
    try:
        engine = create_engine(DATABASE_URL)
        # Prueba la conexión
        with engine.connect() as connection:
            pass
        break
    except Exception as e:
        retry_count += 1
        if retry_count < max_retries:
            print(f"Error connecting to database: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed to connect to database after {max_retries} attempts: {e}")
            raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()