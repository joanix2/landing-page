"""Application FastAPI principale."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import engine
from src.database import Base
from src.routes import clients_router, estimations_router, ai_router

# Création de l'application FastAPI
app = FastAPI(title="Studio Web API (Postgres)")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(clients_router)
app.include_router(estimations_router)
app.include_router(ai_router)


@app.on_event("startup")
async def on_startup():
    """Créer les tables au démarrage (pour dev ; en prod -> Alembic)."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Base de données connectée et tables créées")
    except Exception as e:
        print(f"⚠️  Avertissement : Impossible de se connecter à la base de données")
        print(f"   Erreur : {e}")
        print(f"   L'API démarre quand même, mais les routes nécessitant la DB échoueront.")


@app.get("/")
async def root():
    """Route racine."""
    return {
        "message": "Bienvenue sur l'API Studio Web",
        "docs": "/docs",
        "redoc": "/redoc"
    }
