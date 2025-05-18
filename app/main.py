from fastapi import FastAPI
from app.database import engine
from app.auth.routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
import os

from app.auth import models
from app.database import engine

# Obtener las URLs de frontend desde la variable de entorno
# Si no está definida, se usa localhost:3000 como valor por defecto
# La variable puede contener múltiples URLs separadas por comas
frontend_urls_str = os.getenv("FRONTEND_URLS", "http://localhost:3000")
FRONTEND_URLS = [url.strip() for url in frontend_urls_str.split(",")]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
