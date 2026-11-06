# Assistant RAG pour la documentation interne d'Altéa Services

## Objectif
Prototype d'assistant qui répond aux questions des salariés à partir de la documentation interne (15 documents fictifs RH, IT et Général) et indique toujours le document source de la réponse (nom du fichier et page).

## Installation
Python 3.10 ou plus, puis :

```
pip install -r requirements.txt
```

Installer [Ollama](https://ollama.com) et télécharger le modèle utilisé pour la génération :

```
ollama pull llama3.2
```

Placer les documents dans `docs/RH`, `docs/IT` et `docs/General`.

## Ordre de lancement
1. `python etape1_collecte.py` : lecture des fichiers (nombre de pages par document)
2. `python etape2_nettoyage.py` : nettoyage du texte
3. `python etape3_decoupage.py` : découpage en chunks (taille retenue : 500 caractères, chevauchement 50)
4. `python etape4_indexation.py` : embeddings et indexation dans `base_vectorielle/`
5. `python etape5_recherche.py` : recherche des chunks les plus proches
6. `python etape6_generation.py` : réponses générées avec sources
7. `python etape7_evaluation.py` : évaluation (recherche, puis réponses)
8. `streamlit run app.py` : interface web

La base vectorielle n'est pas versionnée : elle se recrée avec l'étape 4.

## Exemple de question
> Combien de jours de télétravail par semaine ?

Réponse attendue : 2 jours maximum, jamais le mardi (source : `teletravail.pdf`, page 1).

## Résultats de l'évaluation (étape 7)
À compléter avec vos résultats :

| Indicateur | Résultat |
|---|---|
| Documents attendus retrouvés (k = 3) | ... / 10 |
| Réponses justes | ... % |
| Réponses correctement sourcées | ... % |

## Limites connues
- Les tableaux des PDF sont mal restitués par l'extraction de texte.
- Le filtre par service est choisi par l'utilisateur : ce n'est pas un contrôle d'accès.
- Le modèle local peut se tromper ou ignorer la consigne ; les sources affichées permettent de vérifier.
- Les documents modifiés doivent être réindexés à la main.

## Auteurs
Marième Mbaye Ndiaye (ajouter le binôme s'il y en a un)
