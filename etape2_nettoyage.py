# ============================================================
# ÉTAPE 2 - NETTOYAGE
# Q3. Appliquez nettoyer à toutes les pages et supprimez les
#     pages devenues vides.
# Q4. Affichez une même page avant et après nettoyage. Citez un
#     défaut qui reste et proposez une règle pour le corriger.
# ============================================================
import re

from etape1_collecte import collecter

# Q4 - règle ajoutée pour corriger le défaut restant :
# l'en-tête, le numéro de page et le pied de page répétés dans les PDF.
LIGNES_PARASITES = [
    r"^Altéa Services — Document interne — Diffusion restreinte$",
    r"^Document fictif réalisé à des fins pédagogiques$",
    r"^\d{1,3}$",  # ligne qui ne contient qu'un numéro de page
]


def nettoyer(texte):
    texte = texte.replace("\xa0", " ")           # espace insécable
    texte = re.sub(r"-\n(?=[a-zà-ÿ])", "", texte)  # mot coupé en fin de ligne
    lignes = []
    for ligne in texte.splitlines():
        ligne = re.sub(r"[ \t]+", " ", ligne).strip()  # espaces en trop
        if not ligne:                                  # lignes vides
            continue
        if any(re.match(motif, ligne) for motif in LIGNES_PARASITES):
            continue
        lignes.append(ligne)
    return "\n".join(lignes)


def nettoyer_pages(pages):
    propres = []
    for p in pages:
        texte = nettoyer(p["texte"])
        if texte:  # on supprime les pages devenues vides
            propres.append({**p, "texte": texte})
    return propres


if __name__ == "__main__":
    pages = collecter()
    propres = nettoyer_pages(pages)
    print(f"Pages avant : {len(pages)} | après : {len(propres)}")

    # Q4 : même page avant / après
    exemple = next(p for p in pages if p["source"] == "teletravail.pdf" and p["page"] == 1)
    print("\n--- AVANT ---")
    print(exemple["texte"][:400])
    print("\n--- APRÈS ---")
    print(nettoyer(exemple["texte"])[:400])