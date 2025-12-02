"""Script de gestion du cache IA."""

import asyncio
from sqlalchemy import select, func, delete
from datetime import datetime, timedelta

from src.config import AsyncSessionLocal
from src.models.ai_cache import AISuggestionCache


async def show_cache_stats():
    """Afficher les statistiques du cache."""
    async with AsyncSessionLocal() as db:
        # Nombre total d'entrées
        result = await db.execute(select(func.count(AISuggestionCache.id)))
        total = result.scalar()
        
        # Utilisation totale
        result = await db.execute(select(func.sum(AISuggestionCache.used_count)))
        total_uses = result.scalar() or 0
        
        # Économies estimées (coût par appel IA = $0.001)
        savings = (total_uses - total) * 0.001
        
        print("=" * 60)
        print("📊 STATISTIQUES DU CACHE IA")
        print("=" * 60)
        print(f"Entrées dans le cache    : {total}")
        print(f"Utilisations totales     : {total_uses}")
        print(f"Économies estimées       : ${savings:.3f}")
        print(f"Taux de réutilisation    : {((total_uses - total) / total * 100) if total > 0 else 0:.1f}%")
        print("=" * 60)


async def show_cache_entries():
    """Afficher les entrées du cache."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(AISuggestionCache).order_by(AISuggestionCache.used_count.desc()).limit(10)
        )
        entries = result.scalars().all()
        
        print("\n🔝 TOP 10 SUGGESTIONS LES PLUS UTILISÉES")
        print("=" * 80)
        
        for i, entry in enumerate(entries, 1):
            print(f"\n{i}. Utilisée {entry.used_count} fois")
            print(f"   Description : {entry.description_projet[:70]}...")
            print(f"   Suggestion  : {entry.type_projet} | {entry.nombre_pages} pages | {entry.budget}")
            print(f"   Créée       : {entry.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Dernière    : {entry.last_used_at.strftime('%Y-%m-%d %H:%M')}")
        
        print("=" * 80)


async def clear_old_cache(days: int = 30):
    """Supprimer les entrées du cache plus anciennes que X jours."""
    async with AsyncSessionLocal() as db:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = await db.execute(
            delete(AISuggestionCache).where(
                AISuggestionCache.last_used_at < cutoff_date
            )
        )
        
        deleted_count = result.rowcount
        await db.commit()
        
        print(f"🗑️  {deleted_count} entrées supprimées (non utilisées depuis {days} jours)")


async def clear_all_cache():
    """Vider complètement le cache."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(delete(AISuggestionCache))
        deleted_count = result.rowcount
        await db.commit()
        
        print(f"🗑️  Cache vidé : {deleted_count} entrées supprimées")


async def main():
    """Menu principal."""
    print("\n" + "=" * 60)
    print("🤖 GESTION DU CACHE IA")
    print("=" * 60)
    print("\nOptions :")
    print("1. Afficher les statistiques")
    print("2. Voir les entrées les plus utilisées")
    print("3. Supprimer les entrées anciennes (30 jours)")
    print("4. Vider complètement le cache")
    print("5. Quitter")
    print()
    
    choice = input("Votre choix (1-5) : ").strip()
    
    if choice == "1":
        await show_cache_stats()
    elif choice == "2":
        await show_cache_entries()
    elif choice == "3":
        days = input("Supprimer les entrées non utilisées depuis combien de jours ? (défaut: 30) : ").strip()
        days = int(days) if days.isdigit() else 30
        confirm = input(f"Confirmer la suppression des entrées de plus de {days} jours ? (o/n) : ").strip().lower()
        if confirm == "o":
            await clear_old_cache(days)
        else:
            print("❌ Opération annulée")
    elif choice == "4":
        confirm = input("⚠️  ATTENTION : Cela supprimera TOUTES les entrées. Confirmer ? (o/n) : ").strip().lower()
        if confirm == "o":
            await clear_all_cache()
        else:
            print("❌ Opération annulée")
    elif choice == "5":
        print("👋 Au revoir !")
        return
    else:
        print("❌ Choix invalide")
    
    # Redemander après chaque action
    input("\nAppuyez sur Entrée pour continuer...")
    await main()


if __name__ == "__main__":
    asyncio.run(main())
