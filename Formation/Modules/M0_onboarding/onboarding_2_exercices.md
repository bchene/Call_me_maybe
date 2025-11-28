# M0 – Exercices Détaillés : Onboarding & Environnement

## Instructions générales

- Chaque exercice doit être complété dans l'ordre
- Documenter vos résultats dans `Formation/Notes/log_onboarding.md`
- Utiliser les templates fournis dans `M0_onboarding/templates/`
- Comparer vos résultats avec les exemples dans `M0_onboarding/exemples/`

---

## Exercice 1 – Installation et vérification de uv

### Objectif
Installer uv et vérifier qu'il fonctionne correctement.

### Étapes détaillées

1. **Installation de uv**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Vérification de l'installation**
   ```bash
   uv --version
   ```
   
   **Résultat attendu** :
   ```
   uv 0.4.x (CPython 3.11.x)
   ```

3. **Test des commandes de base**
   ```bash
   uv --help
   uv pip --help
   ```

4. **Vérification du PATH**
   ```bash
   # macOS/Linux
   which uv
   
   # Windows
   where uv
   ```

### Livrable

Créer un fichier `Formation/Notes/exercice1_uv.md` avec :

```markdown
# Exercice 1 - Installation uv

## Date : [VOTRE_DATE]

## Version installée
uv 0.4.x (CPython 3.11.x)

## Commandes testées
- `uv --version` : ✓ OK
- `uv --help` : ✓ OK
- `uv pip --help` : ✓ OK

## Problèmes rencontrés
[Aucun / Description détaillée]

## Notes
[Vos observations]
```

### Vérification

Exécuter le script de test :
```bash
bash M0_onboarding/tests/test_uv_installed.sh
```

---

## Exercice 2 – Création et configuration de l'environnement

### Objectif
Créer le fichier `pyproject.toml` et synchroniser l'environnement.

### Étapes détaillées

1. **Créer le dossier Dev si nécessaire**
   ```bash
   mkdir -p Dev
   cd Dev
   ```

2. **Créer pyproject.toml**
   
   Utiliser le template : `M0_onboarding/templates/pyproject.toml.template`
   
   Copier et adapter :
   ```bash
   cp Formation/Modules/M0_onboarding/templates/pyproject.toml.template Dev/pyproject.toml
   ```

3. **Synchroniser l'environnement**
   ```bash
   cd Dev
   uv sync
   ```

4. **Vérifier l'installation**
   ```bash
   uv pip list
   uv run python -c "import numpy; import pydantic; print('✓ Packages OK')"
   ```

### Livrable

Créer `Formation/Notes/exercice2_env.md` avec :

```markdown
# Exercice 2 - Configuration environnement

## Date : [VOTRE_DATE]

## Packages installés
- numpy : [VERSION]
- pydantic : [VERSION]

## Commande uv sync
[Sortie complète de la commande]

## Tests d'import
[Sortie des tests]

## Problèmes rencontrés
[Aucun / Description]
```

### Vérification

```bash
uv run python scripts/check_env.py
```

Tous les checks doivent passer.

---

## Exercice 3 – Création du Makefile

### Objectif
Créer un Makefile complet avec toutes les cibles nécessaires.

### Étapes détaillées

1. **Créer le Makefile**
   
   Utiliser le template : `M0_onboarding/templates/Makefile.template`
   
   ```bash
   cp Formation/Modules/M0_onboarding/templates/Makefile.template Dev/Makefile
   ```

2. **Tester chaque cible**
   
   ```bash
   cd Dev
   
   # Test install
   make install
   echo $?  # Doit retourner 0
   
   # Test run (peut échouer si src/ n'existe pas encore)
   make run
   
   # Test lint
   make lint
   
   # Test clean
   make clean
   
   # Test doc
   make doc
   ```

3. **Ajouter la cible check-env**
   
   Ajouter dans le Makefile :
   ```make
   check-env:
   	@echo "Vérification de l'environnement..."
   	@uv run python scripts/check_env.py
   ```

4. **Tester la nouvelle cible**
   ```bash
   make check-env
   ```

### Livrable

Créer `Formation/Notes/exercice3_makefile.md` avec :

```markdown
# Exercice 3 - Makefile

## Date : [VOTRE_DATE]

## Cibles créées
- [x] install
- [x] run
- [x] debug
- [x] lint
- [x] clean
- [x] doc
- [x] check-env

## Tests effectués
| Cible | Résultat | Notes |
|-------|----------|-------|
| make install | ✓ | [Notes] |
| make run | ? | [Notes] |
| make lint | ✓ | [Notes] |
| make clean | ✓ | [Notes] |
| make doc | ✓ | [Notes] |
| make check-env | ✓ | [Notes] |

## Problèmes rencontrés
[Aucun / Description]
```

