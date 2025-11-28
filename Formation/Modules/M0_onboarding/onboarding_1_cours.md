# M0 – Cours Détaillé : Onboarding & Environnement

## 1. Introduction

Ce module prépare votre environnement de développement pour le projet Call Me Maybe. L'objectif est d'avoir un environnement reproductible, isolé et documenté avant de commencer à coder.

### 1.1 Pourquoi un environnement isolé ?

- **Reproductibilité** : Les versions exactes des dépendances sont verrouillées
- **Isolation** : Pas de conflit avec d'autres projets Python
- **Collaboration** : Tous les développeurs utilisent les mêmes versions
- **Déploiement** : L'environnement de production peut être identique

### 1.2 Outils utilisés

- **uv** : Gestionnaire de paquets Python moderne et rapide (remplace pip + venv)
- **Makefile** : Automatisation des tâches répétitives
- **flake8** : Linter pour vérifier la qualité du code

---

## 2. Installation de uv

### 2.1 Installation sur macOS/Linux

```bash
# Installation via script officiel
curl -LsSf https://astral.sh/uv/install.sh | sh

# Vérification
uv --version
# Sortie attendue : uv 0.4.x (CPython 3.11.x)
```

### 2.2 Installation sur Windows

```powershell
# Via PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Ou via pip (si Python déjà installé)
pip install uv
```

### 2.3 Vérification de l'installation

```bash
# Test rapide
uv --help
# Doit afficher la liste des commandes disponibles

# Vérifier que uv est dans le PATH
which uv  # macOS/Linux
where uv  # Windows
```

**Problèmes courants** :
- Si `uv: command not found` : ajouter `~/.cargo/bin` au PATH ou redémarrer le terminal
- Sur macOS, peut nécessiter `xcode-select --install` pour les outils de compilation

---

## 3. Structure du projet

### 3.1 Arborescence complète

```
Call_me_maybe/
├── .CursorSpec/              # Documentation partagée avec l'IA
│   ├── general.md            # Document général du projet
│   └── 0_prompt_sujet42.md   # Template de prompt réutilisable
├── Doc/                      # Documentation
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
├── Dev/                      # Code source (à créer)
│   ├── src/                  # Code Python principal
│   ├── input/                 # Fichiers d'entrée
│   ├── output/                # Fichiers de sortie
│   ├── Makefile              # Automatisation
│   └── pyproject.toml        # Configuration uv
├── scripts/                  # Scripts utilitaires
├── .gitignore               # Fichiers ignorés par Git
└── README.md                # Description du projet
```

### 3.2 Fichiers clés à comprendre

**`.CursorSpec/general.md`** : Document central qui décrit tout le projet. À lire en premier.

**`Doc/Sujet/Call_me_maybe_subject_fr.md`** : Sujet complet avec toutes les contraintes et exigences.

**`Dev/pyproject.toml`** : Configuration des dépendances Python (équivalent de `requirements.txt` mais plus moderne).

---

## 4. Configuration de l'environnement avec uv

### 4.1 Création du fichier pyproject.toml

Le fichier `pyproject.toml` définit les dépendances du projet :

```toml
[project]
name = "call-me-maybe"
version = "0.1.0"
description = "Function calling tool for LLMs"
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
exclude = [".git", "__pycache__", ".venv"]
```

### 4.2 Synchronisation des dépendances

```bash
# Créer l'environnement virtuel et installer les dépendances
uv sync

# Cette commande :
# 1. Crée un environnement virtuel dans .venv/
# 2. Installe les dépendances listées dans pyproject.toml
# 3. Génère un fichier uv.lock (verrouillage des versions exactes)
```

### 4.3 Vérification de l'installation

```bash
# Lister les packages installés
uv pip list

# Vérifier la version de Python
uv run python --version
# Doit afficher : Python 3.11.x ou supérieur

# Tester l'import des dépendances
uv run python -c "import numpy; import pydantic; print('OK')"
```

### 4.4 Gestion de llm_sdk

Selon le sujet, `llm_sdk` doit être copié dans le même dossier que `src` :

```bash
# Structure attendue
Dev/
├── src/
│   └── __init__.py
└── llm_sdk/          # Copié depuis le projet fourni
    └── ...
```

**Important** : `llm_sdk` n'est pas installé via `uv`, il est fourni séparément.

---

## 5. Makefile : Automatisation des tâches

### 5.1 Structure d'un Makefile

Un Makefile contient des **cibles** (targets) qui exécutent des commandes :

```make
# Syntaxe générale
cible:
	commande1
	commande2
	@commande3  # @ masque l'affichage de la commande
```

### 5.2 Makefile complet pour le projet

```make
.PHONY: install run debug lint clean doc check-env

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
	uv run flake8 Dev/src --max-line-length=100

# Nettoyage des fichiers temporaires
clean:
	@echo "Nettoyage..."
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .mypy_cache

# Ouverture de la documentation
doc:
	@echo "Ouverture de la documentation..."
	@open Doc/Sujet/Call_me_maybe_subject_fr.md || \
	 xdg-open Doc/Sujet/Call_me_maybe_subject_fr.md || \
	 echo "Ouvrez manuellement: Doc/Sujet/Call_me_maybe_subject_fr.md"

# Vérification de l'environnement
check-env:
	@echo "Vérification de l'environnement..."
	@uv run python scripts/check_env.py
```

