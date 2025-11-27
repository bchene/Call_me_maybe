version 1.0
# call_me_maybe
***Introduction au function calling dans les LLMs***

**Résumé**  
Les LLMs parlent-ils la langue des ordinateurs ? Nous allons le découvrir.  
Réalisé en collaboration avec @ldevelle, @pcamaren, @crfernan

## Sommaire

- [1 Préface](#1-préface)
- [2 Instructions communes](#2-instructions-communes)
  - [2.1 Règles générales](#21-règles-générales)
  - [2.2 Makefile](#22-makefile)
  - [2.3 Consignes supplémentaires](#23-consignes-supplémentaires)
    - [2.3.1 Instructions additionnelles](#231-instructions-additionnelles)
- [3 Les LLMs parlent-ils la langue des ordinateurs ?](#3-les-llms-parlent-ils-la-langue-des-ordinateurs-)
  - [3.0.1 Résumé](#301-résumé)
  - [3.0.2 Input](#302-input)
  - [3.0.3 Interaction avec lllm](#303-interaction-avec-lllm)
  - [3.0.4 Format du fichier de sortie](#304-format-du-fichier-de-sortie)

## 1 Préface

Les ingénieurs romains gravaient des tablettes de pierre avec des quadrillages parfaits pour suivre les cargaisons de grains à travers l’empire, afin qu’aucune livraison ne soit perdue à cause d’une écriture illisible. Au XIXᵉ siècle, les marins consignaient les courants océaniques dans des tableaux structurés si précis que certains sont encore utilisés en navigation aujourd’hui.
  
Les premières prévisions météo étaient envoyées sous forme de télégrammes codés — quelques chiffres décrivaient tout un ciel. Dans les années 1960, le contrôle mission de la NASA travaillait avec des organigrammes plastifiés qui expliquaient exactement la signification de chaque voyant, quel que soit l’opérateur de service. Les lecteurs de codes-barres des supermarchés traduisaient les bandes noires et blanches en données d’inventaire bien avant que la plupart des foyers ne possèdent un ordinateur. Même les apiculteurs utilisent depuis des décennies des formulaires normalisés, enregistrant l’état des ruches, le flux de nectar et la lignée des reines dans de minuscules cases qu’eux seuls pouvaient lire d’un coup d’œil.
  
Les humains ont toujours construit des structures pour rendre l’information fiable, partageable et exploitable. Ce qui nous amène à aujourd’hui, où l’objectif est de faire parler aux IA la langue des ordinateurs.

### 2.1 Règles générales

- Votre projet doit être écrit en **Python 3.11 ou supérieur**.
- Votre projet doit respecter le standard de code **flake8**. Les fichiers bonus y sont également soumis.
- Vos fonctions doivent gérer les exceptions proprement afin d’éviter les crashs. Utilisez des blocs try-except pour traiter les erreurs potentielles. Si votre programme plante à cause d’exceptions non gérées pendant la soutenance, il sera considéré comme non fonctionnel.
- Toutes les ressources (par ex. descripteurs de fichiers, connexions réseau) doivent être correctement gérées pour éviter les fuites.

### 2.2 Makefile

Incluez un Makefile dans votre projet pour automatiser les tâches courantes. Il doit contenir les règles suivantes :
- **install** : installe les dépendances du projet via pip, uv, pipx ou tout autre gestionnaire de paquets de votre choix.
- **run** : exécute le script principal de votre projet.
- **debug** : lance le script principal en mode debug avec le debugger intégré de Python.
- **clean** : supprime les fichiers temporaires ou caches pour garder un environnement propre.
- **lint** : lance flake8 afin de garantir le respect des standards de code.

### 2.3 Consignes supplémentaires
- Créez des programmes de test pour vérifier les fonctionnalités du projet (non soumis ni notés).
- Soumettez votre travail dans le dépôt Git assigné. Seul le contenu présent dans ce dépôt sera évalué.
  
_Si des exigences supplémentaires propres au projet s’appliquent, elles seront indiquées immédiatement après cette section._

#### 2.3.1 Instructions additionnelles
- Toutes les classes doivent utiliser **pydantic** pour la validation.
- Vous pouvez utiliser les packages **numpy** et **json**.
- L’usage de **dspy** (ou de tout package similaire) est strictement interdit, y compris pytorch, huggingface package, transformers, etc.
- Vous devez utiliser les modèles suivants :
  - **Qwen/Qwen3-0.6B** (par défaut)
  - Vous pouvez utiliser d’autres modèles tant qu’ils fonctionnent avec **Qwen/Qwen3-0.6B**
- La fonction à appeler doit être choisie par le LLM, et non via des heuristiques ou toute autre magie médiévale.
- Il est interdit d’utiliser des méthodes ou attributs privés du package LLM_SDK.
- Vous devez créer un environnement virtuel et installer les packages **numpy** et **pydantic** avec **uv**. Pour utiliser **llm_sdk**, vous pouvez le copier dans le même dossier que celui contenant src.
- Les évaluateurs, ainsi que la moulinette, lanceront uniquement uv sync.
- Votre programme doit être exécuté avec la commande suivante (où src est le dossier contenant vos fichiers) :
```bash
uv run python -m src
```
- Toutes les erreurs doivent être gérées proprement. Le programme ne doit jamais planter de façon inattendue et doit toujours fournir un message d’erreur clair à l’utilisateur.

## 3 Les LLMs parlent-ils la langue des ordinateurs ?

#### 3.0.1 Résumé

Dans ce projet, vous devez créer un function calling tool. Qu’est-ce que c’est ? C’est un programme qui reçoit une question et, au lieu d’en renvoyer directement la réponse, fournit une boîte à outils pour la résoudre.
  
Par exemple, pour la question « Quelle est la somme de 40 et 2 ? », la solution ne doit pas renvoyer 42, mais fournir une fonction à appeler, dans ce cas précis fn_add_numbers, avec les arguments 40 et 2.

#### 3.0.2 Input

Même si 42 a de grandes attentes vis-à-vis de ses étudiant·es, on ne vous demande pas de coder le function-calling-crystal-ball. Du moins, pas encore.
  
Pour vous faire une idée des types de problèmes que votre solution doit résoudre, vous disposez du fichier input/function_calling_tests.json, qui contient une **liste structurée JSON** de **prompts** possibles à fournir à votre fonction.
  
Dans le fichier input/function_definitions.json, vous trouverez une liste de fonctions parmi lesquelles votre solution devra choisir celle à appeler pour résoudre chaque prompt. Cette liste inclut la définition des noms et types des arguments, ainsi que le type de retour de chaque fonction.
  
_WARNING : Ces exemples servent à établir le niveau de complexité attendu. Gardez néanmoins à l’esprit que votre solution sera testée avec d’autres prompts et différents ensembles de fonctions. Sinon l’exercice ne serait pas très stimulant. Vous devez implémenter une gestion appropriée des erreurs JSON pour les fichiers d’entrée, car ils peuvent contenir du JSON invalide ou être manquants._

#### 3.0.3 Interaction avec lllm

Nous avons mis le mot prompt en évidence ; vous vous doutez donc déjà que vous interagirez avec une IA d’une manière ou d’une autre. Et devinez quoi ? Vous avez encore raison !
  
La solution attendue doit interagir avec un LLM pour produire la boîte à outils évoquée plus haut.
  
Ce projet inclut une classe wrapper **Small_LLM_Model** que vous pouvez utiliser pour interagir avec le LLM.
  
Deux méthodes permettent l’interaction :
- get_logits_from_input_ids : prend un tenseur input_ids et renvoie les logits bruts après l’appel au modèle LLM.
- get_path_to_vocabulary_json : renvoie l’emplacement sur votre machine du JSON structuré qui fait correspondre les input_ids aux tokens.
  
Le schéma suivant illustre le processus d’interaction avec le LLM.
  
**Prompt → Tokens → Inputs_Ids → LLM_Interaction → Logits → Next_Token**
  
_WARNING : Votre solution ne doit pas consister à inclure l’intégralité du JSON function definitions directement dans le prompt envoyé au LLM. Cette approche serait considérée comme invalide, car elle contourne le défi principal qui consiste à faire comprendre et raisonner le LLM sur le function calling via un prompt engineering adéquat et des interactions au niveau des tokens._

#### 3.0.4 Format du fichier de sortie
Votre programme produira un unique fichier JSON : output/function_calling_name.json. Pour chaque prompt, ajoutez un objet JSON à ce fichier. Chaque objet du tableau doit contenir exactement les clés suivantes :
- str : la requête originale en langage naturel.
- str : le nom de la fonction à appeler.
- object : tous les arguments requis avec les bons types.
  
Par exemple :  
**output/function_calling_name.json**
```json
[
    {
        "prompt": "What is the sum of 2 and 3?"
        "fn_name": "fn_add_numbers",
        "args": { "a": 2.0, "b": 3.0 }
    },
    {
        "prompt": "Reverse the string ’hello’",
        "fn_name": "fn_reverse_string",
        "args": { "s": "hello" }
    }
]

```

Règles de validation :
- Le fichier doit être un JSON valide (pas de virgules finales, pas de commentaires).
- Les clés et types doivent correspondre exactement au schéma défini dans functions_definitions.json.
- Aucune clé supplémentaire ni texte libre n’est autorisé dans la sortie.

Le fichier est généré à l’exécution par le scaffold ; votre rôle est de guider le modèle pour que chaque fn_name et args prédits passent la validation et se retrouvent dans output/function_calling_name.json comme montré ci-dessus.
  
Les fichiers fournis peuvent changer pendant l’évaluation, donc ne les utilisez pas comme référence figée.

