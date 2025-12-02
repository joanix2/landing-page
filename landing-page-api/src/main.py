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

# Inclusion des routes avec préfixe /api
app.include_router(clients_router, prefix="/api")
app.include_router(estimations_router, prefix="/api")
app.include_router(ai_router, prefix="/api")


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


@app.get("/api")
async def root():
    """Route racine."""
    return {
        "message": "Bienvenue sur l'API Studio Web",
    }


@app.get("/health")
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint - Vérifie l'état de l'API et de la base de données.
    
    Returns:
        dict: Status de l'API et de la base de données
    """
    from datetime import datetime
    from sqlalchemy import text
    from src.database import async_session
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "api": {
            "status": "ok",
            "version": "1.0.0"
        },
        "database": {
            "status": "unknown",
            "connected": False,
            "details": None
        }
    }
    
    # Test de connexion à la base de données
    try:
        async with async_session() as session:
            # Exécuter une requête simple pour vérifier la connexion
            result = await session.execute(text("SELECT 1"))
            result.scalar()
            
            # Vérifier la version de PostgreSQL
            version_result = await session.execute(text("SELECT version()"))
            db_version = version_result.scalar()
            
            health_status["database"]["status"] = "ok"
            health_status["database"]["connected"] = True
            health_status["database"]["details"] = {
                "type": "PostgreSQL",
                "version": db_version.split(",")[0] if db_version else "unknown"
            }
            
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"]["status"] = "error"
        health_status["database"]["connected"] = False
        health_status["database"]["details"] = {
            "error": str(e),
            "type": type(e).__name__
        }
    
    return health_status
