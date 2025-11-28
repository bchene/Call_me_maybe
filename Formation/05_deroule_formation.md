# Phase 4 – Déroulé de Formation

Ce document structure l’apprentissage en modules progressifs. Chaque module possède :
- des objectifs pédagogiques,
- une durée indicative,
- les supports associés (dossiers `Formation/Modules/`),
- des ressources vidéo YouTube FR/EN,
- des exercices pratiques et des livrables.

---

## Vue d’ensemble

| Module | Thème | Durée | Livrable principal |
|--------|-------|-------|--------------------|
| M0 | Onboarding & environnement | 0.5 j | Environnement uv + Makefile opérationnel |
| M1 | Fondamentaux LLM & tokenisation | 1.5 j | Carte mentale des concepts + notebook tokenisation |
| M2 | Function calling & prompt engineering | 2 j | Bibliothèque de prompts + protocole de tests |
| M3 | Validation JSON & Pydantic | 1 j | Modèles Pydantic + plan de tests |
| M4 | Interaction LLM (pipeline complet) | 2 j | Prototype de boucle génération/validation |
| M5 | Robustesse, logs & QA | 1 j | Grille d’erreurs + scripts de vérification |
| M6 | Perspectives & outils avancés | 0.5 j | Note comparative (libs interdites vs implémentation maison) |

Durée totale indicative : **8 jours** (peut être étalée selon disponibilité).

---

## Module M0 – Onboarding & Environnement
- **Support** : `Formation/Modules/module_00_onboarding.md`
- **Objectifs** :
  - Installer uv, configurer le repo, vérifier `Makefile`.
  - Prendre connaissance du dossier `Doc/Sujet/`.
