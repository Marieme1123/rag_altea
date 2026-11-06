# ============================================================
# ÉTAPE 4 - EMBEDDINGS ET INDEXATION
# Q8.  Dimension d'un vecteur ? Combien de nombres à stocker pour
#      tout le corpus avec la taille de chunk retenue ?
# Q9.  (partie A) Lisez la matrice de similarité. Quelles phrases
#      sont proches ? Pourquoi 1 et 2, sans mot en commun ?
# Q10. (partie B) Enchaînez les étapes 1 à 4 dans un même script et
#      vérifiez : chunks indexés == chunks produits.
# Q11. Première recherche : 3 questions, 3 chunks les plus proches
#      avec leur source.
# Q12. Relancez le script : le nombre de chunks double-t-il ?
# ============================================================
from pathlib import Path

import chromadb
import numpy as np

from etape1_collecte import collecter
from etape2_nettoyage import nettoyer_pages
from etape3_decoupage import decouper_pages

MODELE = "paraphrase-multilingual-MiniLM-L12-v2"  # multilingue, bon en français
TAILLE, CHEVAUCHEMENT = 500, 50                   # taille retenue (Q7)
BASE_DIR = Path(__file__).parent / "base_vectorielle"
COLLECTION = "altea"


def charger_modele():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODELE)


def ouvrir_collection():
    client = chromadb.PersistentClient(path=str(BASE_DIR))
    return client.get_or_create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )


# ---------- Partie A : comprendre les embeddings (Q8, Q9) ----------
def partie_a(modele):
    phrases = [
        "Je peux travailler depuis chez moi.",
        "Le télétravail est autorisé deux jours par semaine.",
        "Comment réinitialiser mon mot de passe ?",
        "Le restaurant d'entreprise ouvre à midi.",
    ]
    vecteurs = modele.encode(phrases, normalize_embeddings=True)
    print("Dimension d'un vecteur :", vecteurs.shape[1])  # Q8

    matrice = vecteurs @ vecteurs.T  # vecteurs normalisés : produit = cosinus
    print("\nMatrice de similarité (cosinus) :")
    print(np.round(matrice, 2))                           # Q9


# ---------- Partie B : pipeline complet (Q10) ----------
def preparer_chunks():
    pages = collecter()                       # étape 1
    pages = nettoyer_pages(pages)             # étape 2
    return decouper_pages(pages, TAILLE, CHEVAUCHEMENT)  # étape 3


def indexer(chunks, modele, collection):
    """Étape 4 : embeddings + upsert (ré-exécutable sans doublons)."""
    textes = [c["texte"] for c in chunks]
    ids = [f"{c['source']}-p{c['page']}-c{c['chunk']}" for c in chunks]
    metadatas = [
        {"source": c["source"], "page": c["page"], "service": c["service"]}
        for c in chunks
    ]
    vecteurs = modele.encode(textes, normalize_embeddings=True).tolist()
    collection.upsert(ids=ids, documents=textes, embeddings=vecteurs, metadatas=metadatas)


# ---------- Q11 : première recherche ----------
def recherche_simple(question, modele, collection, k=3):
    vecteur = modele.encode([question], normalize_embeddings=True).tolist()
    res = collection.query(query_embeddings=vecteur, n_results=k)
    return list(zip(res["documents"][0], res["metadatas"][0], res["distances"][0]))


if __name__ == "__main__":
    modele = charger_modele()

    partie_a(modele)

    chunks = preparer_chunks()
    collection = ouvrir_collection()
    indexer(chunks, modele, collection)

    dim = len(modele.encode(["test"])[0])
    print(f"\nChunks produits : {len(chunks)} | indexés : {collection.count()}")  # Q10
    print(f"Q8 : {len(chunks)} chunks x {dim} dimensions = {len(chunks) * dim} nombres")

    questions = [
        "Combien de jours de télétravail par semaine ?",
        "Comment réinitialiser mon mot de passe ?",
        "Quel est le plafond pour un repas du midi en déplacement ?",
    ]
    for q in questions:  # Q11
        print("\n" + "=" * 70)
        print("QUESTION :", q)
        for texte, meta, distance in recherche_simple(q, modele, collection):
            score = 1 - distance  # distance cosinus -> similarité
            print(f"  [{score:.2f}] {meta['source']} (page {meta['page']}, {meta['service']})")
            print("        ", texte[:110].replace("\n", " "), "...")