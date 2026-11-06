# ============================================================
# ÉTAPE 5 - RECHERCHE
# Q1. Complétez rechercher et affichez les résultats (source,
#     page, score) pour 3 questions de salariés.
# Q2 ✍ Essayez k = 1, 3 et 10 sur une même question. Que gagne-t-on
#     et que perd-on quand k augmente ?
# Q3 ✍ Relancez une question RH avec service="RH", puis "IT".
#     Qu'observez-vous ? En quoi ce filtre est-il une première étape
#     vers la confidentialité, et pourquoi ne suffit-il pas ?
# ============================================================
from functools import lru_cache

from etape4_indexation import charger_modele, ouvrir_collection


@lru_cache(maxsize=1)
def _modele():
    return charger_modele()  # chargé une seule fois


@lru_cache(maxsize=1)
def _collection():
    return ouvrir_collection()


def rechercher(question, k=3, service=None):
    """Retourne les k chunks les plus proches de la question.
    service="RH" / "IT" / "General" restreint la recherche à ce service."""
    vecteur = _modele().encode([question], normalize_embeddings=True).tolist()
    filtre = {"service": service} if service else None
    res = _collection().query(query_embeddings=vecteur, n_results=k, where=filtre)

    resultats = []
    for texte, meta, distance in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        resultats.append({
            "texte": texte,
            "source": meta["source"],
            "page": meta["page"],
            "service": meta["service"],
            "score": 1 - distance,  # distance cosinus -> similarité
        })
    return resultats


def afficher(resultats):
    for r in resultats:
        print(f"  [{r['score']:.2f}] {r['source']} (page {r['page']}, {r['service']})")


if __name__ == "__main__":
    # Q1
    questions = [
        "Combien de jours de télétravail par semaine ?",
        "Comment réinitialiser mon mot de passe ?",
        "Quel est le plafond pour un repas du midi en déplacement ?",
    ]
    for q in questions:
        print("\nQUESTION :", q)
        afficher(rechercher(q, k=3))

    # Q2 : même question avec k = 1, 3 et 10
    q = "Combien de jours de télétravail par semaine ?"
    for k in (1, 3, 10):
        print(f"\n--- Q2 : k = {k} ---")
        afficher(rechercher(q, k=k))

    # Q3 : même question RH, filtrée sur RH puis sur IT
    for service in ("RH", "IT"):
        print(f"\n--- Q3 : service = {service} ---")
        afficher(rechercher(q, k=3, service=service))
