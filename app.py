from flask import Flask, render_template
from flask_cors import CORS
from controllers.plagiat_controller import plagiat_bp

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration CORS pour permettre les requêtes cross-origin
CORS(app)

# Enregistrement du Blueprint du contrôleur
app.register_blueprint(plagiat_bp)

# Route principale pour servir le frontend
@app.route('/')
def index():
    """
    Route qui sert la page d'accueil (interface utilisateur)
    """
    return render_template('index.html')

# Point d'entrée de l'application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)