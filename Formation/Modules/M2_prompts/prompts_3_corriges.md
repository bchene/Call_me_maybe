# M2 – Corrigés Complets : Function Calling & Prompt Engineering

## Exercice 1 – Cartographie des fonctions

### Solution

**Script complet** (`scripts/analyze_functions.py`) :

```python
#!/usr/bin/env python3
"""Analyse les fonctions disponibles."""

import json
from pathlib import Path
from typing import Dict, List


def categorize_function(fn_name: str, args: Dict, return_type: str) -> str:
    """Catégorise une fonction."""
    fn_lower = fn_name.lower()
    
    if any(word in fn_lower for word in ['add', 'multiply', 'divide', 'subtract', 'sum', 'math', 'calculate']):
        return 'math'
    elif any(word in fn_lower for word in ['string', 'reverse', 'upper', 'lower', 'concat', 'substring']):
        return 'string'
    elif any(word in fn_lower for word in ['date', 'time', 'day', 'month', 'year', 'format_date']):
        return 'date'
    elif any(word in fn_lower for word in ['compare', 'equal', 'greater', 'less', 'and', 'or', 'not']):
        return 'logic'
    else:
        return 'misc'


def analyze_functions(definitions_path: str) -> Dict:
    """Analyse et catégorise les fonctions."""
    with open(definitions_path, 'r') as f:
        functions = json.load(f)
    
    categories = {
        'math': [],
        'string': [],
        'date': [],
        'logic': [],
        'misc': []
    }
    
    for fn_name, fn_def in functions.items():
        args = fn_def.get('args', {})
        return_type = fn_def.get('return_type', 'unknown')
        
        category = categorize_function(fn_name, args, return_type)
        categories[category].append({
            'name': fn_name,
            'args': args,
            'return_type': return_type
        })
    
    return categories


def generate_report(categories: Dict, output_path: str):
    """Génère un rapport markdown."""
    report = "# Catalogue des Fonctions\n\n"
    
    # Tableau récapitulatif
    report += "## Tableau Récapitulatif\n\n"
    report += "| fn_name | Catégorie | Arguments | Return Type | Remarques |\n"
    report += "|---------|-----------|-----------|-------------|-----------|\n"
    
    for category, funcs in categories.items():
        for func in funcs:
            args_str = ", ".join([f"{k}: {v}" for k, v in func['args'].items()])
            report += f"| {func['name']} | {category} | {args_str} | {func['return_type']} | - |\n"
    
    report += "\n## Détails par Catégorie\n\n"
    
    for category, funcs in categories.items():
        if funcs:
            report += f"### {category.upper()}\n\n"
            for func in funcs:
                report += f"#### {func['name']}\n"
                report += f"- **Arguments** : {func['args']}\n"
                report += f"- **Return Type** : {func['return_type']}\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)


if __name__ == '__main__':
    categories = analyze_functions('Dev/input/function_definitions.json')
    generate_report(categories, 'Formation/Notes/catalogue_fonctions.md')
    print(f"Rapport généré : Formation/Notes/catalogue_fonctions.md")
```

---

## Exercice 2 – Création de templates

### Solution

**Template Math** (`M2_prompts/templates/math_prompt.md`) :

```markdown
# Template Prompt - Mathématiques

## Rôle
Tu es un assistant qui convertit des questions mathématiques en appels de fonctions.

## Format attendu
Réponds uniquement avec un JSON valide :
{
    "fn_name": "nom_de_la_fonction",
    "args": {
        "a": nombre1,
        "b": nombre2
    }
}

## Exemples
Question: "Quelle est la somme de 5 et 3 ?"
Réponse: {"fn_name": "fn_add_numbers", "args": {"a": 5.0, "b": 3.0}}

Question: "Multiplie 4 par 7"
Réponse: {"fn_name": "fn_multiply", "args": {"a": 4.0, "b": 7.0}}

## Checklist
- [ ] Format JSON valide
- [ ] fn_name correspond à une fonction math
- [ ] Arguments sont des nombres (float)
- [ ] Pas de texte supplémentaire
```

**Module PromptEngineering** (`Dev/src/prompt_engineering.py`) :

```python
"""Génération de prompts pour function calling."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class PromptEngineer:
    """Génère des prompts optimisés pour le function calling."""
    
    def __init__(self, function_definitions: Dict):
        """Initialise avec les définitions de fonctions."""
        self.function_definitions = function_definitions
        self.examples = self._select_examples()
    
    def _select_examples(self) -> List[Dict]:
        """Sélectionne des exemples représentatifs."""
        return [
            {
                "question": "Quelle est la somme de 5 et 3 ?",
                "response": {"fn_name": "fn_add_numbers", "args": {"a": 5.0, "b": 3.0}}
            },
            {
                "question": "Inverse la chaîne 'hello'",
                "response": {"fn_name": "fn_reverse_string", "args": {"s": "hello"}}
            },
            {
                "question": "Quelle est la date aujourd'hui ?",
                "response": {"fn_name": "fn_get_current_date", "args": {}}
            }
        ]
    
    def build_prompt(self, question: str) -> str:
        """Construit un prompt pour une question."""
        prompt = """Tu es un assistant qui convertit des questions en appels de fonctions structurés.

Réponds uniquement avec un JSON valide au format suivant :
{
    "fn_name": "nom_de_la_fonction",
    "args": {
        "argument1": valeur1,
        "argument2": valeur2
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

## Exercice 3 – Batterie de tests

### Solution

**Questions de test** (`M2_prompts/tests/test_questions.json`) :

```json
[
    {
        "question": "Quelle est la somme de 2 et 3 ?",
        "expected_fn": "fn_add_numbers",
        "expected_args": {"a": 2.0, "b": 3.0},
        "category": "math"
    },
    {
        "question": "Inverse la chaîne 'hello'",
        "expected_fn": "fn_reverse_string",
        "expected_args": {"s": "hello"},
        "category": "string"
    },
    {
        "question": "Quelle est la date aujourd'hui ?",
        "expected_fn": "fn_get_current_date",
        "expected_args": {},
        "category": "date"
    }
]
```

**Script de test** (`scripts/test_prompts_external.py`) :

```python
"""Test des prompts avec un LLM externe (exemple avec OpenAI)."""

