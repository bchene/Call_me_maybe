# Architecture du Système - Call Me Maybe

## Vue d'Ensemble

Ce document présente l'architecture technique du système de function calling pour LLMs, avec des schémas et diagrammes détaillés.

---

## 1. Architecture en Couches

```
┌─────────────────────────────────────────────────────────────┐
│                    COUCHE APPLICATION                       │
│                  (Orchestration & I/O)                      │
│  - main.py (point d'entrée)                                 │
│  - input_handler.py (chargement JSON)                       │
│  - output_handler.py (écriture JSON)                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  COUCHE LOGIQUE MÉTIER                      │
│              (Traitement des prompts)                       │
│  - prompt_engineering.py (construction prompts)             │
│  - parser.py (extraction données)                           │
│  - validator.py (validation Pydantic)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              COUCHE INTERACTION LLM                         │
│          (Tokenisation & Génération)                        │
│  - tokenizer.py (texte ↔ tokens ↔ input_ids)                │
│  - llm_interaction.py (génération token par token)          │
│  - decoder.py (tokens → texte)                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              COUCHE INFRASTRUCTURE                          │
│         (Modèle LLM & Vocabulaire)                          │
│  - Small_LLM_Model (fourni par le projet)                   │
│  - Vocabulaire JSON (fourni par le projet)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Diagramme de Séquence - Traitement d'un Prompt

```
User/System          main.py        InputHandler    PromptEng    Tokenizer    LLMInteract    Decoder    Parser    Validator    OutputHandler
    │                  │                 │             │            │            │            │         │          │              │
    │───run()─────────>│                 │             │            │            │            │         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───load()───────>│             │            │            │            │         │          │              │
    │                  │<───data─────────│             │            │            │            │         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───build()───────┼────────────>│            │            │            │         │          │              │
    │                  │<───prompt───────┼─────────────│            │            │            │         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───tokenize()────┼─────────────┼───────────>│            │            │         │          │              │
    │                  │<───input_ids────┼─────────────┼────────────│            │            │         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───generate()────┼─────────────┼────────────┼───────────>│            │         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │                 │             │            │            │───logits──>│         │          │              │
    │                  │                 │             │            │            │<──logits───│         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │                 │             │            │            │ (loop)     │         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │<───tokens───────┼─────────────┼────────────┼────────────│            │         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───decode()──────┼─────────────┼────────────┼────────────┼───────────>│         │          │              │
    │                  │<───text─────────┼─────────────┼────────────┼────────────┼────────────│         │          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───parse()───────┼─────────────┼────────────┼────────────┼────────────┼────────>│          │              │
    │                  │<───data─────────┼─────────────┼────────────┼────────────┼────────────┼─────────│          │              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───validate()────┼─────────────┼────────────┼────────────┼────────────┼─────────┼─────────>│              │
    │                  │<───valid────────┼─────────────┼────────────┼────────────┼────────────┼─────────┼──────────│              │
    │                  │                 │             │            │            │            │         │          │              │
    │                  │───write()───────┼─────────────┼────────────┼────────────┼────────────┼─────────┼──────────┼─────────────>│─
    │                  │                 │             │            │            │            │         │          │              │
    │<───success───────│                 │             │            │            │            │         │          │              │
```

---

## 3. Flux de Données Détaillé

### 3.1 Flux Complet

```
┌─────────────────┐
│  Input Files    │
│  (JSON)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Input Handler   │───► Validation JSON
│                 │───► Parsing en structures Python
└────────┬────────┘
         │
         │ Prompts + Function Definitions
         ▼
┌─────────────────────────────────────────┐
│  Pour chaque prompt :                   │
│                                         │
│  1. Prompt Engineering                  │
│     └─► Construction prompt avec        │
│         exemples                        │
│                                         │
│  2. Tokenization                        │
│     └─► Texte → Tokens → Input_Ids      │
│                                         │
│  3. LLM Interaction                     │
│     └─► Génération token par token      │
│         (boucle)                        │
│                                         │
│  4. Decoding                            │
│     └─► Tokens → Texte                  │
│                                         │
│  5. Parsing                             │
│     └─► Extraction fn_name + args       │
│                                         │
│  6. Validation                          │
│     └─► Validation Pydantic             │
│                                         │
│  7. Ajout au résultat                   │
│                                         │
└────────┬────────────────────────────────┘
         │
         │ Liste de résultats validés
         ▼
