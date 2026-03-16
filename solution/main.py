"""
CORRECTION : main.py - Script principal
=========================================
Cree les tables, insere des articles, et les affiche.
Lancez : python main.py
"""

from sqlalchemy import select

from app.database import engine, SessionLocal, Base
from app.models import Article


# ============================================================================
# ETAPE 1 : Creer les tables
# ============================================================================

def creer_tables():
    """Cree toutes les tables definies dans nos modeles."""
    Base.metadata.create_all(bind=engine)
    print("Tables creees avec succes !")


# ============================================================================
# ETAPE 2 : Inserer des articles
# ============================================================================

def inserer_articles():
    """Insere plusieurs articles de test."""
    with SessionLocal() as session:
        articles = [
            Article(
                title="Introduction a SQLAlchemy",
                slug="introduction-sqlalchemy",
                content="SQLAlchemy est un ORM pour Python. "
                        "Il permet de manipuler des bases de donnees "
                        "en utilisant des objets Python au lieu de SQL brut. "
                        "C'est l'ORM le plus populaire en Python.",
                is_published=True,
            ),
            Article(
                title="Les modeles en pratique",
                slug="modeles-en-pratique",
                content="Un modele SQLAlchemy est une classe Python "
                        "qui represente une table dans la base de donnees. "
                        "Chaque attribut de la classe correspond a une colonne.",
                is_published=True,
            ),
            Article(
                title="Les requetes SELECT",
                slug="requetes-select",
                content="Pour lire des donnees, on utilise select(). "
                        "C'est l'API moderne de SQLAlchemy 2.0 "
                        "qui remplace l'ancien session.query().",
                is_published=True,
            ),
            Article(
                title="Article en brouillon",
                slug="article-brouillon",
                content="Cet article n'est pas encore pret. "
                        "Il restera en brouillon jusqu'a publication.",
                # is_published reste False par defaut
            ),
            Article(
                title="Les bonnes pratiques",
                slug="bonnes-pratiques",
                content="Utilisez le Repository Pattern pour organiser "
                        "votre code d'acces aux donnees.",
                # Aussi en brouillon
            ),
        ]

        session.add_all(articles)
        session.commit()

        print(f"{len(articles)} articles inseres !")
        for a in articles:
            session.refresh(a)
            print(f"  {a}")


# ============================================================================
# ETAPE 3 : Lire et afficher
# ============================================================================

def afficher_articles():
    """Lit tous les articles et affiche leurs details."""
    with SessionLocal() as session:
        requete = select(Article).order_by(Article.id)
        articles = session.execute(requete).scalars().all()

        print(f"\n{'='*60}")
        print(f" {len(articles)} articles en base de donnees")
        print(f"{'='*60}")

        for article in articles:
            status = "PUBLIE" if article.is_published else "BROUILLON"
            print(f"\n  [{status}] {article.title}")
            print(f"    ID         : {article.id}")
            print(f"    Slug       : {article.slug}")
            print(f"    Contenu    : {article.content[:60]}...")
            print(f"    Vues       : {article.view_count}")
            print(f"    Cree le    : {article.created_at}")
            print(f"    Modifie le : {article.updated_at}")

        # Stats
        publies = sum(1 for a in articles if a.is_published)
        brouillons = sum(1 for a in articles if not a.is_published)
        print(f"\n  --- Statistiques ---")
        print(f"  Publies    : {publies}")
        print(f"  Brouillons : {brouillons}")


# ============================================================================
# ETAPE 4 : Tester la modification (pour voir updated_at)
# ============================================================================

def tester_modification():
    """Modifie un article pour montrer que updated_at se met a jour."""
    with SessionLocal() as session:
        article = session.execute(
            select(Article).where(Article.slug == "introduction-sqlalchemy")
        ).scalar_one_or_none()

        if article:
            print(f"\n--- Test de modification ---")
            print(f"  AVANT : title='{article.title}', updated_at={article.updated_at}")

            article.title = "Introduction a SQLAlchemy 2.0"
            article.view_count = 42
            session.commit()
            session.refresh(article)

            print(f"  APRES : title='{article.title}', updated_at={article.updated_at}")
            print(f"  Vues  : {article.view_count}")


# ============================================================================
# LANCEMENT
# ============================================================================

if __name__ == "__main__":
    print()
    print("=" * 60)
    print(" TP 1 - SOLUTION : Configuration et Premiers Modeles")
    print("=" * 60)
    print()

    print("--- Etape 1 : Creation des tables ---")
    creer_tables()
    print()

    print("--- Etape 2 : Insertion des articles ---")
    inserer_articles()
    print()

    print("--- Etape 3 : Lecture des articles ---")
    afficher_articles()

    print()
    print("--- Etape 4 : Test de modification ---")
    tester_modification()

    print()
    print("=" * 60)
    print(" TP 1 TERMINE avec succes !")
    print(" Lancez 'python visualiser_db.py' pour voir la base")
    print("=" * 60)
