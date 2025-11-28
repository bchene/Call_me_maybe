# Module 05 – Robustesse, QA & Tests

## Objectifs
- Formaliser la gestion d’erreurs (skip, retry, fallback).
- Mettre en place des tests automatisés et du linting.

## Plan
1. Lister toutes les erreurs possibles (I/O, JSON, LLM, validation).
2. Définir pour chacune : message utilisateur, action automatique.
3. Écrire des tests unitaires ciblés + un test d’intégration minimal.
4. Configurer `make lint` + `make test`.

## Ressources
- Fiche cours : `Formation/Modules/M5_quality/cours.md`
- Exercices : `Formation/Modules/M5_quality/exercices.md`
- Corrigés : `Formation/Modules/M5_quality/corriges.md`

| Langue | Lien | Notes |
|--------|------|-------|
| FR (texte) | [OpenClassrooms – Gérer les erreurs en Python](https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/233326-gerer-les-erreurs) | Rappels fondamentaux. |
| EN (texte) | [Real Python – Python Exceptions](https://realpython.com/python-exceptions/) | Bonnes pratiques. |
| EN (texte) | [flake8 docs](https://flake8.pycqa.org/en/latest/) | Référence lint. |
| EN (vidéo) | [TestDriven – Python Exception Handling Best Practices](https://www.youtube.com/watch?v=nlCKrKGHSSk) | Vidéo synthétique. |
| EN (vidéo) | [Corey Schafer – Python unittest Crash Course](https://www.youtube.com/watch?v=6tNS--WetLI) | Tests unitaires. |

## Exercices
1. Créer un fichier `docs/error_matrix.md` avec : erreur, origine, message, action.
2. Simuler un JSON corrompu et vérifier que le programme continue.
3. Ajouter un test qui vérifie que le fichier de sortie est un JSON valide.

## Livrables
- Matrice des erreurs.
- Dossier `tests/` avec au moins 3 tests.
- Rapport court sur la couverture (même approximative).

## Critères
- Les erreurs prévues ne font jamais planter l’application.
- `make lint` et `make test` passent sans warning.

