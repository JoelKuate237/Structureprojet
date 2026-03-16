"""
CORRECTION : config.py - Configuration avec Pydantic Settings
==============================================================
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration de l'application.
    Les valeurs sont lues automatiquement depuis le fichier .env

    Pydantic fait la correspondance par nom :
      - database_url  dans Python  <-->  DATABASE_URL  dans .env
      - database_echo dans Python  <-->  DATABASE_ECHO dans .env
    """

    # URL de la base de donnees
    # Valeur par defaut si .env n'existe pas
    database_url: str = "sqlite:///tp1_articles.db"

    # Afficher les requetes SQL dans la console (utile pour debugger)
    database_echo: bool = False

    # Configuration pour lire le fichier .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Instance unique utilisee dans toute l'application
settings = Settings()