### Vérification

Exécuter tous les tests :
```bash
bash M0_onboarding/tests/test_makefile.sh
```

---

## Exercice 4 – Script de vérification de l'environnement

### Objectif
Créer un script Python qui vérifie automatiquement l'environnement.

### Étapes détaillées

1. **Créer le dossier scripts**
   ```bash
   mkdir -p scripts
   ```

2. **Créer le script**
   
   Utiliser le template : `M0_onboarding/templates/check_env.py.template`
   
   ```bash
   cp Formation/Modules/M0_onboarding/templates/check_env.py.template scripts/check_env.py
   chmod +x scripts/check_env.py
   ```

3. **Tester le script**
   ```bash
   uv run python scripts/check_env.py
   ```

4. **Intégrer au Makefile**
   
   Vérifier que la cible `check-env` utilise bien ce script.

### Livrable

Le script `scripts/check_env.py` doit :
- Vérifier la version de Python (3.11+)
- Vérifier que numpy et pydantic sont installés
- Vérifier la structure du projet
- Vérifier que le Makefile existe et contient les cibles essentielles
- Afficher un rapport clair avec ✓ et ✗

### Exemple de sortie attendue

```
==================================================
Vérification de l'environnement
==================================================

[Version Python]
✓ Python 3.11.8
✓ Version Python OK

[Packages]
✓ numpy installé
✓ pydantic installé

[Structure projet]
✓ Doc/ existe
✓ Formation/ existe
✓ Dev/ existe

[Makefile]
✓ Makefile existe
✓ Cible 'make install' trouvée
✓ Cible 'make run' trouvée
✓ Cible 'make lint' trouvée
✓ Cible 'make clean' trouvée

==================================================
✓ Tous les checks sont passés
```

### Vérification

```bash
# Test unitaire
uv run python -m pytest M0_onboarding/tests/test_check_env.py -v
```

---

## Exercice 5 – Documentation de l'arborescence

### Objectif
Comprendre et documenter la structure complète du projet.

### Étapes détaillées

1. **Générer l'arborescence**
   ```bash
   # Installer tree si nécessaire
   # macOS: brew install tree
   # Linux: sudo apt-get install tree
   
   tree -L 3 -I '__pycache__|*.pyc|.venv' > Formation/Notes/arborescence.txt
   ```

