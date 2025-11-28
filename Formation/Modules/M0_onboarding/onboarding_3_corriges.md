# M0 – Corrigés Complets : Onboarding & Environnement

## Exercice 1 – Installation et vérification de uv

### Solution

**1. Installation de uv**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**2. Vérification**

```bash
$ uv --version
uv 0.4.25 (CPython 3.11.8)
```

**3. Test des commandes**

```bash
$ uv --help
# Affiche l'aide complète

$ uv pip --help
# Affiche l'aide pour pip
```

**4. Vérification du PATH**

```bash
# macOS/Linux
$ which uv
/Users/votre_user/.cargo/bin/uv

# Windows
$ where uv
C:\Users\votre_user\.cargo\bin\uv.exe
```

### Livrable attendu

Fichier `Formation/Notes/exercice1_uv.md` :

```markdown
# Exercice 1 - Installation uv

## Date : 2024-01-15

## Version installée
uv 0.4.25 (CPython 3.11.8)

## Commandes testées
- `uv --version` : ✓ OK
- `uv --help` : ✓ OK
- `uv pip --help` : ✓ OK

## Problèmes rencontrés
Aucun

## Notes
Installation réussie, uv accessible dans le PATH.
```

---

## Exercice 2 – Création et configuration de l'environnement

### Solution

**1. Création de pyproject.toml**

Fichier `Dev/pyproject.toml` :

```toml
[project]
name = "call-me-maybe"
version = "0.1.0"
description = "Function calling tool for LLMs - 42 Angoulême"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "numpy>=1.24.0",
    "pydantic>=2.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.flake8]
max-line-length = 100
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "build",
    "dist",
]
```

**2. Synchronisation**

```bash
$ cd Dev
$ uv sync
Resolving dependencies...
Downloading packages...
Installing packages...
Successfully installed numpy-1.26.0 pydantic-2.5.0
```

**3. Vérification**

```bash
$ uv pip list
Package    Version
---------- -------
numpy      1.26.0
pydantic   2.5.0

$ uv run python -c "import numpy; import pydantic; print('✓ Packages OK')"
✓ Packages OK
```

### Livrable attendu

Fichier `Formation/Notes/exercice2_env.md` :

```markdown
# Exercice 2 - Configuration environnement

## Date : 2024-01-15

## Packages installés
- numpy : 1.26.0
- pydantic : 2.5.0

## Commande uv sync
[Sortie complète de la commande]

## Tests d'import
✓ Packages OK

## Problèmes rencontrés
Aucun
```

---

## Exercice 3 – Création du Makefile

### Solution

**Makefile complet** (`Dev/Makefile`) :

```make
.PHONY: install run debug lint clean doc check-env help

# Installation des dépendances
install:
	@echo "Installation des dépendances..."
	uv sync

# Exécution du programme principal
run:
	@echo "Exécution du programme..."
	uv run python -m src

# Mode debug avec pdb
debug:
	@echo "Lancement en mode debug..."
	uv run python -m pdb -m src

# Vérification du code avec flake8
lint:
	@echo "Vérification du code..."
	@if [ -d "src" ]; then \
		uv run flake8 src --max-line-length=100; \
	else \
		echo "Aucun code à vérifier (src/ n'existe pas encore)"; \
	fi

# Nettoyage des fichiers temporaires
clean:
	@echo "Nettoyage..."
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@echo "Nettoyage terminé"

# Ouverture de la documentation
doc:
	@echo "Ouverture de la documentation..."
	@if command -v open > /dev/null; then \
		open ../Doc/Sujet/Call_me_maybe_subject_fr.md; \
	elif command -v xdg-open > /dev/null; then \
		xdg-open ../Doc/Sujet/Call_me_maybe_subject_fr.md; \
	else \
		echo "Ouvrez manuellement: Doc/Sujet/Call_me_maybe_subject_fr.md"; \
	fi

# Vérification de l'environnement
check-env:
	@echo "Vérification de l'environnement..."
	@if [ -f "../scripts/check_env.py" ]; then \
		uv run python ../scripts/check_env.py; \
	else \
		echo "Script check_env.py non trouvé"; \
	fi

# Aide
help:
	@echo "Cibles disponibles:"
	@echo "  make install    - Installer les dépendances"
	@echo "  make run        - Exécuter le programme"
	@echo "  make debug      - Lancer en mode debug"
	@echo "  make lint       - Vérifier le code avec flake8"
	@echo "  make clean      - Nettoyer les fichiers temporaires"
	@echo "  make doc        - Ouvrir la documentation"
	@echo "  make check-env  - Vérifier l'environnement"
	@echo "  make help       - Afficher cette aide"
```

