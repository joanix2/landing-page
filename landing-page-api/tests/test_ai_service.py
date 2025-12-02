"""Script de test pour le service IA."""

import asyncio
from src.services.ai_service import AIService


async def test_ai_service():
    """Tester le service IA avec différentes descriptions."""
    
    # Créer le service
    try:
        ai_service = AIService()
    except ValueError as e:
        print(f"❌ Erreur de configuration : {e}")
        print("💡 Assurez-vous que OPENAI_API_KEY est défini dans votre fichier .env")
        return
    
    # Cas de test
    test_cases = [
        {
            "nom": "Landing Page SaaS",
            "description": "Je lance un nouveau produit SaaS et j'ai besoin d'une page pour présenter les fonctionnalités et collecter des emails pour la beta."
        },
        {
            "nom": "Site Restaurant",
            "description": "Je veux créer un site web pour mon restaurant avec un menu en ligne, une galerie de photos et un formulaire de réservation."
        },
        {
            "nom": "E-commerce Artisanal",
            "description": "Je veux vendre mes créations artisanales en ligne. J'ai environ 50 produits à présenter avec un système de paiement sécurisé."
        },
        {
            "nom": "Plateforme Complexe",
            "description": "Besoin d'une plateforme de gestion de projets pour mon équipe avec dashboard, suivi du temps, chat intégré, et API."
        }
    ]
    
    print("🤖 Test du Service IA - Suggestions d'Estimation\n")
    print("=" * 80)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i} : {test['nom']}")
        print(f"Description : {test['description'][:70]}...")
        print("-" * 80)
        
        result = await ai_service.analyze_and_suggest(test['description'])
        
        if result['success']:
            suggestions = result['suggestions']
            print(f"✅ Suggestions générées :")
            print(f"   • Type de projet    : {suggestions['type_projet']}")
            print(f"   • Nombre de pages   : {suggestions['nombre_pages']}")
            print(f"   • Délai souhaité    : {suggestions['delai_souhaite']}")
            print(f"   • Budget estimé     : {suggestions['budget']}")
            print(f"\n   📋 Explication :")
            print(f"   {result['explication']}")
        else:
            print(f"❌ Erreur : {result['message']}")
        
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_ai_service())
