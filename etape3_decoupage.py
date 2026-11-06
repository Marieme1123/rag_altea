# ============================================================
# ÉTAPE 3 - DÉCOUPAGE (CHUNKING)
# Q5. Complétez decouper. Vérifiez :
#     decouper("abcdefghij", taille=4, chevauchement=1)
#     doit renvoyer ["abcd", "defg", "ghij"].
# Q6. Découpez tout le corpus avec trois tailles et complétez le
#     tableau (taille, chevauchement, nombre de chunks, longueur
#     moyenne).
# ============================================================
from etape1_collecte import collecter
from etape2_nettoyage import nettoyer_pages


def decouper(texte, taille=500, chevauchement=50):
    if chevauchement >= taille:
        raise ValueError("Le chevauchement doit être plus petit que la taille")
    chunks = []
    debut = 0
    while debut < len(texte):
        chunks.append(texte[debut:debut + taille])
        if debut + taille >= len(texte):  # le dernier chunk touche la fin
            break
        debut += taille - chevauchement   # on avance de (taille - chevauchement)
    return chunks


def decouper_pages(pages, taille=500, chevauchement=50):
    """Découpe chaque page et garde source, page, service pour chaque chunk."""
    chunks = []
    for p in pages:
        for i, morceau in enumerate(decouper(p["texte"], taille, chevauchement)):
            chunks.append({
                "texte": morceau,
                "source": p["source"],
                "page": p["page"],
                "service": p["service"],
                "chunk": i,
            })
    return chunks


if __name__ == "__main__":
    # Q5 : test
    resultat = decouper("abcdefghij", taille=4, chevauchement=1)
    print(resultat)
    assert resultat == ["abcd", "defg", "ghij"]

    # Q6 : tableau
    pages = nettoyer_pages(collecter())
    print(f"\n{'Taille':>7} {'Chevauch.':>10} {'Nb chunks':>10} {'Long. moy.':>11}")
    for taille, chev in [(200, 20), (500, 50), (1000, 100)]:
        chunks = decouper_pages(pages, taille, chev)
        moyenne = sum(len(c["texte"]) for c in chunks) / len(chunks)
        print(f"{taille:>7} {chev:>10} {len(chunks):>10} {moyenne:>11.0f}")