# Module 03 – Validation JSON & Pydantic

## Objectifs
- Modéliser toutes les entrées/sorties avec Pydantic.
- Garantir des messages d’erreur clairs et actionnables.

## Plan
1. Créer `models.py` avec :
   - `PromptItem`, `FunctionDefinition`, `FunctionArgument`, `FunctionCallResult`.
2. Écrire des validateurs personnalisés (conversion float, trimming str, etc.).
3. Intégrer la validation dans le pipeline (early fail).

## Ressources
- Fiche cours : `Formation/Modules/M3_validation/cours.md`
- Exercices : `Formation/Modules/M3_validation/exercices.md`
- Corrigés : `Formation/Modules/M3_validation/corriges.md`

| Langue | Lien | Notes |
|--------|------|-------|
| FR (texte) | [Real Python – Pydantic (version FR)](https://realpython.com/fr/python-pydantic/) | Tutoriel détaillé. |
| EN (texte) | [Pydantic docs](https://docs.pydantic.dev/latest/) | Référence officielle. |
| EN (texte) | [FastAPI docs – Body](https://fastapi.tiangolo.com/tutorial/body/) | Exemples orientés API. |
| EN (vidéo) | [ArjanCodes – Data validation in Python with Pydantic](https://www.youtube.com/watch?v=Vj-iWWuQj7E) | Démonstration pratique. |

## Exercices
1. Charger `function_definitions.json` via un modèle Pydantic.
2. Simuler 3 erreurs :
   - JSON invalide.
   - Type incorrect (string vs float).
   - Clé manquante.
3. Documenter la stratégie de message utilisateur.

## Livrables
- `src/models.py` (brouillon) + fichier de tests rapide.
- Note `Formation/Notes/pydantic_insights.md`.

## Critères
- Tous les champs critiques sont typés.
- Les erreurs Pydantic sont capturées et reformulées.

