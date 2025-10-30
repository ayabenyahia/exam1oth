# exam1oth (corrigé)

Ce dépôt contient le back-end Flask (Python) pour la détection de plagiat / triche.

## Exécution locale (Linux/Windows/macOS)

1. Crée un environnement virtuel (optionnel mais recommandé):
   ```bash
   python -m venv venv
   source venv/bin/activate  # sur Windows: venv\Scripts\activate
   ```
2. Installe les dépendances:
   ```bash
   pip install -r requirements.txt
   ```
3. Lance l'application:
   ```bash
   python app.py
   ```
4. Ouvre ton navigateur sur: http://127.0.0.1:5000  (ou /api endpoints)

## Endpoints principaux (POST JSON)
- POST /api/compare {"text1":"...","text2":"..."}
- POST /api/clean-text {"text":"..."}
- POST /api/jaccard-similarity {"text1":"...","text2":"..."}
- POST /api/cosine-similarity {"text1":"...","text2":"..."}
- POST /api/common-words {"text1":"...","text2":"..."}
- POST /api/unique-words {"text1":"...","text2":"..."}
