#!/usr/bin/env python3
"""Script de validation de la configuration des services."""

import sys
from pathlib import Path

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Tester les imports des services."""
    print("🔍 Test des imports...")
    
    try:
        from src.services import AIService, EmailService, get_ai_service
        print("  ✅ Import centralisé OK")
        print(f"     - AIService: {AIService}")
        print(f"     - EmailService: {EmailService}")
        print(f"     - get_ai_service: {get_ai_service}")
    except ImportError as e:
        print(f"  ❌ Erreur d'import centralisé: {e}")
        return False
    
    try:
        from src.services.ai_service import AIService
        from src.services.email_service import EmailService
        print("  ✅ Imports spécifiques OK")
    except ImportError as e:
        print(f"  ❌ Erreur d'import spécifique: {e}")
        return False
    
    return True


def test_ai_service_structure():
    """Vérifier la structure du service IA."""
    print("\n🤖 Test structure AI Service...")
    
    service_dir = Path("src/services/ai_service")
    templates_dir = service_dir / "templates"
    
    required_files = [
        service_dir / "__init__.py",
        service_dir / "ai_service.py",
        service_dir / "README.md",
        templates_dir / "system_prompt.txt.j2",
        templates_dir / "user_prompt.txt.j2",
    ]
    
    all_ok = True
    for file_path in required_files:
        if file_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ Manquant: {file_path}")
            all_ok = False
    
    return all_ok


def test_email_service_structure():
    """Vérifier la structure du service email."""
    print("\n📧 Test structure Email Service...")
    
    service_dir = Path("src/services/email_service")
    templates_dir = service_dir / "templates"
    
    required_files = [
        service_dir / "__init__.py",
        service_dir / "email_service.py",
        service_dir / "README.md",
        templates_dir / "newsletter_confirmation.html.j2",
        templates_dir / "newsletter_confirmation.txt.j2",
        templates_dir / "estimation_confirmation.html.j2",
        templates_dir / "estimation_confirmation.txt.j2",
        templates_dir / "admin_notification.html.j2",
        templates_dir / "admin_notification.txt.j2",
    ]
    
    all_ok = True
    for file_path in required_files:
        if file_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ Manquant: {file_path}")
            all_ok = False
    
    return all_ok


def test_dependencies():
    """Vérifier les dépendances requises."""
    print("\n📦 Test des dépendances...")
    
    dependencies = {
        "jinja2": "Jinja2 (templates)",
        "langchain": "LangChain (AI)",
        "langchain_openai": "LangChain OpenAI (AI)",
        "pydantic": "Pydantic (validation)",
    }
    
    all_ok = True
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {description}")
        except ImportError:
            print(f"  ❌ Manquant: {description} (module: {module})")
            all_ok = False
    
    return all_ok


def test_template_loading():
    """Tester le chargement des templates."""
    print("\n🎨 Test du chargement des templates...")
    
    import os
    
    # Tester AIService (peut nécessiter OPENAI_API_KEY)
    try:
        # Temporairement définir une clé factice si elle n'existe pas
        original_key = os.getenv("OPENAI_API_KEY")
        if not original_key:
            os.environ["OPENAI_API_KEY"] = "sk-fake-key-for-testing"
            print("  ⚠️  OPENAI_API_KEY non définie, utilisation d'une clé factice pour les tests")
        
        from src.services.ai_service import get_ai_service
        ai_service = get_ai_service()
        print("  ✅ AIService initialisé")
        print(f"     - Templates Jinja2: {ai_service.jinja_env}")
        print(f"     - System prompt: {ai_service.system_prompt_template}")
        print(f"     - User prompt: {ai_service.user_prompt_template}")
        
        # Restaurer l'état original
        if not original_key:
            del os.environ["OPENAI_API_KEY"]
    except Exception as e:
        print(f"  ❌ Erreur AIService: {e}")
        return False
    
    try:
        from src.services import EmailService
        email_service = EmailService()
        print("  ✅ EmailService initialisé")
        print(f"     - Templates Jinja2: {email_service.jinja_env}")
    except Exception as e:
        print(f"  ❌ Erreur EmailService: {e}")
        return False
    
    return True


def main():
    """Exécuter tous les tests."""
    print("=" * 60)
    print("🧪 VALIDATION DE LA CONFIGURATION DES SERVICES")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Structure AI Service": test_ai_service_structure(),
        "Structure Email Service": test_email_service_structure(),
        "Dépendances": test_dependencies(),
        "Chargement Templates": test_template_loading(),
    }
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 Tous les tests sont passés !")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