import json
import os
from src.prompt_engineering import PromptEngineer

# Note: Ceci est un exemple, adapter selon l'API utilisée
def test_with_openai(prompt: str, api_key: str) -> str:
    """Teste un prompt avec OpenAI (exemple)."""
    # import openai
    # openai.api_key = api_key
    # response = openai.ChatCompletion.create(...)
    # return response.choices[0].message.content
    pass

def run_test_suite():
    """Exécute la suite de tests."""
    with open('M2_prompts/tests/test_questions.json', 'r') as f:
        test_cases = json.load(f)
    
    with open('Dev/input/function_definitions.json', 'r') as f:
        functions = json.load(f)
    
    engineer = PromptEngineer(functions)
    results = []
    
    for test_case in test_cases:
        prompt = engineer.build_prompt(test_case['question'])
        # response = test_with_openai(prompt, os.getenv('OPENAI_API_KEY'))
        # results.append({
        #     'question': test_case['question'],
        #     'expected': test_case,
        #     'actual': parse_response(response),
        #     'is_valid': validate_response(response, test_case)
        # })
    
    # Générer le rapport
    generate_report(results)

if __name__ == '__main__':
    run_test_suite()
```

---

## Exercice 4 – Optimisation

### Solution

**Document d'optimisation** (`Formation/Notes/m2_optimisation.md`) :

```markdown
# Optimisation des Prompts

## Problèmes identifiés

### Problème 1 : Texte supplémentaire
**Symptôme** : Le LLM ajoute "Voici la réponse :" avant le JSON
**Solution** : Renforcer l'instruction "Réponds UNIQUEMENT avec le JSON, sans texte"

### Problème 2 : JSON invalide
**Symptôme** : Virgules manquantes, guillemets incorrects
**Solution** : Parsing flexible avec correction automatique

### Problème 3 : fn_name incorrect
**Symptôme** : Le LLM invente des noms de fonctions
**Solution** : Ajouter un rappel des fonctions disponibles (sans les définitions complètes)

## Améliorations appliquées

1. Instruction renforcée : "Réponds UNIQUEMENT avec un JSON valide, sans texte supplémentaire"
2. Parsing flexible implémenté
3. Validation stricte avec Pydantic

## Résultats

| Version | Taux de succès | Notes |
|---------|----------------|-------|
| V1 (basique) | 60% | Beaucoup d'erreurs |
| V2 (améliorée) | 85% | Meilleur guidage |
| V3 (optimisée) | 95% | Parsing flexible + validation |
```

---

## Exercice 5 – Intégration

### Solution

**Pipeline complet** (`scripts/test_full_pipeline.py`) :

```python
"""Test du pipeline complet."""

from src.prompt_engineering import PromptEngineer
from src.vocabulary import Vocabulary
from src.tokenizer import Tokenizer
from src.llm_interaction import LLMGenerator
from src.parser import FlexibleParser
from src.validator import FunctionCallValidator
from llm_sdk import Small_LLM_Model

def test_full_pipeline(question: str):
    """Test le pipeline complet."""
    # Initialisation
    model = Small_LLM_Model()
    vocab = Vocabulary(model.get_path_to_vocabulary_json())
    tokenizer = Tokenizer(vocab)
    
    with open('Dev/input/function_definitions.json', 'r') as f:
        functions = json.load(f)
    
    engineer = PromptEngineer(functions)
    generator = LLMGenerator(model, tokenizer)
    parser = FlexibleParser()
    validator = FunctionCallValidator(functions)
    
    # 1. Construire le prompt
    prompt = engineer.build_prompt(question)
    print(f"Prompt: {prompt[:100]}...")
    
    # 2. Générer avec le LLM
    generated_text = generator.generate(prompt, max_length=100)
    print(f"Généré: {generated_text}")
    
    # 3. Parser
    parsed = parser.parse(generated_text)
    print(f"Parsé: {parsed}")
    
    # 4. Valider
    is_valid, error = validator.validate(parsed)
    print(f"Valide: {is_valid}")
    if not is_valid:
        print(f"Erreur: {error}")
    
    return parsed if is_valid else None

if __name__ == '__main__':
    test_full_pipeline("Quelle est la somme de 2 et 3 ?")
```

---

## Validation finale

Tous les exercices doivent être complétés et testés avant de passer au module suivant.
