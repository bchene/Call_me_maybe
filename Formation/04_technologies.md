# Phase 3 - Technologies & Outils

Ce document recense les technologies à maîtriser pour mener à bien le projet, ainsi que les outils avancés à connaître pour la mise en perspective.

---

## 1. Stack Obligatoire

| Technologie | Rôle dans le projet | Actions à réaliser | Points d’attention |
|-------------|--------------------|--------------------|--------------------|
| **Python 3.11+** | Langage principal | Implémenter tous les modules | Respect strict de flake8 ; utiliser les features 3.11 si utiles |
| **uv** | Gestion des dépendances / exécution | `uv sync`, `uv run python -m src` | Vérifier la présence de `llm_sdk` dans le dossier `src` |
| **numpy** | Manipulation de tenseurs | gérer `input_ids`, `logits` | Optimiser les conversions pour éviter les copies inutiles |
| **json** | Lecture/écriture des fichiers | Parser inputs, produire output | Gestion des erreurs (JSON invalide, types) |
| **pydantic** | Validation de données | Modèles pour inputs/outputs | Créer des messages d’erreur pédagogiques |
| **Small_LLM_Model** | Wrapper LLM imposé | `get_logits_from_input_ids`, `get_path_to_vocabulary_json` | Ne jamais utiliser de méthodes privées |
| **Makefile** | Automatisation | Règles install/run/debug/clean/lint | Tester chaque cible localement |

---

## 2. Modules à Implémenter (Rappel)

1. `input_handler.py` – lecture et validation des JSON.
2. `prompt_engineering.py` – construction des prompts few-shot.
3. `tokenizer.py` – conversions texte ↔ tokens ↔ input_ids via le vocabulaire.
4. `llm_interaction.py` – boucle de génération token-par-token (greedy).
5. `decoder.py` – input_ids → texte.
6. `parser.py` – extraction du JSON (fn_name, args) avec correction.
7. `validator.py` – modèles Pydantic + vérifications contre `function_definitions`.
8. `output_handler.py` – écriture du fichier `output/function_calling_name.json`.

---

## 3. Outils d’Apprentissage Recommandés (Phase 4)

| Thème | Ressources FR (à trouver) | Ressources EN (à trouver) | Format |
|-------|---------------------------|---------------------------|--------|
| Tokenisation & vocabulaire | Vidéo explicative BPE | Vidéo Hugging Face tokenization | YouTube |
| Prompt Engineering | Workshops 42 / talks FR | OpenAI / Anthropic prompt tips | Vidéo + article |
| Pydantic | Tutoriel rapide FR | Documentation officielle | Article + doc |
| uv + Makefile | Démo 42 FR | Blog post EN | Article |
| LLMs & logits | Conférence FR (IA School) | Andrej Karpathy playlists | YouTube |

Ces ressources seront sélectionnées et ajoutées dans `Formation/05_deroule_formation.md` pendant la Phase 4, avec liens et descriptions complètes.

---

## 4. Tests & Qualité

- **flake8** : linting obligatoire (`make lint`).
- **Tests internes** : scripts non notés mais recommandés pour chaque module.
- **Logs / monitoring** : prévoir un niveau de log minimal (info, warning, error).
- **Validation JSON** : utiliser des scripts simples pour s’assurer de la conformité (`python -m json.tool` ou équivalent).

---

## 5. Technologies Avancées (Hors Contraintes mais à connaître)

| Outil | Pourquoi il est interdit ici | Ce qu’il apporterait dans un contexte réel |
|-------|------------------------------|--------------------------------------------|
| **transformers (HF)** | Fournit des abstractions haut niveau (tokenizer, generate) contournant l’objectif pédagogique | Tokenisation automatique, génération push-button, support multi-modèles |
| **pytorch** | Base de nombreux LLMs modernes ; trop haut niveau pour l’exercice | Contrôle fin sur les tensors, possibilité de fine-tuning ou d’analyse interne |
| **dspy / langchain** | Frameworks de reasoning / orchestration | Outils de planning, agents, fonction calling prêt à l’emploi |
| **autres SDK LLM** | Simplifient l’accès aux modèles | Écosystème riche (OpenAI, Anthropic) pour prototyper rapidement |

**Objectif** : En Phase 7, comparer notre implémentation “from scratch” avec ce que permettent ces bibliothèques, afin de comprendre les compromis pédagogiques vs industriels.

---

## 6. Plan d’Approfondissement

1. **Court terme (Phase 5-6)** :
   - Mettre en place des scripts de test minimalistes.
   - Ajouter des hooks flake8/pre-commit si nécessaire.
2. **Moyen terme (Phase 7)** :
   - Reproduire la pipeline avec `transformers` pour comparer.
   - Tester l’usage d’API LLM externes pour valider la portabilité.
3. **Long terme** :
   - Étudier les frameworks d’agents (langchain, dspy) pour industrialiser le function calling.

---

*Document créé lors de la Phase 3 – Technologies*  
*Date : [À compléter]*

