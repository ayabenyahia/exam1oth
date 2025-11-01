from flask import Flask, jsonify
from flask_cors import CORS
from controllers.plagiat_controller import plagiat_bp

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration CORS
CORS(app)

# Enregistrement du Blueprint du contrôleur
app.register_blueprint(plagiat_bp)

# Route de base (juste pour confirmer que ça marche)
@app.route('/')
def home():
    return jsonify({
        'message': 'API de détection de plagiat',
        'status': 'opérationnel',
        'routes_disponibles': [
            'GET  /api/health',
            'POST /api/clean-text',
            'POST /api/extract-words',
            'POST /api/jaccard-similarity',
            'POST /api/cosine-similarity',
            'POST /api/common-words',
            'POST /api/unique-words',
            'POST /api/compare',
            'POST /api/compare-with-highlight'
        ]
    })

# Point d'entrée de l'application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)