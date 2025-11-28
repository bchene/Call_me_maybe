# Phase 3 - Concepts à Maîtriser

Ce document recense les concepts théoriques indispensables pour réussir le projet **Call Me Maybe**. Chaque section précise la définition, les points d’attention, les ressources ciblées (à compléter lors de la Phase 4) et le niveau de maîtrise attendu.

---

## 1. Function Calling avec les LLMs
- **Définition** : Mécanisme permettant à un LLM de choisir une fonction pré-définie et de générer les arguments nécessaires au lieu de répondre directement en texte libre.
- **Points clés** :
  - Compréhension de l’intention utilisateur.
  - Mapping prompt → fonction → arguments.
  - Importance du format de sortie strict (JSON).
- **Ressources** : cours internes à produire + vidéos (Phase 4).
- **Maîtrise attendue** : être capable d’expliquer le processus complet et de diagnostiquer un mauvais choix de fonction.

## 2. Architecture Transformer / LLMs
- **Définition** : Modèles basés sur l’attention, générant un token à la fois.
- **Points clés** :
  - Notion de logits, softmax, sélection de tokens.
  - Rôle des embeddings, couches attention, feed-forward.
  - Compréhension de Qwen/Qwen3-0.6B à haut niveau.
- **Maîtrise attendue** : savoir décrire le pipeline Prompt → Tokens → Logits → Token suivant, et identifier où intervenir dans le projet.

## 3. Tokenisation et Vocabulaire
- **Définition** : Conversion du texte en unités (tokens) puis en identifiants numériques (input_ids) via un vocabulaire.
- **Points clés** :
  - Manipulation du fichier vocabulaire JSON.
  - Gestion des tokens inconnus / spéciaux.
  - Respect de l’ordre des tokens lors de la génération.
- **Maîtrise attendue** : implémenter une tokenisation/décodage fiables et diagnostiquer les erreurs liées aux tokens.

## 4. Logits et Stratégies de Décodage
- **Définition** : Les logits sont les scores bruts produits par le modèle pour chaque token possible.
- **Points clés** :
  - Sélection greedy vs sampling.
  - Gestion des critères d’arrêt (EOS, longueur maximale, JSON complet).
  - Interprétation des logits pour comprendre les erreurs de génération.
- **Maîtrise attendue** : savoir analyser une séquence de logits et ajuster la stratégie de décodage.

## 5. Prompt Engineering
- **Définition** : Conception de prompts guidant le modèle vers le comportement souhaité.
- **Points clés** :
  - Utilisation d’exemples structurés (few-shot).
  - Indication explicite du format JSON attendu.
  - Limitation : interdiction d’inclure le JSON complet des fonctions.
- **Maîtrise attendue** : être capable de concevoir, tester et ajuster des prompts pour améliorer la précision.

## 6. JSON Schema & Validation
- **Définition** : Ensemble de règles garantissant qu’un JSON respecte une structure imposée.
- **Points clés** :
  - Validation avec Pydantic (obligatoire dans le sujet).
  - Conversion de types (string → float, etc.).
  - Gestion des erreurs utilisateurs/LLM (clés manquantes, types invalides).
- **Maîtrise attendue** : créer des modèles Pydantic robustes et interpréter les messages d’erreur.

## 7. Gestion d’Erreurs et Résilience
- **Définition** : Techniques pour éviter les crashs et fournir des messages clairs.
- **Points clés** :
  - Try/except systématiques.
  - Log des erreurs + poursuite de l’exécution.
  - Correction automatique des JSON partiellement valides.
- **Maîtrise attendue** : concevoir un pipeline qui continue malgré les erreurs de certains prompts.

## 8. Structure JSON du Projet
- **Définition** : Format attendu pour les fichiers d’entrée/sortie.
- **Points clés** :
  - `function_calling_tests.json` : liste de prompts.
  - `function_definitions.json` : dictionnaire de fonctions.
  - `output/function_calling_name.json` : tableau de résultats strictement formaté.
- **Maîtrise attendue** : manipuler ces fichiers sans casser leur structure et détecter les incohérences.

## 9. Gestion de l’Environnement Python (uv)
- **Définition** : Utilisation de `uv` pour gérer l’environnement virtuel et les dépendances.
- **Points clés** :
  - Création/synchronisation (`uv sync`).
  - Exécution standard (`uv run python -m src`).
  - Isolation des dépendances.
- **Maîtrise attendue** : être autonome pour installer, lancer et dépanner l’environnement.

## 10. Bibliothèques Avancées (Perspective)
- **Contexte** : `transformers`, `pytorch`, `huggingface`, `dspy`, etc. sont interdits pendant le projet.
- **Objectif d’apprentissage** :
  - Comprendre pourquoi le projet impose des interactions bas niveau.
  - Savoir comment ces bibliothèques faciliteraient certaines étapes (tokenisation, génération, gestion des logits) dans un contexte réel.
- **Maîtrise attendue** : être capable de comparer l’approche contrainte (bas niveau) avec les stacks modernes et d’expliquer ce que l’on gagnerait/perdrait.

---

## Table de Suivi des Concepts

| Concept | Priorité | Niveau actuel | Besoins identifiés | Ressources prévues (Phase 4) |
|---------|----------|---------------|--------------------|------------------------------|
| Function Calling | Haute | À clarifier | Exemples concrets supplémentaires | Cours interne + vidéos FR/EN |
| Architecture LLM | Haute | Notions de base | Approfondir logits/attention | Vidéos LLM Fundamentals |
| Tokenisation | Haute | À pratiquer | Manipulation du vocabulaire | Atelier + notebook démo |
| Prompt Engineering | Haute | À expérimenter | Créer une librairie d’exemples | Série d’exercices guidés |
| Validation Pydantic | Moyenne | Base solide à acquérir | Cas d’erreurs réels | Documentation + exercices |
| Gestion d’erreurs | Moyenne | À structurer | Stratégies de retry/skip | Études de cas |
| Environnement uv | Basse | Basique | Scripts Makefile + uv | Tutoriel rapide |
| Bibliothèques avancées | Perspective | Observation | Benchmark hors contraintes | Veille technique |

---

*Document créé lors de la Phase 3 – Concepts*  
*Date : [À compléter]*

