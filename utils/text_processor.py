import re
import nltk

# Téléchargement automatique des stopwords
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

from nltk.corpus import stopwords
stop_words = set(stopwords.words("french"))

def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", "", text)
    tokens = text.split()
    tokens = [w for w in tokens if w not in stop_words]
    return tokens
