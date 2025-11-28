# Phase 2 : Conception et Architecture

## Vue d'Ensemble

Ce document présente la conception détaillée du système de function calling pour LLMs. Il définit l'architecture, les modules, les interactions et les stratégies de résolution des défis identifiés lors de la Phase 1.

---

## 1. Architecture Générale

### 1.1 Vue d'Ensemble du Système

Le système est organisé en modules distincts qui communiquent via des interfaces bien définies :

```
┌─────────────────────────────────────────────────────────────┐
│                    Point d'Entrée (main.py)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼──────────┐
│ Input Handler  │            │  Output Handler   │
│  (JSON Loader) │            │  (JSON Writer)    │
└───────┬────────┘            └───────────────────┘
        │
        │ Prompts + Function Definitions
        │
┌───────▼──────────────────────────────────────────┐
│         Function Calling Orchestrator            │
│  (Coordonne le traitement de chaque prompt)      │
└───────┬──────────────────────────────────────────┘
        │
        │ Pour chaque prompt
        │
┌───────▼──────────────────────────────────────────┐
│            Prompt Engineering Module              │
│  (Construit le prompt optimisé)                  │
└───────┬──────────────────────────────────────────┘
        │
        │ Prompt construit
        │
┌───────▼──────────────────────────────────────────┐
│            Tokenization Module                    │
│  (Texte → Tokens → Input_Ids)                    │
└───────┬──────────────────────────────────────────┘
        │
        │ Input_Ids
        │
┌───────▼──────────────────────────────────────────┐
│            LLM Interaction Module                 │
│  (Génération token par token)                    │
└───────┬──────────────────────────────────────────┘
        │
        │ Tokens générés
        │
┌───────▼──────────────────────────────────────────┐
│            Decoding Module                       │
│  (Tokens → Texte)                                 │
└───────┬──────────────────────────────────────────┘
        │
        │ Texte généré
        │
┌───────▼──────────────────────────────────────────┐
│            Parsing Module                         │
│  (Extraction fn_name + args)                     │
└───────┬──────────────────────────────────────────┘
        │
        │ Données extraites
        │
┌───────▼──────────────────────────────────────────┐
│            Validation Module (Pydantic)           │
│  (Validation des types et structure)              │
└───────┬──────────────────────────────────────────┘
        │
        │ Données validées
        │
        └───────────────┐
                        │
            ┌───────────▼──────────┐
            │   Output Handler     │
            │   (JSON Writer)      │
            └──────────────────────┘
```

### 1.2 Principes de Conception

1. **Séparation des responsabilités** : Chaque module a une responsabilité unique et bien définie
2. **Interfaces claires** : Communication entre modules via des structures de données standardisées
3. **Gestion d'erreurs centralisée** : Chaque module gère ses erreurs et les remonte de manière structurée
4. **Validation à chaque étape** : Validation progressive pour détecter les erreurs tôt
5. **Extensibilité** : Architecture modulaire permettant d'ajouter facilement de nouvelles fonctionnalités

---

## 2. Modules Détaillés

### 2.1 Input Handler (Gestionnaire d'Entrée)

**Responsabilité** : Charger et valider les fichiers d'entrée JSON

**Fonctionnalités** :
- Chargement de `function_calling_tests.json` (liste de prompts)
- Chargement de `function_definitions.json` (définitions des fonctions)
- Validation du format JSON
- Gestion des erreurs (fichier manquant, JSON invalide)

**Structure de données** :
```python
# Pydantic models à créer
- PromptList : Liste de prompts
- FunctionDefinition : Définition d'une fonction
- FunctionDefinitionsList : Liste de définitions
```

**Erreurs à gérer** :
- Fichier introuvable
- JSON invalide (syntaxe incorrecte)
- Structure JSON incorrecte (clés manquantes)
- Types incorrects dans le JSON

### 2.2 Prompt Engineering Module

**Responsabilité** : Construire des prompts efficaces pour guider le LLM

**Défi principal** : Faire comprendre au LLM le concept de function calling sans inclure les définitions complètes

**Stratégie proposée** :