2. **Créer un document annoté**
   
   Créer `Formation/Notes/arborescence_annotee.md` :
   
   ```markdown
   # Arborescence du projet Call Me Maybe
   
   ## Structure principale
   
   ```
   [Coller ici l'arborescence générée]
   ```
   
   ## Description des dossiers
   
   ### .CursorSpec/
   **Rôle** : Documentation partagée avec l'assistant IA
   **Contenu** :
   - `general.md` : Document central du projet
   - `0_prompt_sujet42.md` : Template de prompt réutilisable
   
   ### Doc/
   **Rôle** : Documentation du projet
   **Contenu** :
   - `Sujet/` : Fichiers du sujet
   - `architecture.md` : Architecture du système
   - `design_decisions.md` : Décisions de conception
   
   ### Formation/
   **Rôle** : Matériel de formation
   **Contenu** :
   - `Modules/` : Modules d'apprentissage (M0, M1, M2, ...)
   - `01_analyse_sujet.md` : Analyse du sujet
   - `05_deroule_formation.md` : Plan de formation
   
   ### Dev/
   **Rôle** : Code source du projet
   **Contenu** :
   - `src/` : Code Python principal
   - `input/` : Fichiers d'entrée JSON
   - `output/` : Fichiers de sortie JSON
   - `Makefile` : Automatisation
   - `pyproject.toml` : Configuration uv
   
   ## Fichiers importants
   
   - `README.md` : Description générale
   - `.gitignore` : Fichiers ignorés par Git
   - `uv.lock` : Verrouillage des versions (généré automatiquement)
   ```

3. **Vérifier la compréhension**
   
   Répondre aux questions suivantes dans `Formation/Notes/comprehension_arborescence.md` :
   
   ```markdown
   # Compréhension de l'arborescence
   
   ## Questions
   
   1. Où se trouve le code source principal ?
   **Réponse** : Dev/src/
   
   2. Où sont les fichiers d'entrée du projet ?
   **Réponse** : Dev/input/
   
   3. Où est la documentation partagée avec l'IA ?
   **Réponse** : .CursorSpec/
   
   4. Où sont les modules de formation ?
   **Réponse** : Formation/Modules/
   
   5. Quel fichier contient la configuration des dépendances ?
   **Réponse** : Dev/pyproject.toml
   ```

### Livrable

- `Formation/Notes/arborescence.txt` : Arborescence générée
- `Formation/Notes/arborescence_annotee.md` : Document annoté
- `Formation/Notes/comprehension_arborescence.md` : Réponses aux questions

---

## Exercice 6 – Lecture de la documentation

### Objectif
Lire et comprendre les documents clés du projet.

### Étapes détaillées

1. **Lire le document général**
   ```bash
   # Ouvrir dans l'éditeur
   code .CursorSpec/general.md
   
   # Ou via make
   make doc
   ```

2. **Prendre des notes**
   
   Créer `Formation/Notes/lecture_general.md` :
   
   ```markdown
   # Lecture de general.md
   
   ## Date : [VOTRE_DATE]
   
   ## Points clés retenus
   
   ### Objectif du projet
   [Vos notes]
   
   ### Contraintes techniques
   - Python 3.11+
   - Packages autorisés : numpy, json, pydantic
   - Packages interdits : pytorch, transformers, huggingface, dspy
   
   ### Phases du projet
   1. Phase 1 : Compréhension et Analyse ✓
   2. Phase 2 : Conception et Architecture ✓
   3. Phase 3 : Identification des Concepts ✓
   4. Phase 4 : Préparation de la Formation ✓
   5. Phase 5 : Réalisation
   6. Phase 6 : Documentation Technique
   7. Phase 7 : Mise en Perspective
   
   ## Questions restantes
   [Vos questions]
   ```

3. **Lire le sujet**
   
   Lire `Doc/Sujet/Call_me_maybe_subject_fr.md` et créer `Formation/Notes/lecture_sujet.md` :
   
   ```markdown
   # Lecture du sujet
   
   ## Date : [VOTRE_DATE]
   
   ## Objectif principal
   [Vos notes]
   
   ## Contraintes importantes
   [Vos notes]
   
   ## Défis techniques identifiés
   [Vos notes]
   
   ## Questions
   [Vos questions]
   ```

### Livrable

- `Formation/Notes/lecture_general.md`
- `Formation/Notes/lecture_sujet.md`

---

## Exercice 7 – Configuration de Git (optionnel mais recommandé)

### Objectif
Configurer Git pour le projet.

### Étapes détaillées

1. **Initialiser le dépôt (si pas déjà fait)**
   ```bash
   git init
   ```

2. **Créer/verifier .gitignore**
   
   Utiliser le template : `M0_onboarding/templates/.gitignore.template`
   
   ```bash
   cp Formation/Modules/M0_onboarding/templates/.gitignore.template .gitignore
   ```

3. **Premier commit**
   ```bash
   git add .
   git commit -m "Initial commit: Setup environment and documentation"
   ```

### Livrable

Vérifier que `.gitignore` est correctement configuré et que les fichiers sensibles ne sont pas versionnés.

---

## Validation finale

### Checklist complète

Avant de passer au module suivant, vérifier :

- [ ] uv installé et fonctionnel (`uv --version`)
- [ ] Environnement créé (`uv sync` exécuté sans erreur)
- [ ] Packages installés (numpy, pydantic)
- [ ] Makefile créé avec toutes les cibles
- [ ] Script check_env.py créé et fonctionnel
- [ ] Arborescence documentée
- [ ] Documentation lue (general.md et sujet)
- [ ] Tous les exercices complétés
- [ ] Notes prises dans `Formation/Notes/`

### Test final

```bash
# Exécuter tous les checks
make check-env

# Tous les tests doivent passer
bash M0_onboarding/tests/test_all.sh
```

### Prochaine étape

Une fois tous les exercices complétés et validés, vous pouvez passer au **Module M1 - Fondamentaux LLM & Tokenisation**.

---

## Aide et support

Si vous rencontrez des problèmes :

1. Consulter la section "Résolution de problèmes" dans `onboarding_1_cours.md`
2. Vérifier les exemples dans `M0_onboarding/exemples/`
3. Comparer votre code avec les templates dans `M0_onboarding/templates/`
4. Exécuter les tests dans `M0_onboarding/tests/` pour diagnostiquer