### 5.3 Utilisation du Makefile

```bash
# Installer les dépendances
make install

# Exécuter le programme
make run

# Vérifier le code
make lint

# Nettoyer
make clean

# Voir toutes les cibles disponibles
make help  # Si défini, sinon juste regarder le Makefile
```

### 5.4 Points importants

- **`.PHONY`** : Indique que les cibles ne correspondent pas à des fichiers
- **Tabulations** : Les commandes doivent être indentées avec des **tabs**, pas des espaces
- **`@`** : Masque l'affichage de la commande (utile pour les messages personnalisés)

---

## 6. Configuration de flake8

### 6.1 Installation

Flake8 est généralement installé via uv, mais peut aussi être ajouté comme dépendance de développement :

```toml
[project.optional-dependencies]
dev = [
    "flake8>=6.0.0",
]
```

Puis : `uv sync --extra dev`

### 6.2 Configuration

Créer un fichier `.flake8` ou `setup.cfg` :

```ini
[flake8]
max-line-length = 100
exclude = 
    .git,
    __pycache__,
    .venv,
    build,
    dist
ignore = 
    E203,  # whitespace before ':'
    E501,  # line too long (géré par max-line-length)
```

### 6.3 Utilisation

```bash
# Vérifier un fichier
uv run flake8 Dev/src/main.py

# Vérifier un dossier
uv run flake8 Dev/src/

# Avec le Makefile
make lint
```

---

## 7. Script de vérification de l'environnement

### 7.1 Script complet

Créer `scripts/check_env.py` :

```python
#!/usr/bin/env python3
"""Script de vérification de l'environnement de développement."""

import sys
import platform
import json
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
    required_dirs = [
        'Doc',
        'Formation',
        'Dev',
    ]
    
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
    
    # Vérifier les cibles essentielles
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

### 7.2 Utilisation

```bash
# Exécuter le script
uv run python scripts/check_env.py

# Ou via Makefile
make check-env
```

---

## 8. Bonnes pratiques

### 8.1 Journal de bord

Créer `Formation/Notes/log_onboarding.md` pour documenter :

```markdown
# Journal d'onboarding

## Date : [DATE]

### Installation uv
- Version installée : uv 0.4.x
- Commande : `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Problèmes rencontrés : [aucun / description]

### Configuration environnement
- Commande : `uv sync`
- Packages installés : numpy, pydantic
- Problèmes rencontrés : [aucun / description]

### Makefile
- Cibles testées : install, run, lint, clean, doc
- Problèmes rencontrés : [aucun / description]
```

### 8.2 Git et .gitignore

Fichier `.gitignore` recommandé :

```gitignore
# Environnement Python
.venv/
venv/
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# uv
uv.lock

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Projet spécifique
Dev/output/
*.log
.pytest_cache/
.mypy_cache/
```

### 8.3 Vérifications avant de commencer

- [ ] uv installé et fonctionnel
- [ ] `uv sync` exécuté sans erreur
- [ ] `make install` fonctionne
- [ ] `make lint` fonctionne (même sans code)
- [ ] `make check-env` passe tous les checks
- [ ] Structure du projet comprise
- [ ] Documentation lue (`general.md` et sujet)

---

## 9. Résolution de problèmes courants

### 9.1 uv: command not found

**Problème** : La commande `uv` n'est pas trouvée après installation.

**Solutions** :
```bash
# Vérifier l'installation
ls ~/.cargo/bin/uv

# Ajouter au PATH (macOS/Linux)
export PATH="$HOME/.cargo/bin:$PATH"

# Ajouter de façon permanente dans ~/.zshrc ou ~/.bashrc
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 9.2 Erreur lors de uv sync

**Problème** : `uv sync` échoue avec une erreur.

**Solutions** :
```bash
# Vérifier la version de Python
python3 --version  # Doit être 3.11+

# Nettoyer et réessayer
rm -rf .venv uv.lock
uv sync

# Vérifier pyproject.toml
cat Dev/pyproject.toml
```

### 9.3 Makefile : missing separator

**Problème** : Erreur "missing separator" dans le Makefile.

**Cause** : Les commandes doivent être indentées avec des **tabs**, pas des espaces.

**Solution** : Configurer l'éditeur pour afficher les tabs et utiliser uniquement des tabs pour l'indentation.

---

## 10. Ressources complémentaires

### 10.1 Documentation officielle

- **uv** : https://docs.astral.sh/uv/
- **Makefile** : https://www.gnu.org/software/make/manual/
- **flake8** : https://flake8.pycqa.org/

### 10.2 Tutoriels

- **FR** : [OpenClassrooms – Automatisez vos tâches avec Make](https://openclassrooms.com/fr/courses/6817271-automatisez-vos-taches-avec-make)
- **EN** : [Real Python – Python Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

---

## Conclusion

Vous devriez maintenant avoir :
- ✅ uv installé et fonctionnel
- ✅ Environnement virtuel créé avec les dépendances
- ✅ Makefile opérationnel avec toutes les cibles
- ✅ Script de vérification fonctionnel
- ✅ Compréhension de la structure du projet

**Prochaine étape** : Module M1 - Fondamentaux LLM & Tokenisation
