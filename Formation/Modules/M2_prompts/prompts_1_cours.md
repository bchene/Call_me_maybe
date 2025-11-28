# M2 – Cours Détaillé : Function Calling & Prompt Engineering

## 1. Introduction

Le prompt engineering est l'art de construire des prompts efficaces pour guider un LLM vers le comportement souhaité. Dans ce projet, l'objectif est de faire comprendre au LLM le concept de function calling **sans** lui donner directement toutes les définitions de fonctions.

### 1.1 Défi principal

**Contrainte** : Il est **interdit** d'inclure l'intégralité du JSON `function_definitions.json` dans le prompt.

**Objectif** : Le LLM doit comprendre qu'il existe des fonctions disponibles et apprendre à les sélectionner via des exemples (few-shot learning).

### 1.2 Approche proposée

- Utiliser des **exemples représentatifs** (2-3 exemples)
- Montrer le **format JSON attendu** clairement
- Guider le LLM avec des **instructions précises**
- Tester et itérer sur différents formats de prompts

---

## 2. Anatomie d'un Prompt Efficace

### 2.1 Structure en 5 parties

Un prompt efficace pour le function calling se compose de :

1. **Rôle** : Définir le rôle de l'assistant
2. **Format attendu** : Montrer la structure JSON
3. **Exemples few-shot** : 2-3 exemples variés
4. **Question cible** : La question à traiter
5. **Instruction finale** : Rappel du format

### 2.2 Template de base

```
[RÔLE]
Tu es un assistant qui convertit des questions en appels de fonctions structurés.

[FORMAT ATTENDU]
Réponds uniquement avec un JSON valide au format suivant :
{
    "fn_name": "nom_de_la_fonction",
    "args": {
        "arg1": valeur1,
        "arg2": valeur2
    }
}

[EXEMPLES]
Question: "Quelle est la somme de 5 et 3 ?"
Réponse: {"fn_name": "fn_add_numbers", "args": {"a": 5.0, "b": 3.0}}

Question: "Inverse la chaîne 'bonjour'"
Réponse: {"fn_name": "fn_reverse_string", "args": {"s": "bonjour"}}

[QUESTION CIBLE]
Question: [QUESTION_ACTUELLE]

[INSTRUCTION FINALE]
Réponds uniquement avec le JSON, sans texte supplémentaire.
```

### 2.3 Exemple complet

```python
def build_prompt(question: str, examples: list[dict]) -> str:
    """
    Construit un prompt pour le function calling.
    
    Args:
        question: Question à traiter
        examples: Liste d'exemples [{"question": "...", "response": {...}}]
    """
    prompt = """Tu es un assistant qui convertit des questions en appels de fonctions structurés.

Réponds uniquement avec un JSON valide au format suivant :
{
    "fn_name": "nom_de_la_fonction",
    "args": {
        "arg1": valeur1,
        "arg2": valeur2
    }
}

Exemples :
"""
    
    for ex in examples:
        prompt += f'Question: "{ex["question"]}"\n'
        prompt += f'Réponse: {json.dumps(ex["response"], ensure_ascii=False)}\n\n'
    
    prompt += f'Question: "{question}"\n'
    prompt += "Réponse:"
    
    return prompt
```

---

## 3. Techniques de Prompt Engineering

### 3.1 Few-Shot Learning

**Principe** : Montrer des exemples plutôt que d'expliquer.

**Avantages** :
- Le LLM apprend par imitation
- Plus efficace que des instructions longues
- Généralise mieux

**Exemple** :
```python
examples = [
    {
        "question": "Quelle est la somme de 5 et 3 ?",
        "response": {"fn_name": "fn_add_numbers", "args": {"a": 5.0, "b": 3.0}}
    },
    {
        "question": "Inverse la chaîne 'hello'",
        "response": {"fn_name": "fn_reverse_string", "args": {"s": "hello"}}
    },
    {
        "question": "Quelle est la date d'aujourd'hui ?",
        "response": {"fn_name": "fn_get_current_date", "args": {}}
    }
]
```

### 3.2 Guidage lexical

**Principe** : Mentionner explicitement les clés attendues.

**Exemple** :
```
Format attendu :
- fn_name : nom de la fonction (string)
- args : arguments de la fonction (object)
```

### 3.3 Instructions claires

**Bon** :
```
Réponds uniquement avec un JSON valide, sans texte supplémentaire.
```

**Mauvais** :
```
Tu peux répondre avec du JSON ou autre chose, c'est comme tu veux.
```

### 3.4 Catégorisation des fonctions

**Stratégie** : Grouper les fonctions par catégorie et créer des templates par catégorie.

**Catégories possibles** :
- **Math** : addition, soustraction, multiplication, etc.
- **String** : reverse, uppercase, lowercase, etc.
- **Date/Time** : get_current_date, format_date, etc.
- **Logic** : comparison, boolean operations, etc.

