# Call Me Maybe - Document Général du Projet

## Préambule

Ce document centralise toutes les informations de base du projet **Call Me Maybe**. Il sert de référence tout au long du développement, à la fois pour l'étudiant et pour l'assistant IA.

### Contexte du Projet

**Call Me Maybe** est un projet d'apprentissage informatique de l'école 42 Angoulême. L'objectif est d'apprendre et de comprendre un concept fondamental de l'intelligence artificielle en le réalisant concrètement.

### Objectifs Pédagogiques

1. **Comprendre le projet** : Analyser le sujet et identifier les enjeux techniques
2. **Concevoir la solution** : Élaborer une architecture et une approche de résolution
3. **Identifier les concepts** : Déterminer les concepts et technologies à maîtriser
4. **Préparer la formation** : Créer un déroulé de cours structuré pour l'apprentissage
5. **Réaliser le projet** : Implémenter la solution avec une documentation technique découpée
6. **Mettre en perspective** : Analyser les méthodes actuelles et approfondir l'apprentissage

---

## Vue d'Ensemble du Projet

### Sujet Principal

**Les LLMs parlent-ils la langue des ordinateurs ?**

Le projet consiste à créer un système de **function calling** pour les LLMs (Large Language Models). Au lieu de répondre directement à une question, le système doit identifier quelle fonction appeler et avec quels arguments pour résoudre la requête.

**Exemple** : Pour la question "Quelle est la somme de 40 et 2 ?", le système ne doit pas retourner 42, mais identifier la fonction `fn_add_numbers` avec les arguments `a=40` et `b=2`.

### Contraintes Techniques

- **Langage** : Python 3.11 ou supérieur
- **Standards** : Code conforme à flake8
- **Validation** : Utilisation de pydantic pour toutes les classes
- **Packages autorisés** : numpy, json, pydantic
- **Packages interdits** : dspy, pytorch, huggingface, transformers, etc.
- **Modèle LLM** : Qwen/Qwen3-0.6B (par défaut)
- **Gestion d'erreurs** : Obligatoire, le programme ne doit jamais planter
- **Exécution** : `uv run python -m src`

### Défi Principal

Le système doit interagir avec un LLM au niveau des tokens pour qu'il comprenne et raisonne sur le function calling. Il est **interdit** d'inclure directement le JSON des définitions de fonctions dans le prompt. La solution doit utiliser le prompt engineering et les interactions au niveau des tokens.

---

## Structure du Projet

### Dossiers Principaux

```
Call_me_maybe/
├── Doc/                    # Documentation du projet
│   └── Sujet/              # Fichiers du sujet du projet
│       ├── Call_me_maybe_subject_fr.md
│       ├── Call_me_maybe_subject_en.md
│       └── Call_me_maybe_subject_en.pdf
├── Formation/              # Matériel de formation et cours
├── Dev/                    # Code source du projet
├── .CursorSpec/            # Spécifications pour l'assistant IA
│   └── general.md          # Ce fichier
└── README.md               # Description générale du projet
```

---

## Déroulé Conceptuel du Projet

### Phase 1 : Compréhension et Analyse

**Objectif** : Comprendre en profondeur le sujet et les enjeux techniques.

**Tâches** :
- Analyser le sujet complet (français et anglais)
- Identifier les concepts clés : function calling, LLMs, tokenisation, logits
- Comprendre le flux : Prompt → Tokens → Input_Ids → LLM → Logits → Next_Token
- Analyser les contraintes et limitations

**Fichiers/Dossiers** :
- `Doc/Sujet/Call_me_maybe_subject_fr.md` : Sujet en français
- `Doc/Sujet/Call_me_maybe_subject_en.md` : Sujet en anglais
- `Formation/01_analyse_sujet.md` : Notes d'analyse (à créer)

**Attendus** :
- Document d'analyse du sujet
- Identification des concepts techniques à maîtriser
- Liste des questions ouvertes

---

### Phase 2 : Conception et Architecture

**Objectif** : Concevoir l'architecture de la solution.

**Tâches** :
- Définir l'architecture générale du système
- Concevoir le système de prompt engineering
- Définir la stratégie d'interaction avec le LLM au niveau des tokens
- Concevoir le système de parsing et de validation des réponses
- Planifier la gestion des erreurs

**Fichiers/Dossiers** :
- `Formation/02_conception.md` : Document de conception (à créer)
- `Doc/architecture.md` : Schéma d'architecture (à créer)
- `Doc/design_decisions.md` : Décisions de conception (à créer)

