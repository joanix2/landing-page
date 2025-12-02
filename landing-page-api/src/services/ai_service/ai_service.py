"""Service IA pour la pré-complétion du formulaire d'estimation."""

import os
import hashlib
from typing import Optional
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from jinja2 import Environment, FileSystemLoader


class EstimationSuggestion(BaseModel):
    """Modèle pour les suggestions d'estimation (sortie IA)."""
    
    type_projet: str = Field(
        description="Type de projet suggéré parmi: Landing Page, Site Vitrine, E-commerce, Projet Sur Mesure"
    )
    liste_pages: list[str] = Field(
        description="Liste complète des pages nécessaires pour le projet (ex: ['Accueil', 'À propos', 'Contact'])"
    )
    explication: str = Field(
        description="Brève explication du projet et des pages suggérées (2-3 phrases)"
    )


class AIService:
    """Service pour l'assistance IA lors du remplissage du formulaire."""
    
    def __init__(self):
        """Initialiser le service IA avec OpenAI."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY n'est pas définie dans les variables d'environnement")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=api_key
        )
        
        # Parser pour structurer la sortie
        self.parser = PydanticOutputParser(pydantic_object=EstimationSuggestion)
        
        # Configuration de Jinja2 pour les templates de prompts
        template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Charger les templates de prompts
        self.system_prompt_template = self.jinja_env.get_template("system_prompt.txt.j2")
        self.user_prompt_template = self.jinja_env.get_template("user_prompt.txt.j2")
    
    def _render_prompts(self, description: str, format_instructions: str) -> tuple[str, str]:
        """
        Rendre les templates de prompts avec Jinja2.
        
        Args:
            description: Description du projet
            format_instructions: Instructions de formatage
            
        Returns:
            Tuple (system_prompt, user_prompt)
        """
        system_prompt = self.system_prompt_template.render(
            format_instructions=format_instructions
        )
        user_prompt = self.user_prompt_template.render(
            description=description
        )
        return system_prompt, user_prompt
    
    def _calculate_budget(self, nombre_pages: int) -> str:
        """
        Calculer le budget en fonction du nombre de pages.
        Formule : nombre_pages × 3 × 500€
        """
        montant = nombre_pages * 3 * 500
        
        if montant < 5000:
            return "Moins de 5 000€"
        elif montant <= 10000:
            return "5 000€ - 10 000€"
        elif montant <= 20000:
            return "10 000€ - 20 000€"
        else:
            return "Plus de 20 000€"
    
    def _calculate_delai(self, nombre_pages: int) -> str:
        """
        Calculer le délai en fonction du nombre de pages.
        Formule : nombre_pages × 3 jours
        """
        jours = nombre_pages * 3
        
        if jours <= 15: # Moins de deux semaines
            return "Rapide"
        elif jours <= 60:  # 1-2 mois
            return "Normal"
        else:  # Plus de 2 mois
            return "Flexible"
    
    @staticmethod
    def _hash_description(description: str) -> str:
        """Générer un hash SHA256 de la description pour le cache."""
        normalized = description.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    async def _get_from_cache(
        self, 
        description: str, 
        db: AsyncSession
    ) -> Optional[EstimationSuggestion]:
        """Récupérer une suggestion depuis le cache."""
        from src.models.ai_cache import AISuggestionCache
        
        description_hash = self._hash_description(description)
        
        result = await db.execute(
            select(AISuggestionCache).where(
                AISuggestionCache.description_hash == description_hash
            )
        )
        cached = result.scalar_one_or_none()
        
        if cached:
            # Mettre à jour les statistiques d'utilisation
            cached.used_count += 1
            cached.last_used_at = datetime.utcnow()
            await db.commit()
            
            print(f"✅ Suggestion trouvée dans le cache (utilisée {cached.used_count} fois)")
            
            return EstimationSuggestion(
                type_projet=cached.type_projet,
                liste_pages=cached.liste_pages,
                explication=cached.explication
            )
        
        return None
    
    async def _save_to_cache(
        self,
        description: str,
        suggestion: EstimationSuggestion,
        db: AsyncSession
    ) -> None:
        """Sauvegarder une suggestion dans le cache."""
        from src.models.ai_cache import AISuggestionCache
        
        description_hash = self._hash_description(description)
        
        # Vérifier si existe déjà (race condition)
        result = await db.execute(
            select(AISuggestionCache).where(
                AISuggestionCache.description_hash == description_hash
            )
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            cached = AISuggestionCache(
                description_hash=description_hash,
                description_projet=description,
                type_projet=suggestion.type_projet,
                liste_pages=suggestion.liste_pages,
                explication=suggestion.explication
            )
            db.add(cached)
            await db.commit()
            print("💾 Suggestion sauvegardée dans le cache")
    
    async def suggest_estimation_params(
        self, 
        description_projet: str,
        db: Optional[AsyncSession] = None
    ) -> Optional[EstimationSuggestion]:
        """
        Analyser la description du projet et suggérer des paramètres.
        Utilise le cache PostgreSQL si disponible.
        
        Args:
            description_projet: Description textuelle du projet client
            db: Session de base de données (optionnelle, pour le cache)
            
        Returns:
            EstimationSuggestion avec les paramètres suggérés ou None en cas d'erreur
        """
        try:
            # Vérifier le cache si DB disponible
            if db:
                cached_suggestion = await self._get_from_cache(description_projet, db)
                if cached_suggestion:
                    return cached_suggestion
            
            # Pas de cache, appeler l'IA
            print("🤖 Génération de nouvelles suggestions via IA...")
            
            # Rendre les prompts avec Jinja2
            system_prompt, user_prompt = self._render_prompts(
                description_projet,
                self.parser.get_format_instructions()
            )
            
            # Créer le prompt LangChain
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", user_prompt)
            ])
            
            # Exécuter la chaîne
            chain = prompt | self.llm | self.parser
            result = await chain.ainvoke({})
            
            # Sauvegarder dans le cache si DB disponible
            if db and result:
                await self._save_to_cache(description_projet, result, db)
            
            return result
            
        except Exception as e:
            print(f"Erreur lors de la suggestion IA : {e}")
            return None
    
    async def analyze_and_suggest(
        self, 
        description_projet: str,
        db: Optional[AsyncSession] = None
    ) -> dict:
        """
        Analyser le projet et retourner des suggestions formatées.
        Utilise le cache PostgreSQL si disponible.
        
        Args:
            description_projet: Description du projet
            db: Session de base de données (optionnelle, pour le cache)
            
        Returns:
            Dictionnaire avec les suggestions ou un message d'erreur
        """
        if not description_projet or len(description_projet.strip()) < 20:
            return {
                "success": False,
                "message": "La description du projet doit contenir au moins 20 caractères pour obtenir des suggestions pertinentes."
            }
        
        suggestion = await self.suggest_estimation_params(description_projet, db)
        
        if not suggestion:
            return {
                "success": False,
                "message": "Impossible de générer des suggestions pour le moment. Veuillez réessayer."
            }
        
        # Calculer les valeurs dérivées à partir de liste_pages
        nombre_pages = len(suggestion.liste_pages)
        budget = self._calculate_budget(nombre_pages)
        delai_souhaite = self._calculate_delai(nombre_pages)
        
        return {
            "success": True,
            "suggestions": {
                "type_projet": suggestion.type_projet,
                "liste_pages": suggestion.liste_pages,
                "nombre_pages": nombre_pages,
                "delai_souhaite": delai_souhaite,
                "budget": budget
            },
            "explication": suggestion.explication,
            "from_cache": db is not None  # Indiquer si provient du cache
        }


# Instance singleton du service
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """Obtenir l'instance du service IA (singleton)."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