**Tests des cibles** :

```bash
$ make install
Installation des dépendances...
uv sync
✓ Succès

$ make run
Exécution du programme...
uv run python -m src
ModuleNotFoundError: No module named 'src'
# Normal tant que src/ n'existe pas

$ make lint
Vérification du code...
Aucun code à vérifier (src/ n'existe pas encore)

$ make clean
Nettoyage...
Nettoyage terminé

$ make doc
Ouverture de la documentation...
# Ouvre le fichier dans l'éditeur par défaut

$ make check-env
Vérification de l'environnement...
[Sortie du script check_env.py]
```

### Livrable attendu

Fichier `Formation/Notes/exercice3_makefile.md` :

```markdown
# Exercice 3 - Makefile

## Date : 2024-01-15

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
| make install | ✓ | Installation réussie |
| make run | ⚠ | Erreur normale (src/ n'existe pas) |
| make lint | ✓ | Pas de code à vérifier |
| make clean | ✓ | Nettoyage OK |
| make doc | ✓ | Documentation ouverte |
| make check-env | ✓ | Tous les checks passés |

## Problèmes rencontrés
Aucun
```

---

## Exercice 4 – Script de vérification de l'environnement

### Solution

**Script complet** (`scripts/check_env.py`) :

```python
#!/usr/bin/env python3
"""Script de vérification de l'environnement de développement."""

import sys
import platform
from pathlib import Path


def check_python_version():
    """Vérifie que Python 3.11+ est utilisé."""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("✗ Python 3.11+ requis")
        return False
    print("✓ Version Python OK")
    return True


def check_packages():
    """Vérifie que les packages requis sont installés."""
    required = ['numpy', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installé")
        except ImportError:
            print(f"✗ {package} manquant")
            missing.append(package)
    
    return len(missing) == 0


def check_project_structure():
    """Vérifie la structure du projet."""
    required_dirs = ['Doc', 'Formation', 'Dev']
    
    base = Path(__file__).parent.parent
    missing = []
    
    for dir_name in required_dirs:
        dir_path = base / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ existe")
        else:
            print(f"✗ {dir_name}/ manquant")
            missing.append(dir_name)
    
    return len(missing) == 0


def check_makefile():
    """Vérifie que le Makefile existe et contient les cibles essentielles."""
    base = Path(__file__).parent.parent
    makefile = base / 'Dev' / 'Makefile'
    
    if not makefile.exists():
        print("✗ Makefile manquant")
        return False
    
    print("✓ Makefile existe")
    
    content = makefile.read_text()
    targets = ['install', 'run', 'lint', 'clean']
    missing = []
    
    for target in targets:
        if f'\n{target}:' in content or f'\n\t{target}:' in content:
            print(f"✓ Cible 'make {target}' trouvée")
        else:
            print(f"✗ Cible 'make {target}' manquante")
            missing.append(target)
    
    return len(missing) == 0


def main():
    """Fonction principale."""
    print("=" * 50)
    print("Vérification de l'environnement")
    print("=" * 50)
    print()
    
    checks = [
        ("Version Python", check_python_version),
        ("Packages", check_packages),
        ("Structure projet", check_project_structure),
        ("Makefile", check_makefile),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        results.append(check_func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ Tous les checks sont passés")
        sys.exit(0)
    else:
        print("✗ Certains checks ont échoué")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

**Sortie attendue** :

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

---

## Exercice 5 – Documentation de l'arborescence

### Solution

**1. Génération de l'arborescence**

```bash
$ tree -L 3 -I '__pycache__|*.pyc|.venv' > Formation/Notes/arborescence.txt
```

**2. Document annoté** (`Formation/Notes/arborescence_annotee.md`) :

```markdown
# Arborescence du projet Call Me Maybe

## Structure principale

