from flask import Flask, jsonify
from flask_cors import CORS
from controllers.plagiat_controller import plagiat_bp

app = Flask(__name__)
app.config['DEBUG'] = True  # ← Ajoute cette ligne
app.config['PROPAGATE_EXCEPTIONS'] = True  # ← Et celle-ci

CORS(app)

app.register_blueprint(plagiat_bp)

@app.route('/')
def home():
    return jsonify({
        'message': 'API de détection de plagiat',
        'status': 'opérationnel'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)