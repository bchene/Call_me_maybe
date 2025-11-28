# Module 04 – Interaction LLM & Pipeline Complet

## Objectifs
- Implémenter la boucle token-par-token avec `Small_LLM_Model`.
- Relier tokenisation → LLM → décodage → parsing → validation.
- Instrumenter la génération (logs, métriques simples).

## Plan
1. **Préparation** : stub `llm_interaction.py`, `decoder.py`, `parser.py`.
2. **Boucle** :
   ```python
   while not stop_condition:
       logits = model.get_logits_from_input_ids(ids)
       next_token = greedy_select(logits)
       ids = append(ids, next_token)
   ```
3. **Parsing & validation** : brancher Module 03 pour contrôler le JSON généré.
4. **Instrumentation** : logs (token choisi, proba, temps de boucle).

## Ressources
- Fiche cours : `Formation/Modules/M4_pipeline/cours.md`
- Exercices : `Formation/Modules/M4_pipeline/exercices.md`
- Corrigés : `Formation/Modules/M4_pipeline/corriges.md`

| Langue | Lien | Notes |
|--------|------|-------|
| FR (texte) | [NUMA – Grands modèles de langage : explications](https://numa.co/fr/blog/grands-modeles-de-langage-explications) | Vulgarisation de l’inférence. |
| EN (texte) | [Stability AI – Autoregressive text generation](https://stability.ai/blog/understanding-autoregressive-text-generation) | Détails sur la boucle. |
| EN (texte) | [OpenAI Cookbook – Sampling strategies](https://cookbook.openai.com/examples/how_to_sample_from_language_models) | Comparaison des stratégies de sélection. |
| EN (vidéo) | [Corey Schafer – Python Logging Tutorial](https://www.youtube.com/watch?v=-ARI4Cz-awo) | Structuration des logs. |
| EN (vidéo) | [James Briggs – LangChain Crash Course](https://www.youtube.com/watch?v=aywZrzNaKjs) | Inspiration pour frameworks (perspective). |

## Exercices
1. Implémenter `greedy_select(logits)` et ajouter un paramètre `top_k` optionnel.
2. Détecter automatiquement la fin d’un JSON valide (compteur d’accolades).
3. Journaliser les séquences invalides et prévoir une tentative de correction.

## Livrables
- Prototype fonctionnel de `llm_interaction.py`.
- Rapport court décrivant les métriques collectées.

## Critères
- Aucun crash lorsque le LLM renvoie une sortie vide.
- Logs exploitables pour rejouer un scénario.

