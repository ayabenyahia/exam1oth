// Calcul de la distance de Levenshtein
function levenshtein(a, b) {
  const matrix = Array.from({ length: a.length + 1 }, () =>
    Array(b.length + 1).fill(0)
  );

  for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
  for (let j = 0; j <= b.length; j++) matrix[0][j] = j;

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }

  return matrix[a.length][b.length];
}

// Calcul du taux de similarité
function calculerSimilarite(texte1, texte2) {
  const distance = levenshtein(texte1, texte2);
  const longueurMax = Math.max(texte1.length, texte2.length);
  return longueurMax === 0
    ? 100
    : ((1 - distance / longueurMax) * 100).toFixed(2);
}

// Diagnostic automatique avec couleur
function interpretation(taux) {
  taux = parseFloat(taux);
  let message = "";
  let couleur = "";

  if (taux < 15) {
    message = "Pas de plagiat";
    couleur = "green";
  } else if (taux < 30) {
    message = "Ressemblance faible (probablement reformulation)";
    couleur = "limegreen";
  } else if (taux < 50) {
    message = "Ressemblance moyenne (suspicion de plagiat partiel)";
    couleur = "orange";
  } else if (taux < 80) {
    message = "Forte similarité (probable plagiat)";
    couleur = "orangered";
  } else {
    message = "Plagiat confirmé (copie quasi directe)";
    couleur = "red";
  }

  return { message, couleur };
}

// Comparaison mot par mot
function genererDiff(texte1, texte2) {
  const mots1 = texte1.split(/\s+/);
  const mots2 = texte2.split(/\s+/);

  const maxLen = Math.max(mots1.length, mots2.length);
  let diff1 = "";
  let diff2 = "";

  for (let i = 0; i < maxLen; i++) {
    const mot1 = mots1[i] || "";
    const mot2 = mots2[i] || "";

    if (mot1 === mot2) {
      diff1 += `<span class="identique">${mot1}</span> `;
      diff2 += `<span class="identique">${mot2}</span> `;
    } else {
      if (mot1) diff1 += `<span class="different">${mot1}</span> `;
      if (mot2) diff2 += `<span class="different">${mot2}</span> `;
    }
  }

  return { diff1, diff2 };
}

// Événement du bouton
document.getElementById("comparerBtn").addEventListener("click", () => {
  const texte1 = document.getElementById("texte1").value.trim();
  const texte2 = document.getElementById("texte2").value.trim();

  const taux = calculerSimilarite(texte1, texte2);

  // Diagnostic automatique
  const { message, couleur } = interpretation(taux);
  const diagEl = document.getElementById("diagnostic");
  diagEl.textContent = message;
  diagEl.style.color = couleur;
  diagEl.style.fontWeight = "bold";

  // Barre principale = affichage du taux
  const progress = document.getElementById("progress-bar");
  progress.style.width = taux + "%";
  progress.style.backgroundColor = couleur;
  progress.textContent = taux + "% de similarité";

  // Comparaison visuelle
  const { diff1, diff2 } = genererDiff(texte1, texte2);
  document.getElementById("diff1").innerHTML = diff1;
  document.getElementById("diff2").innerHTML = diff2;
});
