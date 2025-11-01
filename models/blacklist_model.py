import sqlite3
import os
from datetime import datetime

# Chemin vers la base de données
# Nous la plaçons à la racine du projet, elle sera créée si elle n'existe pas.
DATABASE_PATH = 'blacklist.db'

class BlacklistModel:
    """
    MODÈLE - Gestion de la liste noire d'utilisateurs.
    Utilise SQLite pour stocker les informations de manière persistante.
    """
    
    def __init__(self):
        # Initialise la connexion et s'assure que la table existe
        self._initialize_db()
        print(f"✅ Modèle Blacklist initialisé. Base de données: {DATABASE_PATH}")

    def _get_connection(self):
        """Ouvre une connexion à la base de données."""
        return sqlite3.connect(DATABASE_PATH)

    def _initialize_db(self):
        """Crée la table 'blacklisted_users' si elle n'existe pas."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blacklisted_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_identifier TEXT NOT NULL UNIQUE,
                    max_similarity REAL NOT NULL,
                    ban_date TEXT NOT NULL,
                    reason TEXT
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")
        finally:
            conn.close()

    def add_to_blacklist(self, user_identifier, similarity_score, reason="Seuil de similarité dépassé ( > 80%)"):
        """
        Ajoute ou met à jour un utilisateur dans la liste noire.
        Note: user_identifier devrait idéalement être un ID utilisateur, sinon une adresse IP.
        """
        conn = self._get_connection()
        now = datetime.now().isoformat()
        try:
            # Tente d'insérer le nouvel enregistrement
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO blacklisted_users (user_identifier, max_similarity, ban_date, reason)
                VALUES (?, ?, ?, ?)
                ''',
                (user_identifier, similarity_score, now, reason)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # L'utilisateur existe déjà, on met juste à jour le score et la date
            cursor.execute(
                '''
                UPDATE blacklisted_users
                SET max_similarity = ?, ban_date = ?
                WHERE user_identifier = ?
                ''',
                (similarity_score, now, user_identifier)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout/mise à jour de l'utilisateur {user_identifier}: {e}")
            return False
        finally:
            conn.close()

    def is_blacklisted(self, user_identifier):
        """Vérifie si un utilisateur est dans la liste noire."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT user_identifier FROM blacklisted_users WHERE user_identifier = ?',
                (user_identifier,)
            )
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Erreur lors de la vérification de la liste noire pour {user_identifier}: {e}")
            return False
        finally:
            conn.close()

    def get_blacklist(self):
        """Retourne toute la liste noire (utile pour une interface d'admin)."""
        conn = self._get_connection()
        try:
            conn.row_factory = sqlite3.Row # Permet d'obtenir des dictionnaires (rows)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM blacklisted_users ORDER BY ban_date DESC')
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Erreur lors de la récupération de la liste noire: {e}")
            return []
        finally:
            conn.close()

    def remove_from_blacklist(self, user_identifier):
        """Retire un utilisateur de la liste noire."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM blacklisted_users WHERE user_identifier = ?',
                (user_identifier,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur {user_identifier}: {e}")
            return False
        finally:
            conn.close()
