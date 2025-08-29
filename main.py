from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware # Pour l'avenir, si nécessaire
import api.users, api.profiles, api.games, api.matchmaking
from database import engine, Base

# Création des tables (si elles n'existent pas encore dans la base de données)
# Base.metadata.create_all(bind=engine) # !!! Uniquement pour les tests ! En production, utilise les migrations (Alembic)

app = FastAPI(title="Esport Platform API", version="0.1.0")

# Configuration de CORS (si le frontend est sur un autre port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, spécifie les origins exacts
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(api.users.router)
app.include_router(api.profiles.router)
app.include_router(api.games.router)
app.include_router(api.matchmaking.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Esport Platform API"}

# Lancement : uvicorn main:app --reload