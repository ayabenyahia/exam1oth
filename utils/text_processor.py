class TextProcessor:
    @staticmethod
    def nettoyer_texte(texte):
        """Nettoyer un texte : enlever la ponctuation, les majuscules, etc."""
        import re
        texte = texte.lower()
        texte = re.sub(r'[^a-zàâçéèêëîïôûùüÿñæœ\s]', '', texte)
        texte = re.sub(r'\s+', ' ', texte).strip()
        return texte