**Attendus** :
- Architecture détaillée du système
- Schémas de flux de données
- Stratégie de prompt engineering
- Plan de gestion d'erreurs

---

### Phase 3 : Identification des Concepts et Technologies

**Objectif** : Lister et comprendre tous les concepts nécessaires.

**Concepts Identifiés** :
- **Function Calling** : Mécanisme permettant aux LLMs de sélectionner et appeler des fonctions
- **Tokenisation** : Conversion du texte en tokens puis en input_ids
- **Logits** : Probabilités brutes du modèle pour chaque token du vocabulaire
- **Prompt Engineering** : Art de construire des prompts efficaces
- **JSON Schema** : Validation des structures de données
- **Pydantic** : Validation de données en Python

**Fichiers/Dossiers** :
- `Formation/03_concepts.md` : Glossaire des concepts (à créer)
- `Formation/04_technologies.md` : Technologies utilisées (à créer)

**Attendus** :
- Glossaire complet des concepts
- Documentation des technologies
- Ressources d'apprentissage identifiées

---

### Phase 4 : Préparation du Déroulé de Formation

**Objectif** : Créer un parcours d'apprentissage structuré.

**Tâches** :
- Organiser les concepts par ordre d'apprentissage
- Créer des modules de cours progressifs
- Préparer des exercices pratiques
- Identifier les ressources externes (documentation, tutoriels)
- Rechercher et ajouter des liens vers des vidéos YouTube de formation en français et en anglais
- Organiser les ressources vidéos par thème, langue et niveau (débutant/intermédiaire/avancé)
- Pour chaque module, maintenir un dossier `Formation/Modules/MX_*` contenant fiche cours, exercices, corrigés, ressources textuelles FR/EN

**Fichiers/Dossiers** :
- `Formation/05_deroule_formation.md` : Plan de formation structuré
- `Formation/Modules/MX_*/` : Dossiers de modules (M0 à M6)
  - `[sujet]_0_info.md` : Fiche d'information du module (ex: `llm_tokenisation_0_info.md`)
  - `[sujet]_1_cours.md` : Cours détaillé avec explications approfondies
  - `[sujet]_2_exercices.md` : Exercices progressifs avec étapes précises
  - `[sujet]_3_corriges.md` : Solutions complètes des exercices
  - `templates/` : Fichiers modèles réutilisables (tous remplis)
  - `exemples/` : Exemples de sorties attendues (tous remplis)
  - `tests/` : Scripts de test automatisés (tous remplis)

**Attendus** :
- Plan de formation structuré
- Modules de cours progressifs
- Exercices pratiques
- Ressources d'apprentissage
- Liens vers vidéos YouTube organisés par thème, langue et niveau
- Chaque ressource vidéo avec : titre, URL, description, niveau, langue
- Structure complète par module :
  - Cours détaillé en français (`[sujet]_1_cours.md`)
  - Exercices progressifs avec étapes précises (`[sujet]_2_exercices.md`)
  - Corrigés complets (`[sujet]_3_corriges.md`)
  - Templates réutilisables (`templates/`) - **Tous remplis**
  - Exemples de rendu attendu (`exemples/`) - **Tous remplis**
  - Tests automatisés (`tests/`) - **Tous remplis**
  - Ressources textuelles FR/EN intégrées dans les cours

---

### Phase 5 : Réalisation du Projet

**Objectif** : Implémenter la solution complète.

**Tâches** :
- Mise en place de l'environnement (uv, dépendances)
- Implémentation des classes principales avec pydantic
- Développement du système de tokenisation
- Implémentation de l'interaction avec le LLM
- Développement du système de parsing des réponses
- Gestion des erreurs complète
- Création du Makefile
- Tests et validation

**Fichiers/Dossiers** :
- `Dev/src/` : Code source principal (à créer)
  - `main.py` : Point d'entrée
  - `llm_interaction.py` : Interaction avec le LLM
  - `tokenizer.py` : Gestion de la tokenisation
  - `function_caller.py` : Logique de function calling
  - `parser.py` : Parsing des réponses
  - `validator.py` : Validation avec pydantic
  - `utils.py` : Utilitaires
- `Dev/input/` : Fichiers d'entrée (à créer)
  - `function_calling_tests.json` : Tests de prompts
  - `function_definitions.json` : Définitions des fonctions
