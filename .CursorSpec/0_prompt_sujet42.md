# Prompt Initial - Projet 42

## Prompt Original

```
Aide moi a remplire le fishier @general.md 
ce fichier est destine atre lisible par moi et par toi tout au long du projet.

Le but est de centraliser les informations de base du projet :
Le but du projet :
C est un projet d apprentissage informatique de l ecole 42 angouleme.
Je dois apprendre et comprendre en realisant un projet un?des concepts.
Tu aura pour tache de comprendre le projet.
De penser a une conceptions pour le realiser.
De degager les concept et technologie que je dois connaitre pour realiser ce projet.
De preparer un deroule de cours pour que je puisse les apprendre.
Puis de passer a la realisation du projet. avec une doc technique bien decoupee sur les differents elements.
enfin de mettre en perspective ce projet avec les methodes actuelles pour savoir si cela est toujours d actualite et daller plus loin dans l apprentissage.
Dans @general.md tu va reformuler les prompt actuel en preambule.
puis tu vas realiser un document qui explique de maniere conceptuelle tout le deroulee du projet.
tu specifira des dossier et des fichier atteche a chacune des taches et des attendus :
exemple :
le sujets se trouve dans le dossier@Sujet 
le deroulee de la foramtion est le fichier ...

Bien sure ce document se remplira au fure et a mesure de l avancee de l avancee du projet avec les nouveaui fichier et autre liens.

Ce document ne contient pas de code.
Ce document est en francais (a lexception des therme techniaue liee au sujet)
Ce document doit etre lisible par moi et par toi car tu t y referera tout au long du projet.
```

---

## Version Optimisée et Générique

### Contexte

Je travaille sur un projet d'apprentissage de l'école 42 Angoulême. L'objectif est d'apprendre et de comprendre un concept informatique en le réalisant concrètement.

### Objectif Principal

Créer un fichier `general.md` (ou `.CursorSpec/general.md`) qui servira de document de référence centralisé tout au long du projet, lisible à la fois par moi et par l'assistant IA.

### Structure Attendue du Document `general.md`

Le document doit contenir :

1. **Préambule** : Reformulation de ce prompt initial avec les objectifs pédagogiques du projet

2. **Vue d'ensemble conceptuelle** : 
   - Description du projet et de son objectif pédagogique
   - Concepts principaux à apprendre
   - Contraintes techniques générales (si spécifiées dans le sujet)

3. **Déroulé conceptuel du projet** : Organisation en phases avec pour chacune :
   - **Objectif** : Ce que cette phase vise à accomplir
   - **Tâches** : Liste des actions à réaliser
   - **Fichiers/Dossiers** : Structure de fichiers associée avec indication des fichiers à créer
   - **Attendus** : Résultats attendus à la fin de la phase

4. **Phases suggérées** :
   - **Phase 1** : Compréhension et Analyse du sujet
   - **Phase 2** : Conception et Architecture de la solution
   - **Phase 3** : Identification des Concepts et Technologies à maîtriser
   - **Phase 4** : Préparation du Déroulé de Formation (cours structurés)
     - Inclure des liens vers des vidéos YouTube de formation en français et en anglais
     - Organiser les ressources par thème, langue et niveau
     - Pour chaque module, créer un dossier `Formation/Modules/MX_*/` contenant :
       - `[sujet]_0_info.md` : Fiche d'information du module (ex: `llm_tokenisation_0_info.md` pour M1)
       - `[sujet]_1_cours.md` : Cours détaillé en français avec explications approfondies, code, exemples, fiches synthétiques créées par l'assistant
       - `[sujet]_2_exercices.md` : Exercices progressifs avec étapes précises, templates, exemples de rendu
       - `[sujet]_3_corriges.md` : Solutions complètes des exercices, synchronisées avec les exercices
       - `templates/` : Fichiers modèles réutilisables (code, config, scripts) - **Doit être rempli pour chaque module**
       - `exemples/` : Exemples de sorties attendues, rendus - **Doit être rempli pour chaque module**
       - `tests/` : Scripts de test automatisés (Python, Bash) - **Doit être rempli pour chaque module**
     - Intégrer des ressources textuelles (articles, documentation) en français et anglais dans les cours
     - Rendre les cours précis et détaillés pour éviter les recherches supplémentaires
     - Assurer la synchronisation entre cours, exercices et corrigés
     - **Important** : Tous les dossiers templates/, exemples/ et tests/ doivent être remplis avec du contenu utile, pas seulement créés vides
   - **Phase 5** : Réalisation du Projet (implémentation)
   - **Phase 6** : Documentation Technique détaillée
  - **Phase 7** : Mise en Perspective (méthodes actuelles, approfondissement)
    - Comparer les contraintes pédagogiques avec les bibliothèques avancées (pytorch, transformers, etc.)
    - Discuter de la manière dont ces bibliothèques, bien que interdites pendant le projet, optimisent ce type de solution dans un contexte réel

