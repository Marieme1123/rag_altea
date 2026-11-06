# ============================================================
# ÉTAPE 7 - ÉVALUATION
# Q8.  Créez evaluation.csv avec 10 questions et le document qui
#      contient la réponse (fichier evaluation.csv).
# Q9.  Complétez le calcul du taux de réussite de la recherche.
# Q10. Notez vous-mêmes les 10 réponses générées (juste, partielle
#      ou fausse ; sources exactes ou non) et donnez les pourcentages.
# Q11 ✍ Choisissez une réponse fausse : le bon document avait-il été
#      trouvé à l'étape 5 ? Proposez une amélioration, testez-la.
#
# Utilisation :
#   python etape7_evaluation.py           -> Q9 + génère resultats_generation.csv
#   python etape7_evaluation.py notes     -> Q10 (après avoir rempli le CSV)
# ============================================================
import csv
import sys
from pathlib import Path

from etape5_recherche import rechercher

DOSSIER = Path(__file__).parent
EVAL_CSV = DOSSIER / "evaluation.csv"
RESULTATS_CSV = DOSSIER / "resultats_generation.csv"


def lire_questions():
    with open(EVAL_CSV, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


# ---------- Q9 : taux de réussite de la recherche ----------
def taux_recherche(k=3, verbose=True):
    lignes = lire_questions()
    reussites = 0
    for ligne in lignes:
        sources = [r["source"] for r in rechercher(ligne["question"], k=k)]
        trouve = ligne["document_attendu"] in sources
        reussites += trouve
        if verbose:
            print(f"  {'OK ' if trouve else 'RATÉ'} | {ligne['question']}")
            if not trouve:
                print(f"         attendu : {ligne['document_attendu']} | obtenu : {sources}")
    taux = 100 * reussites / len(lignes)
    print(f"\nk = {k} : {reussites}/{len(lignes)} documents attendus retrouvés ({taux:.0f} %)")
    return taux


# ---------- Q10 : générer les réponses à noter ----------
def generer_reponses(k=3):
    from etape6_generation import repondre  # import ici : demande Ollama

    lignes = lire_questions()
    with open(RESULTATS_CSV, "w", encoding="utf-8-sig", newline="") as f:
        champs = ["question", "document_attendu", "reponse_attendue", "reponse_generee",
                  "sources_citees", "jugement", "sources_ok"]
        ecrivain = csv.DictWriter(f, fieldnames=champs, delimiter=";")
        ecrivain.writeheader()
        for ligne in lignes:
            res = repondre(ligne["question"], k=k)
            ecrivain.writerow({
                "question": ligne["question"],
                "document_attendu": ligne["document_attendu"],
                "reponse_attendue": ligne["reponse_attendue"],
                "reponse_generee": res["reponse"].replace("\n", " "),
                "sources_citees": " | ".join(sorted({s["source"] for s in res["sources"]})),
                "jugement": "",    # à remplir : juste / partielle / fausse
                "sources_ok": "",  # à remplir : oui / non
            })
            print("fait :", ligne["question"])
    print(f"\nOuvrez {RESULTATS_CSV.name} dans Excel et remplissez les 2 dernières colonnes.")


def calculer_notes():
    with open(RESULTATS_CSV, encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.DictReader(f, delimiter=";"))
    n = len(lignes)
    justes = sum(1 for l in lignes if l["jugement"].strip().lower() == "juste")
    partielles = sum(1 for l in lignes if l["jugement"].strip().lower() == "partielle")
    sources = sum(1 for l in lignes if l["sources_ok"].strip().lower() == "oui")
    print(f"Réponses justes      : {justes}/{n} ({100 * justes / n:.0f} %)")
    print(f"Réponses partielles  : {partielles}/{n} ({100 * partielles / n:.0f} %)")
    print(f"Sources exactes      : {sources}/{n} ({100 * sources / n:.0f} %)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "notes":
        calculer_notes()
    else:
        print("=== Q9 : qualité de la recherche ===")
        for k in (1, 3, 5):  # Q11 : comparer plusieurs valeurs de k
            taux_recherche(k=k, verbose=(k == 3))
            print()
        generer_reponses(k=3)
