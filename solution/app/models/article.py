"""
CORRECTION : models/article.py - Le modele Article
====================================================
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Article(Base):
    """
    Modele Article pour un blog.
    Chaque instance de cette classe = une ligne dans la table 'articles'.
    """

    # Nom de la table dans la base de donnees
    __tablename__ = "articles"

    # Cle primaire : identifiant unique, auto-incremente
    id: Mapped[int] = mapped_column(primary_key=True)

    # Titre : texte de 200 caracteres max, obligatoire
    # index=True cree un index pour accelerer les recherches par titre
    title: Mapped[str] = mapped_column(String(200), index=True)

    # Slug : identifiant pour les URLs, unique (pas de doublons)
    # Exemple : "mon-premier-article" au lieu de id=1
    slug: Mapped[str] = mapped_column(String(250), unique=True)

    # Contenu : texte long sans limite de taille
    content: Mapped[str] = mapped_column(Text)

    # Publie ou brouillon : False par defaut
    # Un article commence en brouillon
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    # Compteur de vues : 0 par defaut
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    # Date de creation : remplie automatiquement par la base de donnees
    # server_default = c'est le SERVEUR SQL qui met la date (pas Python)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # Date de derniere modification : None au debut
    # onupdate = mis a jour automatiquement a chaque modification
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=func.now()
    )

    def __repr__(self) -> str:
        """Affichage lisible quand on fait print(article)."""
        status = "publie" if self.is_published else "brouillon"
        return f"Article(id={self.id}, title='{self.title}', {status})"