- `Dev/output/` : Fichiers de sortie (à créer)
  - `function_calling_name.json` : Résultats générés
- `Dev/Makefile` : Automatisation des tâches (à créer)
- `Dev/pyproject.toml` : Configuration uv (à créer)
- `Doc/technique/` : Documentation technique (à créer)
  - `architecture_detaillee.md`
  - `api_reference.md`
  - `guide_utilisation.md`

**Attendus** :
- Code fonctionnel et conforme aux standards
- Gestion d'erreurs complète
- Makefile opérationnel
- Documentation technique détaillée
- Tests de validation

---

### Phase 6 : Documentation Technique

**Objectif** : Documenter chaque élément du projet.

**Tâches** :
- Documenter l'architecture
- Documenter chaque module et classe
- Créer un guide d'utilisation
- Documenter les décisions techniques
- Créer des diagrammes de flux

**Fichiers/Dossiers** :
- `Doc/technique/architecture_detaillee.md` : Architecture complète
- `Doc/technique/api_reference.md` : Référence API
- `Doc/technique/guide_utilisation.md` : Guide d'utilisation
- `Doc/technique/decisions_techniques.md` : Décisions techniques
- `Doc/technique/diagrammes/` : Diagrammes (à créer)

**Attendus** :
- Documentation complète et structurée
- Diagrammes clairs
- Exemples d'utilisation
- Guide de maintenance

---

### Phase 7 : Mise en Perspective et Approfondissement

**Objectif** : Analyser les méthodes actuelles et approfondir l'apprentissage.

**Tâches** :
- Rechercher les méthodes actuelles de function calling
- Comparer avec les approches du projet
- Identifier les limites et améliorations possibles
- Explorer les techniques avancées
- Documenter les apprentissages
- Évaluer les bibliothèques avancées actuellement interdites (pytorch, transformers, etc.) et décrire comment elles optimisent ce type de solution hors contraintes pédagogiques

**Fichiers/Dossiers** :
- `Formation/06_perspectives.md` : Analyse des méthodes actuelles (à créer)
- `Formation/07_approfondissement.md` : Techniques avancées (à créer)
- `Doc/comparaison_methodes.md` : Comparaison des approches (à créer)

**Attendus** :
- Analyse comparative des méthodes
- Identification des tendances actuelles
- Proposition d'améliorations
- Plan d'approfondissement incluant une réflexion sur l'apport des bibliothèques non permises dans le cadre du projet

---

## Fichiers de Référence

### Sujet du Projet
- **Emplacement** : `Doc/Sujet/Call_me_maybe_subject_fr.md`
- **Description** : Sujet complet en français avec toutes les spécifications
- **Usage** : Référence principale pour les contraintes et exigences

### Sujet en Anglais
- **Emplacement** : `Doc/Sujet/Call_me_maybe_subject_en.md`
- **Description** : Sujet complet en anglais (version originale)
- **Usage** : Référence complémentaire pour clarifications

### Fichiers de Formation
- **Emplacement** : `Formation/01_analyse_sujet.md`
- **Description** : Analyse approfondie du sujet réalisée lors de la Phase 1
- **Contenu** : Concepts clés, flux de traitement, contraintes, défis techniques, questions ouvertes
- **Usage** : Référence pour comprendre les enjeux du projet et guider les phases suivantes

- **Emplacement** : `Formation/02_conception.md`
- **Description** : Conception détaillée du système réalisée lors de la Phase 2
- **Contenu** : Architecture modulaire, modules détaillés, stratégies de résolution, structure des fichiers
- **Usage** : Guide pour l'implémentation en Phase 5

- **Emplacement** : `Formation/03_concepts.md`
- **Description** : Synthèse des concepts à maîtriser (Phase 3)
- **Contenu** : Définitions, points clés, niveaux de priorité, tableau de suivi
- **Usage** : Base du plan de formation et des exercices

- **Emplacement** : `Formation/04_technologies.md`
- **Description** : Inventaire des technologies/outils (Phase 3)
- **Contenu** : Stack obligatoire, outils avancés, plan d’approfondissement
- **Usage** : Référence pour la mise en place technique et la perspective

- **Emplacement** : `Formation/05_deroule_formation.md`
- **Description** : Déroulé pédagogique complet (Phase 4)
- **Contenu** : Modules M0→M6, planning, ressources YouTube FR/EN, exercices
- **Usage** : Support principal pour suivre/appliquer la formation

