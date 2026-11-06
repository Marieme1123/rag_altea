# ============================================================
# ÉTAPE 6 - GÉNÉRATION
# Q4. Complétez construire_prompt, puis affichez le prompt complet
#     envoyé pour une question (consigne, extraits, question).
# Q5. Posez 5 questions, dont 2 sans réponse dans la documentation,
#     et complétez le tableau (réponse juste ? sources citées ?
#     phrase de repli ?).
# Q6 ✍ Posez directement au LLM, sans extraits, la question sur le
#     télétravail. Comparez avec le RAG. Hallucination ?
# Q7 ✍ Pourquoi temperature=0 pour un assistant documentaire ?
# ============================================================
import ollama

from etape5_recherche import rechercher

LLM = "llama3.2"  # modèle Ollama installé en local
PHRASE_REPLI = "Je ne trouve pas cette information dans la documentation."

CONSIGNE = (
    "Tu es l'assistant de documentation interne d'Altéa Services.\n"
    "Réponds uniquement à partir des extraits ci-dessous, en français, "
    "en deux ou trois phrases maximum.\n"
    "Cite la source utilisée entre crochets, par exemple [teletravail.pdf, page 1].\n"
    f"Si les extraits ne contiennent pas la réponse, réponds exactement : « {PHRASE_REPLI} »\n"
    "N'invente rien."
)


def construire_prompt(question, resultats):
    extraits = "\n\n".join(
        f"[{i}] (source : {r['source']}, page {r['page']})\n{r['texte']}"
        for i, r in enumerate(resultats, start=1)
    )
    return f"{CONSIGNE}\n\nEXTRAITS :\n{extraits}\n\nQUESTION : {question}"


def generer(prompt):
    reponse = ollama.chat(
        model=LLM,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0},  # Q7 : réponse stable et factuelle
    )
    return reponse["message"]["content"].strip()


def repondre(question, k=3, service=None):
    resultats = rechercher(question, k=k, service=service)
    texte = generer(construire_prompt(question, resultats))
    return {"reponse": texte, "sources": resultats}


if __name__ == "__main__":
    # Q4 : prompt complet pour une question
    q = "Combien de jours de télétravail par semaine ?"
    print(construire_prompt(q, rechercher(q, k=3)))

    # Q5 : 5 questions dont 2 sans réponse dans la documentation
    questions = [
        "Combien de jours de télétravail par semaine ?",
        "Comment réinitialiser mon mot de passe ?",
        "Quel est le plafond pour un repas d'affaires avec un client ?",
        "Quel temps fera-t-il demain ?",
        "Quel est le salaire du directeur général ?",
    ]
    for q in questions:
        res = repondre(q)
        print("\n" + "=" * 70)
        print("QUESTION :", q)
        print("RÉPONSE  :", res["reponse"])
        print("SOURCES  :", sorted({f"{s['source']} p.{s['page']}" for s in res["sources"]}))

    # Q6 : le même LLM, sans extraits
    q = "Combien de jours de télétravail par semaine sont autorisés chez Altéa ?"
    print("\n" + "=" * 70)
    print("Q6 - SANS RAG :", generer(q))
    print("Q6 - AVEC RAG :", repondre(q)["reponse"])
