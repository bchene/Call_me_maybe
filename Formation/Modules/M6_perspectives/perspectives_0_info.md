# Module 06 – Perspectives & Bibliothèques Avancées

## Objectifs
- Comprendre ce que les bibliothèques interdites apporteraient (transformers, langchain, dspy, etc.).
- Préparer une feuille de route post-projet pour migrer vers ces outils si nécessaire.

## Plan
1. **Cartographie** : pour chaque lib interdite, préciser les fonctionnalités utiles (tokenizer intégré, gestion des prompts, outils fonction calling).
2. **Benchmark** : comparer notre pipeline bas niveau avec l’utilisation d’un framework haut niveau.
3. **Roadmap** : définir à quel moment ces outils deviennent rentables (maintenance, scalabilité, prototypage rapide).

## Ressources
- Fiche cours : `Formation/Modules/M6_perspectives/cours.md`
- Exercices : `Formation/Modules/M6_perspectives/exercices.md`
- Corrigés : `Formation/Modules/M6_perspectives/corriges.md`

| Langue | Lien | Notes |
|--------|------|-------|
| FR (texte) | [LeMondeInformatique – LangChain](https://www.lemondeinformatique.fr/actualites/lire-langchain-comment-ce-framework-simplifie-les-projets-ia-generative-91470.html) | Article sur les usages en entreprise. |
| FR (texte) | [DataScientest – Guide transformers](https://datascientest.com/transformers-guide-complet) | Présentation des Transformers. |
| EN (texte) | [LangChain docs](https://python.langchain.com/docs/get_started/introduction) | Documentation officielle. |
| EN (texte) | [Hugging Face – Function calling blog](https://huggingface.co/blog/function-calling) | Utilisation haut niveau. |
| EN (vidéo) | [James Briggs – LangChain Crash Course](https://www.youtube.com/watch?v=aywZrzNaKjs) | Tour d’horizon. |
| EN (vidéo) | [Harrison Chase – LangChain Agents & Tools](https://www.youtube.com/watch?v=_wY6uFYyP0w) | Cas avancés. |

## Exercices
1. Construire un tableau « besoin → solution bas niveau → solution lib avancée ».
2. Écrire un court script (hors projet) utilisant `transformers` ou `langchain` pour comparer.
3. Rédiger une note de synthèse (1 page) : quand migrer, pourquoi, risques.

## Livrables
- `Doc/perspectives/bibliotheques_avancees.md`.
- Tableau comparatif (format Markdown ou spreadsheet).

## Critères
- La note explique clairement les bénéfices/limites de chaque lib.
- Les risques (dépendances, coût, interprétabilité) sont identifiés.

