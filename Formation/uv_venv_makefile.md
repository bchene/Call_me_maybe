Gestion d'Environnements Python avec uv

Ce document détaille la procédure pour installer, configurer et utiliser uv comme gestionnaire de paquets et d'environnements virtuels en remplacement de Conda.

1. Installation de uv

L'installation se fait via un script officiel qui configure automatiquement le path.

# Téléchargement et installation
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Vérification de l'installation
uv --version


2. Création d'un venv avec uv

La création de l'environnement virtuel est séparée de l'installation des paquets.

# Se placer dans le dossier du projet
cd /chemin/vers/mon_projet

# Créer l'environnement avec une version spécifique de Python (recommandé)
# uv télécharge automatiquement cette version si elle est absente
uv venv --python 3.10

# Activer l'environnement (pour un usage manuel dans le terminal)
source .venv/bin/activate


3. Principe

Contrairement à Conda qui mélange gestion de système et de paquets, uv adopte une approche modulaire standard :

Structure : uv venv crée un dossier local .venv contenant l'interpréteur Python isolé.

Version : Si --python X.Y est spécifié, uv récupère cette version exacte. Sinon, il utilise l'interpréteur du système.

Paquets : L'installation des bibliothèques se fait ensuite via uv pip install, qui est une implémentation ultra-rapide de pip.

4. Utilisation Reproductible

Pour garantir qu'un projet fonctionne à l'identique sur une autre machine, on combine requirements.txt et un Makefile.

Fichier requirements.txt

Ce fichier liste les dépendances.

Commande pour installer les dépendances :

uv pip install -r requirements.txt


Commande pour geler les versions actuelles (snapshot) :

uv pip freeze > requirements.txt


Modèle requirements.txt (Exemple)

pandas
numpy
matplotlib
seaborn
scikit-learn
ipykernel


Fichier Makefile

Le Makefile automatise les tâches. Il pointe directement vers les exécutables du dossier .venv pour éviter les problèmes d'activation de shell.

Modèle Makefile (Copier-coller)

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Installation complète (création venv + dépendances)
install:
	uv venv --python 3.10
	$(PIP) install -r requirements.txt

# Lancer le script principal
run:
	$(PYTHON) main.py

# Sauvegarder les dépendances actuelles
freeze:
	$(PIP) freeze > requirements.txt

# Supprimer l'environnement virtuel
clean:
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: install run freeze clean


Annexe : Désinstallation de Conda (macOS)

Si vous migrez de Conda vers uv, voici comment supprimer proprement Conda.

Désactiver l'auto-activation

conda config --set auto_activate_base false


Nettoyer la configuration du Shell

Ouvrez le fichier de configuration (~/.zshrc ou ~/.bash_profile).

Supprimez tout le bloc de code compris entre :
# >>> conda initialize >>>
et
# <<< conda initialize <<<

Supprimer les fichiers
Supprimez le dossier d'installation (le chemin peut varier selon votre installation initiale).

rm -rf ~/anaconda3
# Ou
rm -rf ~/opt/anaconda3