┌─────────────────┐
│ Output Handler  │───► Formatage JSON
│                 │───► Écriture fichier
└─────────────────┘
```

### 3.2 Flux LLM (Détail)

```
Prompt Text
    │
    ▼
┌──────────────────┐
│ Tokenization     │
│                  │
│ 1. Load vocab    │
│ 2. Text → Tokens │
│ 3. Tokens → IDs  │
└────────┬─────────┘
         │
         │ Input_Ids (numpy array)
         ▼
┌──────────────────┐
│ LLM Interaction  │
│                  │
│ Loop:            │
│  - Get logits    │
│  - Select token  │
│  - Add to seq    │
│  - Check stop    │
└────────┬─────────┘
         │
         │ Generated Input_Ids
         ▼
┌──────────────────┐
│ Decoding         │
│                  │
│ 1. IDs → Tokens  │
│ 2. Tokens → Text │
└────────┬─────────┘
         │
         │ Generated Text
         ▼
```

---

## 4. Structure des Données

### 4.1 Structures d'Entrée

**Function Calling Tests** :
```json
[
    "prompt 1",
    "prompt 2",
    ...
]
```

**Function Definitions** :
```json
{
    "fn_name_1": {
        "args": {
            "arg1": "type1",
            "arg2": "type2"
        },
        "return_type": "type"
    },
    ...
}
```

### 4.2 Structures Intermédiaires

**Prompt Construit** :
```
String avec exemples + question actuelle
```

**Input IDs** :
```
numpy.ndarray([id1, id2, id3, ...])
```

**Logits** :
```
numpy.ndarray([prob1, prob2, ..., probN])
```

**Texte Généré** :
```
String (potentiellement JSON)
```

### 4.3 Structures de Sortie

**Function Call Result** :
```python
{
    "prompt": str,
    "fn_name": str,
    "args": dict
}
```

**Output File** :
```json
[
    {
        "prompt": "...",
        "fn_name": "...",
        "args": {...}
    },
    ...
]
```

---

## 5. Interactions entre Modules

### 5.1 Dépendances

```
main.py
  ├─► input_handler.py
  ├─► prompt_engineering.py
  ├─► tokenizer.py
  ├─► llm_interaction.py
  ├─► decoder.py
  ├─► parser.py
  ├─► validator.py
  └─► output_handler.py

validator.py
  └─► models.py (Pydantic)

llm_interaction.py
  └─► Small_LLM_Model (fourni)

tokenizer.py
  └─► Vocabulaire JSON (fourni)
```

### 5.2 Interfaces entre Modules

**Input Handler → Prompt Engineering** :
- Input : Liste de prompts (strings)
- Output : Prompts avec contexte

**Prompt Engineering → Tokenizer** :
- Input : Prompt text (string)
- Output : Input IDs (numpy array)

**Tokenizer → LLM Interaction** :
- Input : Input IDs (numpy array)
- Output : Input IDs (numpy array) [pas de transformation]

**LLM Interaction → Decoder** :
- Input : Generated Input IDs (numpy array)
- Output : Generated Input IDs (numpy array) [pas de transformation]

**Decoder → Parser** :
- Input : Generated Input IDs (numpy array)
- Output : Generated text (string)

**Parser → Validator** :
- Input : Generated text (string)
- Output : Parsed data (dict)

**Validator → Output Handler** :
- Input : Validated data (Pydantic models)
- Output : Validated data (dict)

---

## 6. Gestion des Erreurs

### 6.1 Points de Contrôle

```
┌─────────────────┐
│ Input Loading   │───► Erreur : Fichier manquant/invalide
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Tokenization    │───► Erreur : Token inconnu
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ LLM Generation  │───► Erreur : Échec génération
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Parsing         │───► Erreur : JSON invalide
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Validation      │───► Erreur : Données invalides
└─────────────────┘
```

### 6.2 Stratégie de Gestion

- **Erreur fatale** : Arrêt du programme
- **Erreur de prompt** : Skip du prompt, log, continuation
- **Erreur récupérable** : Retry ou correction automatique

---

## 7. Performance et Optimisations

### 7.1 Points d'Optimisation

1. **Chargement du vocabulaire** : Une seule fois au démarrage
2. **Génération token par token** : Optimiser la boucle
3. **Validation** : Validation progressive (arrêt précoce si erreur)

### 7.2 Limitations

- Génération token par token peut être lent
- Pas de parallélisation possible (séquentiel par prompt)

---

*Document créé lors de la Phase 2 - Conception et Architecture*  
*Date : [À compléter]*

