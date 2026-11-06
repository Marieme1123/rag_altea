## etape1_collecte.py
# ============================================================
# ÉTAPE 1 - COLLECTE
# Q1. Complétez le code et affichez le nombre de pages lues
#     pour chaque document.
# ============================================================


from collections import Counter
from pathlib import Path

from pypdf import PdfReader

DOCS_DIR = Path(__file__).parent / "docs"


def collecter(dossier=DOCS_DIR):
    """Lit tous les PDF et .txt. Retourne une liste de pages :
    {"texte", "source" (nom du fichier), "page", "service"}."""
    pages = []
    for chemin in sorted(Path(dossier).rglob("*")):
        extension = chemin.suffix.lower()
        service = chemin.parent.name  # RH, IT ou General

        if extension == ".pdf":
            lecteur = PdfReader(chemin)
            for numero, page in enumerate(lecteur.pages, start=1):
                pages.append({
                    "texte": page.extract_text() or "",
                    "source": chemin.name,
                    "page": numero,
                    "service": service,
                })
        elif extension == ".txt":
            pages.append({
                "texte": chemin.read_text(encoding="utf-8"),
                "source": chemin.name,
                "page": 1,  # un fichier texte = une seule "page"
                "service": service,
            })
    return pages


if __name__ == "__main__":
    pages = collecter()
    nb_pages = Counter((p["service"], p["source"]) for p in pages)
    for (service, source), n in nb_pages.items():
        print(f"{service:8} {source:28} {n} page(s)")
    print(f"\nTotal : {len(nb_pages)} documents, {len(pages)} pages")