- **Emplacement** : `Formation/Modules/MX_*/`
- **Description** : Modules enrichis (M0 à M6) avec structure complète
- **Contenu** : 
  - `[sujet]_0_info.md` : Fiche d'information du module (ex: `llm_tokenisation_0_info.md`, `prompts_0_info.md`)
  - `[sujet]_1_cours.md` : Cours détaillé avec explications approfondies, code, exemples
  - `[sujet]_2_exercices.md` : Exercices progressifs avec étapes précises
  - `[sujet]_3_corriges.md` : Solutions complètes des exercices
  - `templates/` : Fichiers modèles réutilisables - **Tous remplis pour M1-M6**
  - `exemples/` : Exemples de sorties attendues - **Tous remplis pour M1-M6**
  - `tests/` : Scripts de test automatisés - **Tous remplis pour M1-M6**
- **Usage** : Feuilles de route opérationnelles pour chaque séquence, avec cours détaillés, exercices précis et corrigés complets

### Fichiers d'Architecture
- **Emplacement** : `Doc/architecture.md`
- **Description** : Schémas d'architecture et diagrammes de flux
- **Contenu** : Architecture en couches, diagrammes de séquence, flux de données, structures de données
- **Usage** : Référence visuelle de l'architecture du système

- **Emplacement** : `Doc/design_decisions.md`
- **Description** : Décisions de conception avec justifications
- **Contenu** : 18 décisions clés documentées avec alternatives considérées
- **Usage** : Comprendre les choix techniques et leurs raisons

---

## État d'Avancement

### Phase Actuelle
- [x] Phase 1 : Compréhension et Analyse ✅
- [x] Phase 2 : Conception et Architecture ✅
- [x] Phase 3 : Identification des Concepts ✅
- [x] Phase 4 : Préparation de la Formation ✅
- [ ] Phase 5 : Réalisation
- [ ] Phase 6 : Documentation Technique
- [ ] Phase 7 : Mise en Perspective

### Notes d'Avancement

#### Phase 1 : Compréhension et Analyse ✅
- **Statut** : Complétée
- **Fichier créé** : `Formation/01_analyse_sujet.md`
- **Contenu** :
  - Analyse approfondie du sujet (français et anglais)
  - Identification des concepts clés : function calling, LLMs, tokenisation, logits, prompt engineering
  - Compréhension du flux complet : Prompt → Tokens → Input_Ids → LLM → Logits → Next_Token
  - Analyse détaillée des contraintes techniques
  - Identification des défis techniques principaux
  - Liste de questions ouvertes à résoudre
  - Éléments à approfondir pour la suite
- **Prochaine étape** : Phase 2 - Conception et Architecture

#### Phase 3 : Identification des Concepts ✅
- **Statut** : Complétée
- **Fichiers créés** :
  - `Formation/03_concepts.md` : Synthèse des concepts clés, priorités, besoins pédagogiques
  - `Formation/04_technologies.md` : Stack obligatoire, outils avancés et plan d’approfondissement
- **Contenu** :
  - Définition et points d’attention pour 10 concepts majeurs (function calling, LLM, tokenisation, etc.)
  - Tableau de suivi (priorité, niveau actuel, ressources nécessaires)
  - Inventaire des technologies obligatoires + bibliothèques avancées pour la perspective
  - Plan d’approfondissement court/moyen/long terme
- **Prochaine étape** : Phase 4 - Préparation du Déroulé de Formation

#### Phase 4 : Préparation du Déroulé de Formation ✅
- **Statut** : Complétée et enrichie
- **Fichiers créés** :
  - `Formation/05_deroule_formation.md` : Parcours détaillé (modules M0 → M6, planification, ressources)
  - `Formation/Modules/MX_*/` : Modules enrichis avec structure complète
- **Contenu** :
  - Organisation pédagogique (objectifs, durées, livrables, exercices)
  - Intégration de ressources YouTube FR/EN (ex. ScienceEtonnante, Andrej Karpathy, freeCodeCamp, Marketing Mania)
  - **Tous les modules (M0-M6) enrichis** avec :
    - `onboarding_1_cours.md` : Cours détaillés avec explications approfondies, code, exemples
    - `onboarding_2_exercices.md` : Exercices progressifs avec étapes précises, templates, exemples
    - `onboarding_3_corriges.md` : Solutions complètes de tous les exercices
    - `templates/` : Fichiers modèles réutilisables (code, config, scripts)
    - `exemples/` : Exemples de sorties attendues, rendus
    - `tests/` : Scripts de test automatisés (Python, Bash)
  - Ressources textuelles FR/EN intégrées dans chaque cours