1. **Prompt de base avec exemples** :
   - Inclure quelques exemples de function calling (2-3 exemples)
   - Montrer le format attendu (JSON avec fn_name et args)
   - Utiliser des exemples variés pour couvrir différents types de fonctions

2. **Contexte minimal** :
   - Mentionner qu'il existe des fonctions disponibles
   - Indiquer le format de sortie attendu
   - Ne pas lister toutes les fonctions disponibles

3. **Format de prompt** :
```
Tu es un assistant qui convertit des questions en appels de fonctions.

Format de sortie attendu (JSON) :
{
    "fn_name": "nom_de_la_fonction",
    "args": { "arg1": valeur1, "arg2": valeur2 }
}

Exemples :
Question: "Quelle est la somme de 5 et 3 ?"
Réponse: {"fn_name": "fn_add_numbers", "args": {"a": 5.0, "b": 3.0}}

Question: "Inverse la chaîne 'bonjour'"
Réponse: {"fn_name": "fn_reverse_string", "args": {"s": "bonjour"}}

Question: [QUESTION_ACTUELLE]
Réponse:
```

**Considérations** :
- Le prompt doit être concis pour éviter de dépasser les limites de tokens
- Les exemples doivent être représentatifs mais pas exhaustifs
- Le format JSON doit être clairement indiqué

### 2.3 Tokenization Module

**Responsabilité** : Convertir le texte en tokens puis en input_ids

**Fonctionnalités** :
- Chargement du vocabulaire JSON (via `get_path_to_vocabulary_json()`)
- Conversion texte → tokens (mapping inverse du vocabulaire)
- Conversion tokens → input_ids (mapping direct du vocabulaire)
- Gestion des tokens inconnus (fallback)

**Processus** :
1. Charger le vocabulaire JSON une seule fois au démarrage
2. Pour chaque prompt :
   - Découper le texte en tokens (stratégie à définir)
   - Mapper chaque token à son input_id via le vocabulaire
   - Créer le tenseur input_ids (numpy array)

**Stratégie de tokenisation** :
- Option 1 : Tokenisation simple par mots (split sur espaces)
- Option 2 : Utiliser le vocabulaire pour trouver les tokens (recherche de correspondances)
- Option 3 : Approche hybride (mots simples + recherche dans vocabulaire)

**Erreurs à gérer** :
- Token non trouvé dans le vocabulaire
- Vocabulaire JSON invalide
- Problème de format du vocabulaire

### 2.4 LLM Interaction Module

**Responsabilité** : Interagir avec le LLM pour générer des tokens