**Avantage** : Permet d'adapter le prompt selon le type de question.

---

## 4. Construction du Prompt

### 4.1 Analyse des fonctions disponibles

**Étape 1** : Lire `function_definitions.json`

```python
import json

with open('input/function_definitions.json', 'r') as f:
    functions = json.load(f)

# Analyser les fonctions
for fn_name, fn_def in functions.items():
    print(f"{fn_name}:")
    print(f"  Args: {fn_def.get('args', {})}")
    print(f"  Return: {fn_def.get('return_type', 'unknown')}")
```

**Étape 2** : Catégoriser

```python
categories = {
    'math': ['fn_add_numbers', 'fn_multiply', ...],
    'string': ['fn_reverse_string', 'fn_uppercase', ...],
    'date': ['fn_get_current_date', ...],
    ...
}
```

### 4.2 Sélection des exemples

**Critères** :
- **Variété** : Couvrir différents types de fonctions
- **Simplicité** : Exemples clairs et non ambigus
- **Représentativité** : Refléter les cas d'usage réels

**Exemple de sélection** :
```python
def select_examples(functions: dict, n_examples: int = 3) -> list:
    """Sélectionne des exemples représentatifs."""
    examples = []
    
    # Un exemple math
    examples.append({
        "question": "Quelle est la somme de 2 et 3 ?",
        "response": {"fn_name": "fn_add_numbers", "args": {"a": 2.0, "b": 3.0}}
    })
    
    # Un exemple string
    examples.append({
        "question": "Inverse 'hello'",
        "response": {"fn_name": "fn_reverse_string", "args": {"s": "hello"}}
    })
    
    # Un exemple date (si disponible)
    if "fn_get_current_date" in functions:
        examples.append({
            "question": "Quelle est la date aujourd'hui ?",
            "response": {"fn_name": "fn_get_current_date", "args": {}}
        })
    
    return examples[:n_examples]
```

### 4.3 Construction finale

```python
def build_function_calling_prompt(
    question: str,
    function_definitions: dict,
    examples: list[dict] = None
) -> str:
    """
    Construit un prompt optimisé pour le function calling.
    """
    if examples is None:
        examples = select_examples(function_definitions)
    
    prompt = """Tu es un assistant qui convertit des questions en appels de fonctions.

Format de réponse attendu (JSON uniquement) :
{
    "fn_name": "nom_de_la_fonction",
    "args": {
        "argument1": valeur1,
        "argument2": valeur2
    }
}

Exemples :

"""
    
    for ex in examples:
        prompt += f'Question: "{ex["question"]}"\n'
        prompt += f'Réponse: {json.dumps(ex["response"], ensure_ascii=False)}\n\n'
    
    prompt += f'Question: "{question}"\n'
    prompt += "Réponse:"
    
    return prompt
```

---

## 5. Gestion des Erreurs et Parsing

### 5.1 Problèmes courants

**Problème 1** : Le LLM génère du texte avant/après le JSON
```
Voici la réponse : {"fn_name": "test", "args": {}}
```

**Solution** : Parsing flexible qui extrait le JSON même s'il est entouré de texte.

**Problème 2** : JSON invalide
```
{"fn_name": "test", "args": {  // Virgule manquante
```

**Solution** : Correction automatique des erreurs JSON courantes.

**Problème 3** : Clés manquantes ou incorrectes
```
{"function": "test", "arguments": {}}  // Mauvais noms de clés
```

**Solution** : Validation stricte avec Pydantic.

### 5.2 Parsing flexible

```python
import json
import re

def extract_json_from_text(text: str) -> dict:
    """
    Extrait un JSON depuis un texte, même s'il est entouré de texte.
    """
    # Chercher un bloc JSON
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            # Essayer de parser
            return json.loads(match)
        except json.JSONDecodeError:
            # Essayer avec correction
            corrected = fix_json_errors(match)
            try:
                return json.loads(corrected)
            except:
                continue
    
    raise ValueError("Aucun JSON valide trouvé dans le texte")


def fix_json_errors(json_str: str) -> str:
    """Corrige les erreurs JSON courantes."""
    # Supprimer les commentaires
    json_str = re.sub(r'//.*', '', json_str)
    
    # Ajouter des virgules manquantes
    json_str = re.sub(r'}\s*{', '},{', json_str)
    
    # Corriger les guillemets simples
    json_str = re.sub(r"'([^']*)'", r'"\1"', json_str)
    
    return json_str
```

---

## 6. Validation avec Pydantic

### 6.1 Modèles Pydantic

```python
from pydantic import BaseModel, Field
from typing import Dict, Any

class FunctionCallArgs(BaseModel):
    """Arguments d'un appel de fonction."""
    # Structure dynamique selon la fonction
    pass

class FunctionCallResult(BaseModel):
    """Résultat d'un appel de fonction."""
    fn_name: str = Field(..., description="Nom de la fonction")
    args: Dict[str, Any] = Field(..., description="Arguments de la fonction")
    
    @validator('fn_name')
    def validate_fn_name(cls, v, values):
        """Vérifie que la fonction existe."""
        # À implémenter : vérifier dans function_definitions
        return v
```

