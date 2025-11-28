# Phase 1 : Analyse et Compréhension du Sujet

## Vue d'Ensemble

**Projet** : Call Me Maybe  
**Objectif pédagogique** : Introduction au function calling dans les LLMs  
**Question centrale** : Les LLMs parlent-ils la langue des ordinateurs ?

---

## 1. Objectif du Projet

### 1.1 Description Générale

Créer un système de **function calling** qui permet à un LLM de :
- Recevoir une question en langage naturel
- Identifier quelle fonction appeler pour résoudre cette question
- Extraire les arguments nécessaires avec les bons types
- Retourner une structure JSON standardisée (et non la réponse directe)

### 1.2 Exemple Concret

**Input** : "Quelle est la somme de 40 et 2 ?"

**Output attendu** (et non "42") :
```json
{
    "prompt": "Quelle est la somme de 40 et 2 ?",
    "fn_name": "fn_add_numbers",
    "args": { "a": 40.0, "b": 2.0 }
}
```

### 1.3 Enjeu Pédagogique

Le projet vise à comprendre comment faire "parler" un LLM dans un format structuré et exploitable par un ordinateur, plutôt que de générer du texte libre. C'est le pont entre le langage naturel et l'exécution de code.

---

## 2. Concepts Clés Identifiés

### 2.1 Function Calling

**Définition** : Mécanisme permettant à un LLM de sélectionner et d'appeler des fonctions programmées plutôt que de générer directement une réponse textuelle.

**Enjeu** : Le LLM doit comprendre l'intention derrière une question et la mapper vers une fonction disponible avec les bons arguments.

### 2.2 LLMs (Large Language Models)

**Modèle utilisé** : Qwen/Qwen3-0.6B (modèle léger de 0.6 milliards de paramètres)

**Caractéristiques importantes** :
- Modèle pré-entraîné, pas d'entraînement nécessaire
- Accès uniquement via l'API fournie (Small_LLM_Model)
- Interaction au niveau des tokens, pas au niveau du texte

### 2.3 Tokenisation

**Processus** : Conversion du texte en tokens, puis en input_ids

**Flux** :
```
Texte → Tokens (mots/sous-mots) → Input_Ids (nombres) → LLM
```

**Importance** : Le LLM ne comprend pas directement le texte, mais des représentations numériques (tokens). Il faut maîtriser cette conversion.

### 2.4 Logits

**Définition** : Probabilités brutes que le modèle assigne à chaque token du vocabulaire pour le prochain token à générer.

**Utilisation** : Les logits sont la sortie brute du modèle. Il faut les interpréter pour déterminer quel token sera généré.

### 2.5 Prompt Engineering

**Définition** : Art de construire des prompts efficaces pour guider le LLM vers le comportement souhaité.

**Contrainte majeure** : Il est **interdit** d'inclure directement le JSON des définitions de fonctions dans le prompt. Le LLM doit apprendre à raisonner sur le function calling via le prompt engineering et les interactions au niveau des tokens.

### 2.6 JSON Schema et Validation

**Outils** : Pydantic pour la validation des structures de données

**Nécessité** : S'assurer que les sorties du LLM respectent exactement le format attendu (types, clés, structure).

---

## 3. Flux de Traitement Complet

### 3.1 Schéma Global

```
Input Files
    ↓
[function_calling_tests.json] → Prompts en langage naturel
[function_definitions.json] → Définitions des fonctions disponibles
    ↓
Prompt Engineering
    ↓
Tokenisation (Prompt → Tokens → Input_Ids)
    ↓
Interaction LLM (Input_Ids → LLM → Logits)
    ↓
Décodage (Logits → Next_Token → Texte)
    ↓
Parsing et Validation (Texte → JSON structuré)
    ↓
Output File
    ↓
[function_calling_name.json] → Résultats validés
```

### 3.2 Détail du Flux LLM

**Étape par étape** :

1. **Prompt** : Question en langage naturel + contexte (sans les définitions complètes des fonctions)

2. **Tokenisation** :
   - Conversion du prompt en tokens (via le vocabulaire JSON)
   - Conversion des tokens en input_ids (tenseur numérique)

3. **Interaction LLM** :
   - Passage des input_ids au modèle via `get_logits_from_input_ids()`
   - Récupération des logits (probabilités pour chaque token du vocabulaire)

4. **Génération de tokens** :
   - Sélection du token suivant basé sur les logits
   - Itération jusqu'à obtenir une réponse complète

5. **Décodage** :
   - Conversion des tokens générés en texte
   - Utilisation du vocabulaire JSON pour mapper input_ids → tokens → texte

6. **Parsing** :
   - Extraction du nom de fonction et des arguments depuis le texte généré
   - Validation avec pydantic

7. **Formatage** :
   - Création du JSON de sortie conforme au schéma

### 3.3 Points Critiques

- **Pas de définitions complètes dans le prompt** : Le LLM doit inférer les fonctions disponibles
- **Génération token par token** : Contrôle fin sur la génération
- **Validation stricte** : Le JSON doit être parfaitement conforme

