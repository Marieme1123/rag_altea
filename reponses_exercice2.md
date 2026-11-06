# Réponses - Exercice 2 : interroger, évaluer et livrer

## Étape 5 - Recherche

**Q1.** Code : `rechercher` dans `etape5_recherche.py`. Le script affiche, pour 3 questions, source, page et score de chaque chunk.

**Q2 ✍ k = 1, 3 et 10 : que gagne-t-on, que perd-on quand k augmente ?**
- On **gagne** en couverture : plus de chances que le bon chunk soit dans les résultats, surtout si l'information est répartie sur deux chunks ou si la question est vague.
- On **perd** en précision : plus de chunks hors sujet (leurs scores baissent), un prompt plus long donc plus lent et plus coûteux, et un LLM qui peut se laisser distraire par des extraits qui ne répondent pas à la question.
- k = 1 est précis mais fragile (si le premier résultat est le mauvais, tout est faux) ; k = 3 est un bon compromis ; k = 10 ajoute surtout du bruit. (Compléter avec tes observations sur les scores.)

**Q3 ✍ `service="RH"` puis `service="IT"`.**
Avec `RH`, on retrouve les chunks de `teletravail.pdf`. Avec `IT`, la recherche ne renvoie que des chunks du service IT, moins pertinents, même pour une question RH : le filtre change l'ensemble de documents dans lequel on cherche.
C'est une **première étape vers la confidentialité** : un service ne voit que ses documents. Mais il **ne suffit pas** : le service est choisi par l'utilisateur (menu), donc n'importe qui peut choisir un autre service ; il n'y a pas d'authentification, pas de droits par salarié, et le filtre ne protège pas les documents eux-mêmes. Il faut identifier le salarié et appliquer ses droits côté serveur, avant la recherche.

## Étape 6 - Génération

**Q4.** Code : `construire_prompt` dans `etape6_generation.py`. Le prompt a 3 parties : la **consigne** (répondre uniquement avec les extraits, citer la source, phrase de repli si la réponse est absente), les **extraits** (numérotés, avec source et page) et la **question**.

**Q5.** Lancer `python etape6_generation.py`, puis remplir le tableau avec tes 5 réponses :

| Question | Réponse juste ? | Sources citées ? | Phrase de repli quand il le fallait ? |
|---|---|---|---|
| Combien de jours de télétravail par semaine ? | | | sans objet |
| Comment réinitialiser mon mot de passe ? | | | sans objet |
| Quel est le plafond pour un repas d'affaires avec un client ? | | | sans objet |
| Quel temps fera-t-il demain ? (sans réponse) | sans objet | | |
| Quel est le salaire du directeur général ? (sans réponse) | sans objet | | |

**Q6 ✍ Question posée directement au LLM, sans extraits.**
Une **hallucination** est une réponse qui paraît plausible mais qui est inventée ou non fondée. Le LLM seul ne connaît pas la règle d'Altéa (entreprise fictive) : il invente un nombre de jours ou donne une règle générale. Le RAG lui fournit le texte de `teletravail.pdf` (2 jours maximum, jamais le mardi) et lui interdit de répondre en dehors des extraits, avec une phrase de repli quand l'information manque. Il limite les hallucinations sans les supprimer : si le mauvais chunk est trouvé, ou si le modèle ignore la consigne, l'erreur reste possible, d'où les sources affichées. (Compléter avec les deux réponses obtenues.)

**Q7 ✍ Pourquoi `temperature=0` ?**
À 0, le modèle choisit toujours le mot le plus probable : les réponses sont stables et reproductibles (la même question donne la même réponse), ce qui est nécessaire pour évaluer l'assistant et lui faire confiance. Un assistant documentaire doit rester fidèle aux documents et non créatif.

## Étape 7 - Évaluation

**Q8.** Fichier `evaluation.csv` : 10 questions, le document attendu et la réponse attendue.

**Q9.** `python etape7_evaluation.py` affiche, pour k = 1, 3 et 5, combien de documents attendus sont retrouvés. Résultat à noter : ... / 10 (... %) avec k = 3.

**Q10.** Le même script génère `resultats_generation.csv`. Ouvre-le dans Excel, remplis `jugement` (juste / partielle / fausse) et `sources_ok` (oui / non), enregistre, puis lance `python etape7_evaluation.py notes` pour obtenir les pourcentages.

**Q11 ✍ Une réponse fausse.**
À compléter avec ta réponse fausse, en suivant cette méthode :
1. Regarde si `document_attendu` figure dans les sources retrouvées (résultat de Q9). Si non : l'erreur vient de la **recherche** ; si oui : elle vient de la **génération**.
2. Améliorations à tester selon le cas : recherche en défaut, augmenter k (5) ou changer la taille des chunks (par exemple 1000) ; génération en défaut, durcir la consigne (« recopie le chiffre exact ») ou donner moins d'extraits.
3. Relance l'évaluation et note le nouveau résultat (avant : ... %, après : ... %).
Pistes probables d'erreur sur ce corpus (à vérifier) : le plafond de repas, car le tableau est mal restitué, et le télétravail, où il faut mentionner « jamais le mardi ».

## Étape 8 - Mise à disposition et GitHub

**Q12.** Code : `app.py`. Lancer `streamlit run app.py`, poser une question, puis faire une capture d'écran de la réponse avec ses sources.

**Q13.** Fichier `README.md` (objectif, installation, ordre de lancement, exemple, résultats, limites, auteurs) et `requirements.txt`. Compléter les résultats de l'étape 7 avant de publier :
```
git add .
git commit -m "Exercice 2 : recherche, génération, évaluation, interface Streamlit"
git push
```

**Q14 ✍ Quatre points avant de proposer l'assistant à tous les salariés.**
1. **Droits d'accès selon le salarié** : certains documents sont à diffusion restreinte. Il faut authentifier le salarié (annuaire de l'entreprise) et filtrer côté serveur selon ses droits, avant la recherche, et non avec un menu qu'il choisit.
2. **Données personnelles** : de vrais documents peuvent contenir des noms, des salaires ou des informations de santé. Il faut respecter le RGPD (retirer ou anonymiser ces données, limiter ce qui est envoyé à un service externe, protéger les journaux de questions).
3. **Mise à jour des documents** : un document obsolète donne une réponse fausse. Il faut une réindexation automatique (détection des fichiers modifiés, suppression des anciens chunks) et des dates de version dans les métadonnées.
4. **Coût et hébergement du LLM** : un petit modèle local est gratuit mais limité et demande une machine adaptée. En production, il faut un serveur ou une API payante, avec un coût par requête, de la latence, de la disponibilité et le choix du lieu d'hébergement des données.
