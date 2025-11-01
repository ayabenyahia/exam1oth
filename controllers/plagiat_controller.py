from flask import Blueprint, request, jsonify
from models.text_analyzer import TextAnalyzer

# Création du Blueprint
plagiat_bp = Blueprint('plagiat', __name__)

# Instance du modèle
analyzer = TextAnalyzer()

# Seuil de similarité pour l'ajout à la liste noire (80%)
BLACKLIST_THRESHOLD = 80.0

def get_user_identifier():
    """
    Récupère un identifiant unique pour l'utilisateur.
    Utilise l'adresse IP si aucun ID utilisateur n'est disponible.
    En production, ceci devrait être un ID utilisateur de session/login.
    """
    # X-Forwarded-For est couramment utilisé par les proxies/load balancers
    return request.headers.get('X-Forwarded-For', request.remote_addr)

# ========================================
# ROUTE 1 : Health Check
# ========================================
@plagiat_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Vérifie que l'API fonctionne
    Test: GET http://localhost:5000/api/health
    """
    return jsonify({
        'status': 'OK',
        'message': 'API de détection de plagiat opérationnelle',
        'version': '1.0'
    }), 200


# ========================================
# ROUTE 2 : Nettoyage de texte uniquement
# ========================================
@plagiat_bp.route('/api/clean-text', methods=['POST'])
def clean_text():
    """
    Nettoie un texte (minuscules, sans ponctuation, espaces normalisés)
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Le champ "text" est requis',
                'success': False
            }), 400
        
        text = data['text']
        
        if not text.strip():
            return jsonify({
                'error': 'Le texte ne peut pas être vide',
                'success': False
            }), 400
        
        # Nettoyage
        cleaned = analyzer.processor.clean_text(text)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'cleaned_text': cleaned
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 3 : Extraction de mots uniquement
# ========================================
@plagiat_bp.route('/api/extract-words', methods=['POST'])
def extract_words():
    """
    Extrait les mots d'un texte
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Le champ "text" est requis',
                'success': False
            }), 400
        
        text = data['text']
        
        if not text.strip():
            return jsonify({
                'error': 'Le texte ne peut pas être vide',
                'success': False
            }), 400
        
        # Nettoyage puis extraction
        cleaned = analyzer.processor.clean_text(text)
        words = analyzer.processor.extract_words(cleaned)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'cleaned_text': cleaned,
            'words': words,
            'word_count': len(words)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 4 : Similarité Jaccard uniquement
# ========================================
@plagiat_bp.route('/api/jaccard-similarity', methods=['POST'])
def jaccard_similarity():
    """
    Calcule uniquement la similarité de Jaccard
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        # Extraction
        words1 = analyzer.processor.extract_words(clean1)
        words2 = analyzer.processor.extract_words(clean2)
        
        # Calcul Jaccard
        jaccard = analyzer._calculate_jaccard_similarity(words1, words2)
        
        return jsonify({
            'success': True,
            'method': 'Jaccard Similarity',
            'similarity_percentage': round(jaccard * 100, 2),
            'details': {
                'words_text1': len(words1),
                'words_text2': len(words2),
                'common_words': len(set(words1) & set(words2)),
                'total_unique_words': len(set(words1) | set(words2))
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 5 : Similarité Cosinus uniquement
# ========================================
@plagiat_bp.route('/api/cosine-similarity', methods=['POST'])
def cosine_similarity():
    """
    Calcule uniquement la similarité cosinus
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        # Extraction
        words1 = analyzer.processor.extract_words(clean1)
        words2 = analyzer.processor.extract_words(clean2)
        
        # Calcul Cosinus
        cosine = analyzer._calculate_cosine_similarity(words1, words2)
        
        return jsonify({
            'success': True,
            'method': 'Cosine Similarity',
            'similarity_percentage': round(cosine * 100, 2),
            'details': {
                'words_text1': len(words1),
                'words_text2': len(words2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 6 : Mots communs uniquement
# ========================================
@plagiat_bp.route('/api/common-words', methods=['POST'])
def common_words():
    """
    Identifie les mots communs entre deux textes
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage et extraction
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        words1 = set(analyzer.processor.extract_words(clean1))
        words2 = set(analyzer.processor.extract_words(clean2))
        
        # Mots communs
        common = words1 & words2
        
        return jsonify({
            'success': True,
            'common_words': sorted(list(common)),
            'common_count': len(common)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 7 : Mots uniques uniquement
# ========================================
@plagiat_bp.route('/api/unique-words', methods=['POST'])
def unique_words():
    """
    Identifie les mots uniques à chaque texte
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage et extraction
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        words1 = set(analyzer.processor.extract_words(clean1))
        words2 = set(analyzer.processor.extract_words(clean2))
        
        # Mots uniques
        unique1 = words1 - words2
        unique2 = words2 - words1
        
        return jsonify({
            'success': True,
            'unique_text1': sorted(list(unique1)),
            'unique_text2': sorted(list(unique2)),
            'unique_count_text1': len(unique1),
            'unique_count_text2': len(unique2)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 8 : Comparaison complète (avec logique de Blacklist)
# ========================================
@plagiat_bp.route('/api/compare', methods=['POST'])
def compare_texts():
    """
    Comparaison complète avec toutes les métriques et vérification de la liste noire.
    """
    user_id = get_user_identifier()
    
    # 1. VÉRIFICATION DE LA LISTE NOIRE
    if analyzer.blacklist_model.is_blacklisted(user_id):
        return jsonify({
            'error': f'Accès refusé. Votre identifiant ({user_id}) est dans la liste noire pour plagiat élevé.',
            'success': False
        }), 403 # Forbidden
        
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # 2. Analyse complète
        result = analyzer.analyze_similarity(text1, text2)
        similarity_percentage = result['similarity_percentage']
        
        # 3. LOGIQUE D'AJOUT À LA LISTE NOIRE
        if similarity_percentage >= BLACKLIST_THRESHOLD:
            analyzer.blacklist_model.add_to_blacklist(user_id, similarity_percentage)
            result['warning'] = f"Attention: Taux de similarité ({similarity_percentage}%) est >= {BLACKLIST_THRESHOLD}%. Identifiant ajouté/mis à jour dans la liste noire."
        
        return jsonify({
            'success': True,
            'similarity_percentage': similarity_percentage,
            'method_used': result['method_used'],
            'details': result['details'],
            'user_id_used': user_id,
            'warning': result.get('warning')
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 9 : Comparaison avec highlight (avec logique de Blacklist)
# ========================================
@plagiat_bp.route('/api/compare-with-highlight', methods=['POST'])
def compare_with_highlight():
    """
    Comparaison avec mise en évidence des différences et vérification de la liste noire.
    """
    user_id = get_user_identifier()

    # 1. VÉRIFICATION DE LA LISTE NOIRE
    if analyzer.blacklist_model.is_blacklisted(user_id):
        return jsonify({
            'error': f'Accès refusé. Votre identifiant ({user_id}) est dans la liste noire pour plagiat élevé.',
            'success': False
        }), 403 # Forbidden
        
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # 2. Analyse avec différences
        result = analyzer.analyze_with_differences(text1, text2)
        similarity_percentage = result['similarity_percentage']

        # 3. LOGIQUE D'AJOUT À LA LISTE NOIRE
        if similarity_percentage >= BLACKLIST_THRESHOLD:
            analyzer.blacklist_model.add_to_blacklist(user_id, similarity_percentage)
            result['warning'] = f"Attention: Taux de similarité ({similarity_percentage}%) est >= {BLACKLIST_THRESHOLD}%. Identifiant ajouté/mis à jour dans la liste noire."
        
        return jsonify({
            'success': True,
            'similarity_percentage': similarity_percentage,
            'method_used': result['method_used'],
            'common_words': result['common_words'],
            'unique_text1': result['unique_text1'],
            'unique_text2': result['unique_text2'],
            'details': result['details'],
            'user_id_used': user_id,
            'warning': result.get('warning')
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500
