"""
CORRECTION : database.py - Engine, Session, Base
=================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


# 1. ENGINE : la connexion a la base de donnees
# On utilise les valeurs de settings (lues depuis .env)
engine = create_engine(
    settings.database_url,      # "sqlite:///tp1_articles.db"
    echo=settings.database_echo  # True = affiche le SQL genere
)

# 2. BASE : classe parent de tous les modeles
class Base(DeclarativeBase):
    pass

# 3. SESSION FACTORY : usine a sessions
SessionLocal = sessionmaker(
    bind=engine,       # Connectee a notre engine
    autocommit=False,  # On fait commit() manuellement
    autoflush=False    # On flush() manuellement
)

# 4. FONCTION get_db : ouvre et ferme une session proprement
def get_db():
    """Generateur de sessions. Utile pour FastAPI (Jour 2)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
