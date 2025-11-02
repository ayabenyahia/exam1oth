# exam1oth

Ceci est le readme de notre projet
Notre groupe est composé de :
1)SY El Hadji Bassirou
2)Benyahia Aya
3)Benchekchou Imane
4)Mabrouki Ferdaous

Ce projet est une application web de détection de plagiat textuel développée avec HTML, CSS, JavaScript pour le Frontend et Python utilisant flask comme API pour le Backend.
Elle permet de comparer deux textes et d’analyser leur taux de similarité grâce à TF-IDF (Term Frequency - Inverse Document Frequency), méthode d'IA ( Machine Learning et de NLP (Natural Language Processing)) utilisée pour évaluer l'importance d'un mot dans un texte par rapport à un ensemble de documents.

L’objectif est de fournir un outil simple, visuel et rapide permettant aux étudiants, enseignants, rédacteurs ou chercheurs de vérifier si un texte présente des ressemblances significatives avec un autre.

⚙️ Fonctionnalités principales

🧮 Calcul automatique du taux de similarité entre deux textes
→ basé sur la distance de Levenshtein pour une mesure fine mot par mot
→ basé sur Jaccard Similarity qui compare deux ensembles en calculant le rapport entre leurs éléments communs et leur union totale.
→ basé sur Cosine Similarity (Méthode vectorielle) pour mesurer la similarité entre deux textes en calculant l'angle entre leurs vecteurs de fréquence de mots.
→ basé sur TF-IDF (Intelligence Artificielle) pour une mesure fine mot par mot sans tenir compte des Mots courants ("le", "la", "de") → Peu importants

🎨 Affichage visuel dynamique avec une barre de progression colorée
→ la couleur change selon le niveau de ressemblance (vert → rouge)

💬 Diagnostic automatique du niveau de plagiat :

Moins de 15 % : Pas de plagiat

15 % à 30 % : Reformulation probable

30 % à 50 % : Suspicion partielle

50 % à 80 % : Plagiat probable

Plus de 80 % : Plagiat confirmé

🧩 Comparaison mot par mot avec surlignage des différences

⚡ Interface simple, fluide et responsive

🧰 Technologies utilisées

Frontend : HTML5, CSS3, JavaScript 

Backend : Python / Flask

Algorithme : - Distance de Levenshtein
             - Jaccard Similarity
             - Cosine Similarity (Méthode vectorielle)
             - TF-IDF ( Term Frequency - Inverse Document Frequency)

Frontend développé par : SY El Hadji Bassirou et Benyahia Aya

Backend développé par : Benchekchou Imane et Mabrouki Ferdaous
