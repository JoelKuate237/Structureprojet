"""
=============================================================================
 VISUALISER LA BASE DE DONNEES
=============================================================================
 Ce script lit le fichier tp1_articles.db et affiche son contenu
 de facon claire et lisible.

 Lancez : python visualiser_db.py
=============================================================================
"""

import os
import sqlite3
from pathlib import Path


def visualiser():
    """Lit et affiche le contenu de la base de donnees SQLite."""

    # Chercher le fichier .db
    db_path = Path("tp1_articles.db")

    if not db_path.exists():
        print("ERREUR : Le fichier 'tp1_articles.db' n'existe pas.")
        print("Avez-vous lance 'python main.py' d'abord ?")
        return

    # Taille du fichier
    taille = db_path.stat().st_size
    print()
    print("=" * 70)
    print(f" BASE DE DONNEES : {db_path}")
    print(f" Taille : {taille:,} octets ({taille / 1024:.1f} Ko)")
    print("=" * 70)

    # Connexion directe avec sqlite3 (sans SQLAlchemy)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row  # Pour acceder aux colonnes par nom
    cursor = conn.cursor()

    # Lister toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        print("\n  La base est vide (aucune table).")
        conn.close()
        return

    print(f"\n  Tables trouvees : {len(tables)}")
    for table in tables:
        print(f"    - {table}")

    # Pour chaque table, afficher la structure et les donnees
    for table in tables:
        print()
        print("-" * 70)
        print(f"  TABLE : {table}")
        print("-" * 70)

        # Structure de la table (colonnes)
        cursor.execute(f"PRAGMA table_info({table})")
        colonnes = cursor.fetchall()

        print(f"\n  Structure ({len(colonnes)} colonnes) :")
        print(f"  {'Colonne':<20s} {'Type':<15s} {'Nullable':<10s} {'Defaut':<15s} {'Cle':<5s}")
        print(f"  {'-'*20} {'-'*15} {'-'*10} {'-'*15} {'-'*5}")

        noms_colonnes = []
        for col in colonnes:
            nom = col[1]
            type_col = col[2]
            nullable = "oui" if not col[3] else "NON"
            defaut = str(col[4]) if col[4] is not None else ""
            cle = "PK" if col[5] else ""
            noms_colonnes.append(nom)
            print(f"  {nom:<20s} {type_col:<15s} {nullable:<10s} {defaut:<15s} {cle:<5s}")

        # Donnees de la table
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        nb_lignes = cursor.fetchone()[0]

        print(f"\n  Donnees ({nb_lignes} ligne(s)) :")

        if nb_lignes == 0:
            print("  (aucune donnee)")
        else:
            cursor.execute(f"SELECT * FROM {table}")
            lignes = cursor.fetchall()

            # Afficher les en-tetes
            largeurs = []
            for nom in noms_colonnes:
                largeur = max(len(nom), 12)
                largeurs.append(largeur)

            en_tete = "  "
            separateur = "  "
            for i, nom in enumerate(noms_colonnes):
                en_tete += f"{nom:<{largeurs[i]}s} | "
                separateur += f"{'-'*largeurs[i]}-+-"

            print(en_tete)
            print(separateur)

            # Afficher chaque ligne
            for ligne in lignes:
                texte = "  "
                for i, valeur in enumerate(ligne):
                    val_str = str(valeur) if valeur is not None else "NULL"
                    # Tronquer les textes longs
                    if len(val_str) > largeurs[i]:
                        val_str = val_str[:largeurs[i] - 3] + "..."
                    texte += f"{val_str:<{largeurs[i]}s} | "
                print(texte)

    # Index
    print()
    print("-" * 70)
    print("  INDEX")
    print("-" * 70)
    cursor.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")
    index_list = cursor.fetchall()
    if index_list:
        for idx in index_list:
            print(f"  {idx[0]} sur table '{idx[1]}'")
    else:
        print("  Aucun index trouve.")

    conn.close()

    print()
    print("=" * 70)
    print(" Fin de la visualisation")
    print("=" * 70)
    print()


if __name__ == "__main__":
    visualiser()