- **Prochaine étape** : Phase 5 - Réalisation du Projet

#### Phase 2 : Conception et Architecture ✅
- **Statut** : Complétée
- **Fichiers créés** :
  - `Formation/02_conception.md` : Document de conception détaillé avec architecture modulaire
  - `Doc/architecture.md` : Schémas d'architecture et diagrammes de flux
  - `Doc/design_decisions.md` : Décisions de conception avec justifications
- **Contenu** :
  - Architecture modulaire avec 8 modules principaux
  - Flux de données détaillé pour chaque étape
  - Stratégies de résolution des défis techniques
  - Structure des fichiers et organisation du code
  - Décisions de conception documentées avec alternatives
- **Prochaine étape** : Phase 3 - Identification des Concepts et Technologies

---

## Liens et Ressources

### Ressources Externes
_(À compléter avec les ressources identifiées au cours du projet)_

### Références Techniques
_(À compléter avec les documentations techniques utilisées)_

---

## Notes Importantes

- Ce document est vivant et sera mis à jour régulièrement
- Tous les fichiers mentionnés seront créés au fur et à mesure
- Les chemins et structures peuvent évoluer selon les besoins
- La documentation doit rester claire et accessible
- **Pour reprendre le projet dans un nouveau chat** : Consultez la section **"Prompt CONTINUE"** ci-dessous

---

## Prompt CONTINUE - Reprendre le Projet dans un Nouveau Chat

Si le contexte du chat est plein ou si vous devez reprendre le projet dans un nouveau chat, utilisez ce prompt :

```
Je reprends le projet Call Me Maybe (42 Angoulême) dans un nouveau chat.

CONTEXTE DU PROJET :
- Projet d'apprentissage sur le function calling avec LLMs
- Objectif : Créer un système qui convertit des questions en appels de fonctions structurés
- Langage : Python 3.11+, packages autorisés : numpy, pydantic
- Modèle LLM : Qwen/Qwen3-0.6B via Small_LLM_Model

ÉTAT D'AVANCEMENT :
- Phase 1 : ✅ Compréhension et Analyse (complétée)
- Phase 2 : ✅ Conception et Architecture (complétée)
- Phase 3 : ✅ Identification des Concepts (complétée)
- Phase 4 : ✅ Préparation de la Formation (complétée, tous les modules M0-M6 enrichis)
- Phase 5 : ⏳ Réalisation du Projet (en cours / à faire)
- Phase 6 : ⏳ Documentation Technique (à faire)
- Phase 7 : ⏳ Mise en Perspective (à faire)

STRUCTURE DU PROJET :
- Documentation centrale : `.CursorSpec/general.md` (ce fichier contient TOUT le contexte)
- Sujet : `Doc/Sujet/Call_me_maybe_subject_fr.md`
- Formation : `Formation/Modules/MX_*/` (M0 à M6, tous enrichis avec cours/exercices/corrigés)
- Code source : `Dev/src/` (à créer/implémenter)
- Input/Output : `Dev/input/` et `Dev/output/`

FICHIERS IMPORTANTS À CONSULTER :
1. `.CursorSpec/general.md` : Document central avec tout le contexte
2. `Formation/01_analyse_sujet.md` : Analyse approfondie du sujet
3. `Formation/02_conception.md` : Architecture et conception
4. `Doc/architecture.md` : Schémas d'architecture
5. `Doc/design_decisions.md` : Décisions de conception
6. `Formation/Modules/MX_*/` : Modules de formation (cours/exercices/corrigés)

QUESTIONS POUR CONTINUER :
1. Quelle est la phase actuelle du projet ?
2. Quels sont les fichiers de code déjà créés dans `Dev/src/` ?
3. Quels sont les tests déjà implémentés ?
4. Y a-t-il des erreurs ou problèmes à résoudre ?
5. Quelle est la prochaine étape à réaliser ?

INSTRUCTIONS :
- Lire d'abord `.CursorSpec/general.md` pour comprendre le contexte complet
- Identifier l'état d'avancement exact du projet
- Proposer la suite logique du travail
- Utiliser les modules de formation comme référence pour l'implémentation
```

---

*Dernière mise à jour : Date de création*
*Version : 1.0*