5. **Structure du projet** : Organisation des dossiers et fichiers principaux

6. **Fichiers de référence** : Emplacements des fichiers importants (sujet, documentation, etc.)

7. **État d'avancement** : Suivi de la progression avec checkboxes

8. **Liens et ressources** : Section à compléter au fur et à mesure
   - L'assistant recherchera et ajoutera des liens vers des vidéos YouTube de formation
   - Les ressources seront organisées par thème, langue (français/anglais) et niveau
   - Chaque lien inclura : titre, URL, description, niveau recommandé, langue

9. **Prompt CONTINUE** : Section obligatoire pour reprendre le projet dans un nouveau chat
   - Cette section doit être ajoutée à la fin du document `general.md`
   - Elle doit contenir un prompt complet permettant de reprendre le projet si le contexte du chat est plein
   - Le prompt doit inclure :
     - Contexte du projet (objectif, contraintes techniques)
     - État d'avancement actuel (phases complétées/en cours)
     - Structure du projet (dossiers et fichiers importants)
     - Fichiers importants à consulter pour comprendre le contexte
     - Questions pour continuer (identifier l'état exact, fichiers créés, prochaines étapes)
     - Instructions pour l'assistant (lire general.md, identifier l'état, proposer la suite)
   - Format : Section markdown avec titre "Prompt CONTINUE - Reprendre le Projet dans un Nouveau Chat"
   - Le prompt doit être copiable tel quel dans un nouveau chat

### Contraintes du Document

- **Pas de code** : Le document est purement conceptuel et organisationnel
- **Langue** : Français (sauf termes techniques spécifiques)
- **Évolutif** : Le document sera complété et mis à jour tout au long du projet
- **Référence partagée** : L'assistant IA s'y référera systématiquement pour comprendre le contexte

### Exemple de Structure de Fichiers à Mentionner

Pour chaque phase, spécifier les fichiers associés avec le format :
```
- `Dossier/fichier.md` : Description du fichier (à créer)
- `Dossier/existant.md` : Description du fichier existant
```

### Instructions pour l'Assistant

1. Lire et analyser le sujet du projet (fichiers dans `Doc/Sujet/` ou équivalent)
2. Créer le document `general.md` avec la structure décrite ci-dessus
3. Adapter les phases selon la nature spécifique du projet
4. Utiliser ce document comme référence principale pour toutes les interactions futures
5. Mettre à jour le document au fur et à mesure de l'avancement
6. **OBLIGATOIRE** : Inclure dès la création initiale une section "Prompt CONTINUE" à la fin du document, et la mettre à jour régulièrement avec l'état d'avancement actuel du projet

### Notes Importantes

- Ce prompt est générique et réutilisable pour tout projet 42
- Les spécificités techniques du projet seront extraites du sujet fourni
- Le document `general.md` servira de base de connaissances partagée
- L'assistant doit se référer à ce document avant chaque nouvelle tâche
- Lors des phases de perspective/approfondissement, inclure une réflexion sur les bibliothèques non permises et leur valeur ajoutée hors contraintes
- Les modules de formation doivent rester synchronisés (cours/exercices/corrigés), avec ressources vidéo et textuelles référencées
- **OBLIGATOIRE** : Le document `general.md` doit toujours contenir une section "Prompt CONTINUE" à la fin pour permettre la reprise du projet dans un nouveau chat. Cette section doit être créée dès la création initiale du document et mise à jour régulièrement avec l'état d'avancement actuel

---

## Utilisation

Ce prompt peut être réutilisé pour n'importe quel projet 42 en :
1. Remplaçant les références spécifiques par des références génériques
2. Adaptant les phases selon la nature du projet
3. Conservant la structure générale et les objectifs pédagogiques