### 6.2 Validation complète

```python
def validate_function_call(
    parsed_json: dict,
    function_definitions: dict
) -> tuple[bool, str]:
    """
    Valide un appel de fonction.
    
    Returns:
        (is_valid, error_message)
    """
    # Vérifier que fn_name existe
    if 'fn_name' not in parsed_json:
        return False, "Clé 'fn_name' manquante"
    
    fn_name = parsed_json['fn_name']
    if fn_name not in function_definitions:
        return False, f"Fonction '{fn_name}' inconnue"
    
    # Vérifier les arguments
    if 'args' not in parsed_json:
        return False, "Clé 'args' manquante"
    
    args = parsed_json['args']
    expected_args = function_definitions[fn_name].get('args', {})
    
    # Vérifier que tous les arguments requis sont présents
    for arg_name, arg_type in expected_args.items():
        if arg_name not in args:
            return False, f"Argument '{arg_name}' manquant"
        
        # Vérifier le type
        if not check_type(args[arg_name], arg_type):
            return False, f"Type incorrect pour '{arg_name}'"
    
    return True, "OK"
```

---

## 7. Stratégies d'Optimisation

### 7.1 Itération sur les prompts

**Processus** :
1. Créer un prompt initial
2. Tester sur 10-20 questions
3. Analyser les erreurs
4. Ajuster le prompt
5. Réitérer

### 7.2 A/B Testing

Tester différentes variantes :
- Nombre d'exemples (2 vs 3 vs 5)
- Format des exemples (compact vs détaillé)
- Instructions (strictes vs flexibles)

### 7.3 Logging et analyse

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_prompt_performance(prompt: str, question: str, result: dict, is_valid: bool):
    """Log les performances du prompt."""
    logger.info(f"Question: {question}")
    logger.info(f"Résultat: {result}")
    logger.info(f"Valide: {is_valid}")
    if not is_valid:
        logger.warning(f"Erreur de validation")
```

---

## 8. Exemple Complet

### 8.1 Module Prompt Engineering

```python
"""Module de prompt engineering pour function calling."""

import json
from typing import Dict, List, Optional

class PromptEngineer:
    """Construit des prompts optimisés pour le function calling."""
    
    def __init__(self, function_definitions: Dict):
        """Initialise avec les définitions de fonctions."""
        self.function_definitions = function_definitions
        self.examples = self._select_examples()
    
    def _select_examples(self) -> List[Dict]:
        """Sélectionne des exemples représentatifs."""
        # [Implémentation]
        return [
            {
                "question": "Quelle est la somme de 5 et 3 ?",
                "response": {"fn_name": "fn_add_numbers", "args": {"a": 5.0, "b": 3.0}}
            },
            {
                "question": "Inverse la chaîne 'hello'",
                "response": {"fn_name": "fn_reverse_string", "args": {"s": "hello"}}
            }
        ]
    
    def build_prompt(self, question: str) -> str:
        """Construit un prompt pour une question."""
        prompt = """Tu es un assistant qui convertit des questions en appels de fonctions.

Format de réponse (JSON uniquement) :
{
    "fn_name": "nom_de_la_fonction",
    "args": {
        "argument": valeur
    }
}

Exemples :

"""
        
        for ex in self.examples:
            prompt += f'Question: "{ex["question"]}"\n'
            prompt += f'Réponse: {json.dumps(ex["response"], ensure_ascii=False)}\n\n'
        
        prompt += f'Question: "{question}"\n'
        prompt += "Réponse:"
        
        return prompt
```

---

## 9. Ressources Complémentaires

### 9.1 Documentation

- **FR** : [Blog du Modérateur – Prompt engineering : guide complet](https://www.blogdumoderateur.com/prompt-engineering-guide/)
- **FR** : [HES-SO – Parler à l'IA : l'essentiel du prompt engineering](https://www.hes-so.ch/formation-devpro/parler-a-lia-ou-lessentiel-du-prompt-engineering)
- **EN** : [Prompt Engineering Guide](https://www.promptingguide.ai/)
- **EN** : [Anthropic – Prompt design best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-design)

### 9.2 Vidéos

- **FR** : [ScienceEtonnante – Les prompts pour l'IA](https://www.youtube.com/watch?v=...) (à rechercher)
- **EN** : [Andrej Karpathy – Prompt Engineering](https://www.youtube.com/watch?v=...)

---

## Conclusion

Vous devriez maintenant comprendre :
- ✅ Comment structurer un prompt efficace pour le function calling
- ✅ L'importance du few-shot learning
- ✅ Comment parser et valider les réponses
- ✅ Comment itérer et optimiser les prompts

**Prochaine étape** : Module M3 - Validation avec Pydantic
