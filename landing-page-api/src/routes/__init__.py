"""Routes de l'API."""

from .clients import router as clients_router
from .estimations import router as estimations_router
from .ai_suggestions import router as ai_router

__all__ = ["clients_router", "estimations_router", "ai_router"]