```
Call_me_maybe/
├── .CursorSpec/              # Documentation partagée avec l'IA
│   ├── general.md            # Document central du projet
│   └── 0_prompt_sujet42.md   # Template de prompt réutilisable
├── Doc/                      # Documentation du projet
│   ├── Sujet/                # Fichiers du sujet
│   │   ├── Call_me_maybe_subject_fr.md
│   │   └── Call_me_maybe_subject_en.md
│   ├── architecture.md       # Architecture du système
│   └── design_decisions.md   # Décisions de conception
├── Formation/                # Matériel de formation
│   ├── Modules/              # Modules d'apprentissage
│   │   ├── M0_onboarding/
│   │   ├── M1_llm_tokenisation/
│   │   └── ...
│   ├── 01_analyse_sujet.md
│   └── 05_deroule_formation.md
├── Dev/                      # Code source du projet
│   ├── src/                  # Code Python principal (à créer)
│   ├── input/                # Fichiers d'entrée JSON (à créer)
│   ├── output/               # Fichiers de sortie JSON (à créer)
│   ├── Makefile              # Automatisation
│   └── pyproject.toml        # Configuration uv
├── scripts/                  # Scripts utilitaires
│   └── check_env.py          # Vérification environnement
├── .gitignore               # Fichiers ignorés par Git
└── README.md                # Description générale du projet
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

**3. Réponses aux questions** (`Formation/Notes/comprehension_arborescence.md`) :

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

---

## Exercice 6 – Lecture de la documentation

### Solution

**1. Notes sur general.md** (`Formation/Notes/lecture_general.md`) :

```markdown
# Lecture de general.md

## Date : 2024-01-15

## Points clés retenus

### Objectif du projet
Créer un système de function calling pour LLMs qui convertit des questions en appels de fonctions structurés.

### Contraintes techniques
- Python 3.11+
- Packages autorisés : numpy, json, pydantic
- Packages interdits : pytorch, transformers, huggingface, dspy
- Modèle : Qwen/Qwen3-0.6B
- Gestion d'erreurs obligatoire

### Phases du projet
1. Phase 1 : Compréhension et Analyse ✓
2. Phase 2 : Conception et Architecture ✓
3. Phase 3 : Identification des Concepts ✓
4. Phase 4 : Préparation de la Formation ✓
5. Phase 5 : Réalisation
6. Phase 6 : Documentation Technique
7. Phase 7 : Mise en Perspective

## Questions restantes
- Comment fonctionne exactement Small_LLM_Model ?
- Quelle stratégie de prompt engineering sera la plus efficace ?
```

**2. Notes sur le sujet** (`Formation/Notes/lecture_sujet.md`) :

```markdown
# Lecture du sujet

## Date : 2024-01-15

## Objectif principal
Créer un function calling tool qui :
- Reçoit une question en langage naturel
- Identifie quelle fonction appeler
- Extrait les arguments avec les bons types
- Retourne un JSON structuré (pas la réponse directe)

## Contraintes importantes
- Interdit d'inclure les définitions complètes dans le prompt
- Doit utiliser prompt engineering et interactions au niveau des tokens
- Format de sortie JSON strict
- Gestion d'erreurs complète obligatoire

## Défis techniques identifiés
1. Prompt engineering sans définitions complètes
2. Génération contrôlée token par token
3. Parsing flexible des réponses
4. Validation stricte avec Pydantic

## Questions
- Comment structurer le prompt avec exemples ?
- Quelle stratégie de génération utiliser ?
```

---

## Exercice 7 – Configuration de Git (optionnel)

### Solution

**1. .gitignore** (déjà créé via template) :

```gitignore
# Environnement Python
.venv/
venv/
__pycache__/
*.py[cod]

# uv
uv.lock

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Projet spécifique
Dev/output/
*.log
.pytest_cache/
```

**2. Premier commit** :

```bash
$ git init
$ git add .
$ git commit -m "Initial commit: Setup environment and documentation"
```

---

## Validation finale

### Checklist complète

- [x] uv installé et fonctionnel (`uv --version`)
- [x] Environnement créé (`uv sync` exécuté sans erreur)
- [x] Packages installés (numpy, pydantic)
- [x] Makefile créé avec toutes les cibles
- [x] Script check_env.py créé et fonctionnel
- [x] Arborescence documentée
- [x] Documentation lue (general.md et sujet)
- [x] Tous les exercices complétés
- [x] Notes prises dans `Formation/Notes/`

### Test final

```bash
# Exécuter tous les checks
$ make check-env
✓ Tous les checks sont passés

# Tous les tests doivent passer
$ bash M0_onboarding/tests/test_all.sh
✓ Tous les tests sont passés
```

---

## Notes importantes

- Les corrigés montrent les **solutions attendues**, mais il peut y avoir plusieurs façons valides de résoudre les exercices
- Adaptez les solutions à votre environnement spécifique
- Si vous rencontrez des erreurs, consultez la section "Résolution de problèmes" dans `onboarding_1_cours.md`
