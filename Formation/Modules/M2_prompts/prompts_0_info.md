# Module 02 – Function Calling & Prompt Engineering

## Objectifs
- Concevoir des prompts few-shot pour guider le LLM vers la bonne fonction.
- Créer une bibliothèque de gabarits classés par type de problème.
- Définir une méthodologie de test des prompts.

## Plan
1. **Analyse des fonctions** : catégoriser `function_definitions.json`.
2. **Atelier prompts** :
   - Format commun (contexte, contraintes, exemples, instruction finale).
   - 5 cas minimum : math, dates, manipulation de texte, conversions, logique.
3. **Tests** :
   - Interroger un LLM accessible (même hors projet) pour valider le format.
   - Mesurer le taux de réponses JSON valides.

## Ressources
- Fiche cours : `Formation/Modules/M2_prompts/cours.md`
- Exercices : `Formation/Modules/M2_prompts/exercices.md`
- Corrigés : `Formation/Modules/M2_prompts/corriges.md`

| Langue | Lien | Notes |
|--------|------|-------|
| FR (texte) | [Blog du Modérateur – Guide prompt engineering](https://www.blogdumoderateur.com/prompt-engineering-guide/) | Panorama complet en français. |
| FR (texte) | [HES-SO – Parler à l’IA](https://www.hes-so.ch/formation-devpro/parler-a-lia-ou-lessentiel-du-prompt-engineering) | Approche pédagogique. |
| FR (vidéo) | [Marketing Mania – « J’ai testé 100 prompts ChatGPT »](https://www.youtube.com/watch?v=9Zcj6n_0uS8) | Retours pratiques. |
| EN (texte) | [Prompting Guide](https://www.promptingguide.ai/) | Recueil de patterns. |
| EN (texte) | [Anthropic – Prompt design best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-design) | Conseils officiels. |
| EN (vidéo) | [freeCodeCamp – Prompt Engineering Full Course](https://www.youtube.com/watch?v=dOxUroR57xs) | Formation complète. |

## Exercices
1. Rédiger une fiche « prompt template » par catégorie.
2. Ajouter une section « erreurs fréquentes » dans chaque fiche.
3. Construire un script de test qui injecte un prompt dans un LLM (API libre / sandbox).

## Livrables
- Dossier `Formation/Prompts/` (à créer) contenant :
  - `math_prompt.md`, `string_prompt.md`, etc.
- Tableau de suivi (Google Sheet ou Markdown) consignant les essais.

## Critères
- Chaque template mentionne explicitement le format JSON attendu.
- Documentation des résultats de test (succès/échecs, hypothèses).