- **Ressources** :
  - FR : `Science des Données – Installer uv et Poetry` *(à compléter avec tutoriel interne)*.
  - EN : [Python Environment Management with uv (Astral)](https://www.youtube.com/watch?v=J5neYBfJtOU) *(overview rapide, 12 min)*.
- **Exercices** :
  - Créer l’environnement, lancer `uv run python -m src` (mock).
  - Ajouter une commande personnalisée `make doc`.

---

## Module M1 – Fondamentaux LLM & Tokenisation
- **Support** : `Formation/Modules/module_01_llms_basics.md`
- **Objectifs** :
  - Comprendre la chaîne Prompt → Tokens → Logits → Token suivant.
  - Manipuler le vocabulaire JSON fourni.
- **Ressources** :
  - FR : [ScienceEtonnante – « GPT-3 : comment ça marche ? »](https://www.youtube.com/watch?v=R5b4wIYNojQ).
  - EN :
    - [Andrej Karpathy – « Let’s build GPT: from scratch »](https://www.youtube.com/watch?v=wjZofJX0v4M).
    - [Andrej Karpathy – « Byte Pair Encoding (BPE) »](https://www.youtube.com/watch?v=zduSFxRajkE).
- **Exercices** :
  - Reconstituer manuellement la tokenisation d’une phrase courte.
  - Écrire un mini-script qui charge le vocabulaire et convertit une phrase en `input_ids`.

---

## Module M2 – Function Calling & Prompt Engineering
- **Support** : `Formation/Modules/module_02_function_calling.md`
- **Objectifs** :
  - Construire des prompts few-shot respectant les contraintes du sujet.
  - Définir une bibliothèque de gabarits (questions math, string, datetime, etc.).
- **Ressources** :
  - FR : [Marketing Mania – « J’ai testé 100 prompts ChatGPT (voici les meilleurs) »](https://www.youtube.com/watch?v=9Zcj6n_0uS8).
  - EN : [freeCodeCamp – « Prompt Engineering Full Course (Learn Prompting) »](https://www.youtube.com/watch?v=dOxUroR57xs).
- **Exercices** :
  - Créer 5 prompts few-shot couvrant des cas variés.
  - Tester les prompts sur un LLM accessible (ex. ChatGPT) et consigner les résultats.

---

## Module M3 – Validation JSON & Pydantic
- **Support** : `Formation/Modules/module_03_validation.md`
- **Objectifs** :
  - Modéliser `function_definitions` et `function_calling_tests` avec Pydantic.
  - Écrire un validateur strict pour la sortie finale.
- **Ressources** :
  - FR : `À compléter` *(prévoir une capsule interne courte sur Pydantic)*.
  - EN : [ArjanCodes – « Data validation in Python with Pydantic »](https://www.youtube.com/watch?v=Vj-iWWuQj7E).
- **Exercices** :
  - Implémenter `models.py` avec Pydantic.
  - Simuler des erreurs (type incorrect, clé manquante) et analyser les messages.

---

## Module M4 – Interaction LLM & Pipeline Complet
- **Support** : `Formation/Modules/module_04_pipeline.md`
- **Objectifs** :
  - Implémenter la boucle token-par-token (greedy) avec `Small_LLM_Model`.
  - Brancher tokenisation → logits → décodage → parsing → validation.
- **Ressources** :
  - EN : [Corey Schafer – « Python Logging Tutorial »](https://www.youtube.com/watch?v=-ARI4Cz-awo) pour la supervision.
  - EN (bonus) : [James Briggs – « LangChain Crash Course »](https://www.youtube.com/watch?v=aywZrzNaKjs) pour comparer avec les frameworks avancés.
- **Exercices** :
  - Ecrire une fonction `generate_response(prompt_ids)` retournant la séquence générée.
  - Mettre en place un log des logits max/token choisi.

---

## Module M5 – Robustesse, QA & Tests
- **Support** : `Formation/Modules/module_05_quality.md`
- **Objectifs** :
  - Formaliser la stratégie de gestion d’erreurs (skip, retry, fallback).
  - Construire une batterie de tests fonctionnels + linters.
- **Ressources** :
  - EN : [TestDriven – « Python Exception Handling Best Practices »](https://www.youtube.com/watch?v=nlCKrKGHSSk).
  - FR : `Capsule interne « Gestion d’erreurs Python » (à produire)` – recap try/except/logging.
- **Exercices** :
  - Créer un tableau des erreurs possibles + action associée.
  - Écrire un script de test qui injecte un JSON invalide volontaire.

---

## Module M6 – Perspectives & Bibliothèques Avancées
- **Support** : `Formation/Modules/module_06_perspectives.md`
- **Objectifs** :
  - Comparer l’implémentation contrainte avec les libs interdites (transformers, langchain, dspy…).
  - Proposer un plan d’évolution post-projet.
- **Ressources** :
  - EN : [James Briggs – « LangChain Crash Course »](https://www.youtube.com/watch?v=aywZrzNaKjs) (re-rappel).
  - EN : [Harrison Chase – « LangChain Agents & Tools »](https://www.youtube.com/watch?v=_wY6uFYyP0w).
  - FR : `Live Mistral/IA Pau – retour d’expérience function calling` *(à identifier si session disponible)*.
- **Livrable** :
  - Note de synthèse listant : avantages/inconvénients de chaque lib, quand l’utiliser, comment migrer.

---

## Planification hebdomadaire suggérée

| Jour | Matin | Après-midi |
|------|-------|-----------|
| J1 | M0 + début M1 | fin M1 (exercices tokenisation) |
| J2 | M2 (theory + prompts FR/EN) | M2 (tests + revue) |
| J3 | M3 (pydantic) | Début M4 |
| J4 | M4 (LLM interaction) | M4 (boucle complète) |
| J5 | M5 (robustesse/tests) | Buffer mise à niveau |
| J6 (optionnel) | M6 + mise en perspective | Préparation doc Phase 5 |

---

## Ressources globales (rappel)

| Sujet | FR | EN |
|-------|----|----|
| LLM & tokenisation | ScienceEtonnante – [GPT-3 : comment ça marche ?](https://www.youtube.com/watch?v=R5b4wIYNojQ) | Karpathy – [Let’s build GPT](https://www.youtube.com/watch?v=wjZofJX0v4M) / [BPE](https://www.youtube.com/watch?v=zduSFxRajkE) |
| Prompt engineering | Marketing Mania – [J’ai testé 100 prompts ChatGPT](https://www.youtube.com/watch?v=9Zcj6n_0uS8) | freeCodeCamp – [Prompt Engineering Full Course](https://www.youtube.com/watch?v=dOxUroR57xs) |
| Validation & JSON | Capsule interne Pydantic (à produire) | ArjanCodes – [Pydantic](https://www.youtube.com/watch?v=Vj-iWWuQj7E) |
| Logs & erreurs | Capsule interne (Python try/except) | Corey Schafer – [Logging](https://www.youtube.com/watch?v=-ARI4Cz-awo) |
| Bibliothèques avancées | (à identifier : live FR autour de LangChain/Mistral) | James Briggs – [LangChain Crash Course](https://www.youtube.com/watch?v=aywZrzNaKjs) |

---

*Document créé lors de la Phase 4 – Déroulé de formation*  
*Date : [À compléter]*