**Fonctionnalités** :
- Appel au modèle via `get_logits_from_input_ids()`
- Sélection du token suivant à partir des logits
- Génération itérative token par token
- Arrêt de la génération (critères d'arrêt)

**Processus de génération** :

1. **Initialisation** :
   - Préparer les input_ids du prompt
   - Initialiser la séquence générée (vide)

2. **Boucle de génération** :
   ```
   Tant que (critère d'arrêt non atteint) :
       - Obtenir les logits pour la séquence actuelle
       - Sélectionner le token suivant (stratégie à définir)
       - Ajouter le token à la séquence
       - Vérifier les critères d'arrêt
   ```

3. **Stratégie de sélection du token** :
   - **Greedy** : Prendre le token avec la probabilité la plus élevée
   - **Sampling** : Échantillonner selon les probabilités (avec température)
   - Pour ce projet : **Greedy** semble approprié pour la cohérence

4. **Critères d'arrêt** :
   - Token de fin de séquence (EOS token)
   - Longueur maximale atteinte
   - Détection de fin de JSON (accolade fermante + validation)

**Erreurs à gérer** :
- Erreur lors de l'appel au modèle
- Logits invalides
- Problème de format des input_ids

### 2.5 Decoding Module

**Responsabilité** : Convertir les tokens générés en texte

**Fonctionnalités** :
- Conversion input_ids → tokens (via vocabulaire)
- Conversion tokens → texte (concaténation)
- Gestion des tokens spéciaux

**Processus** :
1. Pour chaque input_id généré :
   - Trouver le token correspondant dans le vocabulaire
   - Ajouter le token au texte en construction
2. Nettoyer le texte (espaces, caractères spéciaux si nécessaire)

**Erreurs à gérer** :
- Input_id non trouvé dans le vocabulaire
- Problème de décodage

### 2.6 Parsing Module

**Responsabilité** : Extraire fn_name et args depuis le texte généré

**Défi** : Le LLM peut générer du texte qui n'est pas du JSON valide

**Stratégies** :

1. **Parsing JSON direct** (si le LLM génère du JSON valide) :
   - Parser le texte comme JSON
   - Extraire fn_name et args

2. **Parsing flexible** :
   - Chercher des patterns JSON dans le texte
   - Extraire le JSON même s'il est entouré de texte
   - Utiliser des expressions régulières pour trouver les structures JSON

3. **Parsing avec correction** :
   - Détecter les erreurs JSON courantes
   - Corriger automatiquement (virgules manquantes, guillemets, etc.)
   - Réessayer le parsing

**Format attendu** :
```json
{
    "fn_name": "nom_fonction",
    "args": { ... }
}
```

**Erreurs à gérer** :
- JSON invalide
- Clés manquantes (fn_name ou args)
- Format incorrect

### 2.7 Validation Module (Pydantic)

**Responsabilité** : Valider les données extraites avec Pydantic

**Fonctionnalités** :
- Validation des types (string pour fn_name, object pour args)
- Validation que fn_name existe dans function_definitions
- Validation que les args correspondent aux définitions
- Validation des types des arguments (float, int, string, etc.)

**Modèles Pydantic à créer** :

```python
# Structure de validation
- FunctionCallResult : Résultat complet (prompt, fn_name, args)
- FunctionCallArgs : Arguments validés selon la définition
- FunctionCallOutput : Liste de résultats pour le fichier de sortie
```

**Processus** :
1. Vérifier que fn_name existe dans les définitions
2. Vérifier que tous les arguments requis sont présents
3. Vérifier que les types correspondent
4. Convertir les types si nécessaire (string → float, etc.)

**Erreurs à gérer** :
- Fonction inconnue
- Arguments manquants
- Types incorrects
- Arguments supplémentaires non autorisés

### 2.8 Output Handler (Gestionnaire de Sortie)

**Responsabilité** : Écrire les résultats dans le fichier JSON de sortie

**Fonctionnalités** :
- Création du fichier output/function_calling_name.json
- Formatage JSON valide (pas de virgules finales, etc.)
- Écriture incrémentale ou en une fois

**Format de sortie** :
```json
[
    {
        "prompt": "...",
        "fn_name": "...",
        "args": { ... }
    },
    ...
]
```

**Erreurs à gérer** :
- Problème d'écriture de fichier
- Problème de formatage JSON
- Permissions insuffisantes

---

## 3. Flux de Données Détaillé

### 3.1 Flux Principal

```
1. Chargement des inputs
   └─> InputHandler charge les fichiers JSON
   └─> Validation de la structure

2. Pour chaque prompt dans function_calling_tests.json :
   
   a. Construction du prompt
      └─> PromptEngineering construit le prompt avec exemples
   
   b. Tokenisation
      └─> Tokenization convertit le prompt en input_ids
   
   c. Génération avec le LLM
      └─> LLMInteraction génère des tokens itérativement
      └─> Décodage des tokens en texte
   
   d. Parsing et validation
      └─> Parsing extrait fn_name et args
      └─> Validation vérifie avec Pydantic
      └─> Si erreur : gestion d'erreur (log, skip, ou retry)
   
   e. Ajout au résultat
      └─> Ajout du résultat validé à la liste

3. Écriture de la sortie
   └─> OutputHandler écrit tous les résultats dans le fichier JSON
```

### 3.2 Gestion des Erreurs

**Stratégie globale** :
- Chaque module gère ses propres erreurs
- Les erreurs sont loggées avec des messages clairs
- En cas d'erreur non récupérable : skip du prompt et continuation
- En cas d'erreur récupérable : retry ou correction automatique

**Types d'erreurs** :
- **Erreurs fatales** : Arrêt du programme (fichiers manquants critiques)
- **Erreurs de prompt** : Skip du prompt, continuation avec les autres
- **Erreurs de validation** : Log de l'erreur, skip du prompt

---

## 4. Stratégies de Résolution des Défis

### 4.1 Défi : Prompt Engineering sans Définitions Complètes

**Solution proposée** :
- Utiliser des exemples représentatifs (2-3 exemples variés)
- Montrer clairement le format JSON attendu
- Mentionner qu'il existe des fonctions sans les lister
- Tester différents formats de prompts et itérer

**Approche itérative** :
1. Commencer avec un prompt simple avec exemples
2. Tester sur quelques prompts
3. Ajuster le prompt selon les résultats
4. Itérer jusqu'à obtenir de bons résultats

### 4.2 Défi : Génération Contrôlée Token par Token

**Solution proposée** :
- Construire le prompt pour forcer le format JSON
- Valider à chaque étape de la génération
- Détecter la fin du JSON (accolade fermante)
- Implémenter un système de "guided generation" si nécessaire

**Techniques** :
- Inclure dans le prompt : "Réponds uniquement avec un JSON valide"
- Détecter les tokens de début/fin de JSON
- Arrêter la génération dès qu'un JSON valide est détecté

### 4.3 Défi : Parsing de Réponses Non-JSON

**Solution proposée** :
- Parsing flexible avec recherche de patterns JSON
- Correction automatique des erreurs JSON courantes
- Extraction du JSON même s'il est entouré de texte
- Fallback : si parsing échoue, essayer d'extraire manuellement

**Techniques** :
- Expressions régulières pour trouver les structures JSON
- Parsing avec gestion d'erreurs et correction
- Validation progressive

### 4.4 Défi : Validation Stricte

**Solution proposée** :
- Utiliser Pydantic pour validation stricte
- Vérifier chaque champ individuellement
- Convertir les types si nécessaire
- Fournir des messages d'erreur clairs

---

## 5. Structure des Fichiers

### 5.1 Organisation du Code

```
Dev/src/
├── __init__.py
├── main.py                 # Point d'entrée
├── input_handler.py        # Chargement des fichiers JSON
├── prompt_engineering.py   # Construction des prompts
├── tokenizer.py            # Tokenisation
├── llm_interaction.py      # Interaction avec le LLM
├── decoder.py              # Décodage tokens → texte
├── parser.py               # Parsing des réponses
├── validator.py             # Validation Pydantic
├── output_handler.py       # Écriture de la sortie
├── models.py               # Modèles Pydantic
└── utils.py                # Utilitaires
```

### 5.2 Modèles Pydantic (models.py)

```python
# Structures de données validées
- PromptInput
- FunctionDefinition
- FunctionCallResult
- FunctionCallArgs
- FunctionCallOutput
```

---

## 6. Points d'Attention et Risques

### 6.1 Risques Identifiés

1. **Le LLM ne génère pas de JSON valide**
   - Mitigation : Parsing flexible + correction automatique

2. **Le LLM ne comprend pas le concept de function calling**
   - Mitigation : Prompt engineering itératif avec exemples

3. **Performance (génération token par token peut être lent)**
   - Mitigation : Optimisation de la boucle de génération

4. **Gestion des tokens inconnus**
   - Mitigation : Stratégie de fallback dans la tokenisation

### 6.2 Tests à Prévoir

- Tests unitaires pour chaque module
- Tests d'intégration pour le flux complet
- Tests avec différents types de prompts
- Tests de gestion d'erreurs

---

## 7. Prochaines Étapes

1. **Phase 3** : Identifier en détail les technologies et concepts à maîtriser
2. **Phase 4** : Créer le plan de formation avec ressources
3. **Phase 5** : Implémenter l'architecture conçue

---

## Conclusion

Cette architecture modulaire permet de :
- Séparer clairement les responsabilités
- Faciliter les tests et la maintenance
- Gérer les erreurs de manière structurée
- Itérer et améliorer chaque composant indépendamment

Le défi principal reste le prompt engineering et la génération contrôlée, qui nécessiteront des tests et ajustements itératifs.

---

*Document créé lors de la Phase 2 - Conception et Architecture*  
*Date : [À compléter]*