---

## 4. Contraintes Techniques Détaillées

### 4.1 Langage et Standards

- **Python 3.11+** : Version minimale requise
- **flake8** : Standard de code strict (tous les fichiers, y compris bonus)
- **Gestion d'erreurs** : Obligatoire partout (try-except)
- **Gestion des ressources** : Pas de fuites (fichiers, connexions, etc.)

### 4.2 Packages Autorisés

**Autorisés** :
- `numpy` : Calculs numériques
- `json` : Manipulation JSON
- `pydantic` : Validation de données (obligatoire pour toutes les classes)

**Strictement interdits** :
- `dspy`
- `pytorch`
- `huggingface` / `transformers`
- Tout package similaire de haut niveau

**Implication** : Il faut travailler au niveau bas (tokens, logits) sans frameworks d'abstraction.

### 4.3 Modèle LLM

- **Modèle par défaut** : Qwen/Qwen3-0.6B
- **Wrapper fourni** : `Small_LLM_Model`
- **Méthodes disponibles** :
  - `get_logits_from_input_ids(input_ids)` : Obtient les logits
  - `get_path_to_vocabulary_json()` : Chemin vers le vocabulaire

**Contraintes** :
- Pas d'utilisation de méthodes/attributs privés du package LLM_SDK
- Le modèle doit choisir la fonction (pas d'heuristiques)

### 4.4 Structure du Projet

**Exécution** :
```bash
uv run python -m src
```

**Environnement** :
- Environnement virtuel avec `uv`
- Installation : `uv sync` (sera exécuté par les évaluateurs)
- `llm_sdk` copié dans le même dossier que `src`

**Makefile requis** :
- `install` : Installation des dépendances
- `run` : Exécution du script principal
- `debug` : Mode debug
- `clean` : Nettoyage
- `lint` : Vérification flake8

### 4.5 Fichiers d'Entrée

**Input** :
- `input/function_calling_tests.json` : Liste de prompts à traiter
- `input/function_definitions.json` : Définitions des fonctions disponibles

**Caractéristiques** :
- Format JSON structuré
- Peuvent contenir du JSON invalide ou être manquants (gestion d'erreurs requise)
- Peuvent changer pendant l'évaluation (ne pas hardcoder)

### 4.6 Fichier de Sortie

**Output** :
- `output/function_calling_name.json` : Résultats finaux

**Format strict** :
```json
[
    {
        "prompt": "string",
        "fn_name": "string",
        "args": { "key": value }
    }
]
```

**Règles de validation** :
- JSON valide (pas de virgules finales, pas de commentaires)
- Clés exactes : `prompt`, `fn_name`, `args`
- Types correspondant exactement à `function_definitions.json`
- Aucune clé supplémentaire

---

## 5. Défis Techniques Identifiés

### 5.1 Défi Principal : Prompt Engineering sans Définitions Complètes

**Problème** : Comment faire comprendre au LLM quelles fonctions sont disponibles sans lui donner le JSON complet ?

**Approches possibles** :
- Utiliser des exemples dans le prompt
- Construire un prompt qui guide vers le format attendu
- Utiliser le fine-tuning implicite via les exemples
- Exploiter les patterns dans les noms de fonctions

### 5.2 Génération Contrôlée Token par Token

**Problème** : Le LLM génère du texte libre, mais on a besoin d'un format JSON strict.

**Approches possibles** :
- Construire le prompt pour forcer le format JSON
- Parser et valider à chaque token généré
- Utiliser des techniques de "guided generation"
- Implémenter un système de validation itérative

### 5.3 Mapping Prompt → Fonction

**Problème** : Le LLM doit comprendre l'intention sémantique et la mapper vers une fonction.

**Complexité** :
- Ambiguïté possible (plusieurs fonctions pourraient convenir)
- Extraction des arguments depuis le langage naturel
- Gestion des types (string, float, int, etc.)

### 5.4 Gestion des Erreurs Robuste

**Exigences** :
- JSON invalide dans les inputs
- Fichiers manquants
- Réponses du LLM non conformes
- Erreurs de tokenisation
- Erreurs de parsing

**Solution** : Try-except partout + messages d'erreur clairs.

---

## 6. Questions Ouvertes

### 6.1 Questions Techniques

1. **Comment structurer le prompt pour guider le LLM sans donner les définitions complètes ?**
   - Faut-il utiliser des exemples ?
   - Comment encoder les informations sur les fonctions disponibles ?
   - Quel format de prompt est le plus efficace ?

2. **Comment gérer la génération token par token pour garantir un JSON valide ?**
   - Faut-il valider à chaque token ?
   - Comment gérer les cas où le LLM génère du texte non-JSON ?
   - Peut-on forcer certains tokens (guillemets, accolades, etc.) ?

3. **Comment extraire et valider les arguments depuis le texte généré ?**
   - Le LLM génère-t-il directement du JSON ?
   - Faut-il parser du texte libre et extraire les informations ?
   - Comment gérer les types (conversion string → float, etc.) ?

4. **Quelle stratégie pour le vocabulaire et la tokenisation ?**
   - Comment utiliser efficacement le vocabulaire JSON fourni ?
   - Faut-il pré-tokeniser certains éléments ?
   - Comment gérer les tokens spéciaux (JSON, noms de fonctions) ?

5. **Comment optimiser les interactions avec le LLM ?**
   - Faut-il plusieurs passes (génération + validation + correction) ?
   - Comment gérer les cas où le LLM ne génère pas le bon format ?
   - Peut-on utiliser des techniques de "retry" avec prompts différents ?

### 6.2 Questions Architecturales

1. **Quelle architecture pour le système ?**
   - Modules séparés (tokenisation, LLM, parsing, validation) ?
   - Pipeline séquentiel ou avec boucles de correction ?
   - Comment structurer le code pour la maintenabilité ?

2. **Comment gérer la validation avec pydantic ?**
   - Quelles classes créer ?
   - Comment valider les réponses du LLM avant de les écrire ?
   - Comment gérer les erreurs de validation de manière informative ?

3. **Quelle stratégie pour les tests ?**
   - Comment tester sans accès direct au LLM ?
   - Faut-il mocker les interactions LLM ?
   - Comment valider que le système fonctionne avec différents prompts ?

### 6.3 Questions Pédagogiques

1. **Quels concepts approfondir en priorité ?**
   - Tokenisation et représentation des textes
   - Architecture des LLMs (transformer, attention)
   - Prompt engineering
   - Génération de texte contrôlée

2. **Quelles ressources d'apprentissage sont les plus pertinentes ?**
   - Documentation sur les transformers
   - Tutoriels sur le prompt engineering
   - Articles sur le function calling
   - Documentation de pydantic

---

## 7. Éléments à Approfondir

### 7.1 Concepts à Maîtriser

1. **Tokenisation** :
   - Comment fonctionne la tokenisation (BPE, WordPiece, SentencePiece)
   - Mapping tokens ↔ input_ids
   - Gestion du vocabulaire

2. **Architecture des LLMs** :
   - Principe des transformers
   - Mécanisme d'attention
   - Génération autoregressive

3. **Logits et Probabilités** :
   - Comment interpréter les logits
   - Sélection du token suivant (greedy, sampling, temperature)
   - Conversion logits → probabilités → token

4. **Prompt Engineering** :
   - Techniques de construction de prompts
   - Few-shot learning
   - Format de prompts pour le function calling

5. **Validation et Parsing** :
   - Utilisation de pydantic
   - Parsing de JSON depuis du texte libre
   - Gestion des erreurs de validation

### 7.2 Technologies à Explorer

1. **Pydantic** : Validation de données en Python
2. **Numpy** : Manipulation de tenseurs (logits, input_ids)
3. **JSON** : Parsing et génération de JSON valide
4. **uv** : Gestionnaire de paquets et environnement virtuel

---

## 8. Prochaines Étapes

### 8.1 Immédiat (Phase 2)

1. Concevoir l'architecture générale du système
2. Définir les modules et leurs responsabilités
3. Concevoir la stratégie de prompt engineering
4. Planifier la gestion des erreurs

### 8.2 Court Terme (Phase 3-4)

1. Identifier toutes les technologies à apprendre
2. Créer un plan de formation structuré
3. Préparer les ressources d'apprentissage

### 8.3 Moyen Terme (Phase 5)

1. Implémenter le système complet
2. Tester avec les fichiers fournis
3. Valider le comportement

---

## 9. Notes et Observations

### 9.1 Points d'Attention

- Le sujet insiste sur le fait que les fichiers d'entrée peuvent changer : **ne pas hardcoder**
- La gestion d'erreurs est critique : le programme ne doit **jamais** planter
- Le format de sortie doit être **strictement** conforme
- L'interdiction d'utiliser les définitions complètes dans le prompt est un **défi majeur**

### 9.2 Analogies Utiles

- **Function Calling** : Comme un traducteur qui convertit le langage naturel en "langage machine"
- **Tokenisation** : Comme un dictionnaire qui convertit les mots en numéros
- **Logits** : Comme des probabilités brutes que le modèle utilise pour "deviner" le prochain mot

### 9.3 Références Implicites

Le sujet mentionne que les humains ont toujours structuré l'information (tablettes romaines, tableaux de marins, etc.). Le projet s'inscrit dans cette tradition : structurer la sortie des LLMs pour qu'elle soit exploitable par des machines.

---

## Conclusion de l'Analyse

Le projet **Call Me Maybe** est un défi technique intéressant qui combine :
- Compréhension des LLMs au niveau bas (tokens, logits)
- Prompt engineering avancé
- Validation et parsing robustes
- Gestion d'erreurs complète

Le défi principal réside dans le fait de faire comprendre au LLM le concept de function calling sans lui donner directement les définitions, en utilisant uniquement le prompt engineering et les interactions au niveau des tokens.

**Prêt pour la Phase 2 : Conception et Architecture**

---

*Document créé lors de la Phase 1 - Analyse du sujet*  
*Date : [À compléter]*

