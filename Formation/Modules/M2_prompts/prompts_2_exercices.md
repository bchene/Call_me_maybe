# M2 – Exercices Détaillés : Function Calling & Prompt Engineering

## Instructions générales

- Chaque exercice doit être complété dans l'ordre
- Utiliser les templates fournis dans `M2_prompts/templates/`
- Comparer vos résultats avec les exemples dans `M2_prompts/exemples/`
- Documenter vos résultats dans `Formation/Notes/m2_exercices.md`

---

## Exercice 1 – Cartographie des fonctions

### Objectif
Analyser et catégoriser toutes les fonctions disponibles dans `function_definitions.json`.

### Étapes détaillées

1. **Lire le fichier de définitions**
   
   Créer `scripts/analyze_functions.py` :
   
   ```python
   """Analyse les fonctions disponibles."""
   
   import json
   from pathlib import Path
   from typing import Dict, List
   
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
           # Analyser la fonction
           args = fn_def.get('args', {})
           return_type = fn_def.get('return_type', 'unknown')
           
           # Catégoriser
           category = categorize_function(fn_name, args, return_type)
           categories[category].append({
               'name': fn_name,
               'args': args,
               'return_type': return_type
           })
       
       return categories
   
   def categorize_function(fn_name: str, args: Dict, return_type: str) -> str:
       """Catégorise une fonction."""
       fn_lower = fn_name.lower()
       
       if any(word in fn_lower for word in ['add', 'multiply', 'divide', 'subtract', 'sum', 'math']):
           return 'math'
       elif any(word in fn_lower for word in ['string', 'reverse', 'upper', 'lower', 'concat']):
           return 'string'
       elif any(word in fn_lower for word in ['date', 'time', 'day', 'month', 'year']):
           return 'date'
       elif any(word in fn_lower for word in ['compare', 'equal', 'greater', 'less', 'and', 'or']):
           return 'logic'
       else:
           return 'misc'
   
   if __name__ == '__main__':
       categories = analyze_functions('Dev/input/function_definitions.json')
       
       # Générer le rapport
       report = "# Catalogue des Fonctions\n\n"
       for category, funcs in categories.items():
           report += f"## {category.upper()}\n\n"
           for func in funcs:
               report += f"### {func['name']}\n"
               report += f"- Arguments: {func['args']}\n"
               report += f"- Return: {func['return_type']}\n\n"
       
       with open('Formation/Notes/catalogue_fonctions.md', 'w') as f:
           f.write(report)
   ```

2. **Créer le tableau récapitulatif**
   
   Créer `Formation/Notes/catalogue_fonctions.md` avec un tableau :
   
   ```markdown
   # Catalogue des Fonctions
   
   | fn_name | Catégorie | Arguments | Return Type | Remarques |
   |---------|-----------|-----------|-------------|-----------|
   | fn_add_numbers | math | a: float, b: float | float | Addition simple |
   | fn_reverse_string | string | s: str | str | Inverse une chaîne |
   ...
   ```

### Livrable

- `scripts/analyze_functions.py` : Script d'analyse
- `Formation/Notes/catalogue_fonctions.md` : Catalogue complet avec tableau

---

## Exercice 2 – Création de templates de prompts

### Objectif
Créer des templates de prompts par catégorie de fonctions.

### Étapes détaillées

1. **Créer les templates**
   
   Pour chaque catégorie, créer un fichier dans `M2_prompts/templates/` :
   
   **`math_prompt.md`** :
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
   
   Créer de même : `string_prompt.md`, `date_prompt.md`, `logic_prompt.md`, `misc_prompt.md`

2. **Créer un générateur de prompts**
   
   Créer `Dev/src/prompt_engineering.py` :
   
   ```python
   """Génération de prompts pour function calling."""
   
   import json
   from pathlib import Path
   from typing import Dict, List
   
   class PromptTemplate:
       """Template de prompt par catégorie."""
       
       def __init__(self, category: str, examples: List[Dict]):
           self.category = category
           self.examples = examples
       
       def build(self, question: str) -> str:
           """Construit le prompt."""
           # [À COMPLÉTER]
           pass
   
   class PromptEngineer:
       """Génère des prompts optimisés."""
       
       def __init__(self, function_definitions: Dict):
           self.function_definitions = function_definitions
           self.templates = self._load_templates()
       
       def _load_templates(self) -> Dict[str, PromptTemplate]:
           """Charge les templates par catégorie."""
           # [À COMPLÉTER]
           pass
       
       def build_prompt(self, question: str, category: str = None) -> str:
           """Construit un prompt pour une question."""
           # [À COMPLÉTER]
           pass
   ```

### Livrable

- 5 fichiers templates dans `M2_prompts/templates/`
- `Dev/src/prompt_engineering.py` : Module de génération de prompts

---

## Exercice 3 – Batterie de tests avec LLM externe

### Objectif
Tester les prompts avec un LLM accessible (ChatGPT, Claude, etc.) pour valider leur efficacité.

### Étapes détaillées

1. **Préparer les questions de test**
   
   Créer `M2_prompts/tests/test_questions.json` :
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
       ...
   ]
   ```

2. **Créer un script de test**
   
   Créer `scripts/test_prompts_external.py` :
   ```python
   """Test des prompts avec un LLM externe."""
   
   import json
   import openai  # Ou autre API
   from src.prompt_engineering import PromptEngineer
   
   def test_prompt_with_external_llm(prompt: str, api_key: str) -> dict:
       """Teste un prompt avec un LLM externe."""
       # [À COMPLÉTER] : Appel à l'API
       pass
   
   def run_test_suite():
       """Exécute la suite de tests."""
       # [À COMPLÉTER]
       pass
   ```

3. **Analyser les résultats**
   
   Créer `Formation/Notes/m2_resultats_tests.md` avec :
   - Pour chaque question : JSON valide ? fn_name correct ? args corrects ?
   - Taux de succès par catégorie
   - Erreurs communes identifiées

### Livrable

- `M2_prompts/tests/test_questions.json` : Questions de test
- `scripts/test_prompts_external.py` : Script de test
- `Formation/Notes/m2_resultats_tests.md` : Analyse des résultats

---

## Exercice 4 – Optimisation des prompts

### Objectif
Identifier les prompts qui échouent et les améliorer.

### Étapes détaillées

1. **Analyser les échecs**
   
   Identifier les patterns d'erreurs :
   - JSON invalide
   - fn_name incorrect
   - Arguments manquants ou incorrects
   - Texte supplémentaire

2. **Créer des variantes améliorées**
   
   Pour chaque problème identifié, créer une variante :
   
   **Problème** : Le LLM ajoute du texte
   **Solution** : Renforcer l'instruction "Réponds UNIQUEMENT avec le JSON"

3. **Retester et comparer**
   
   Créer `Formation/Notes/m2_optimisation.md` avec :
   - Problèmes identifiés
   - Solutions appliquées
   - Résultats avant/après

### Livrable

- `Formation/Notes/m2_optimisation.md` : Document d'optimisation
- Templates améliorés dans `M2_prompts/templates/`

---

## Exercice 5 – Intégration avec le tokenizer

### Objectif
Intégrer la génération de prompts avec le système de tokenisation.

### Étapes détaillées

1. **Créer le module complet**
   
   Intégrer `PromptEngineer` avec `Tokenizer` pour :
   - Construire le prompt
   - Tokeniser le prompt
   - Générer avec le LLM
   - Parser la réponse

2. **Tester le pipeline complet**
   
   Créer `scripts/test_full_pipeline.py` :
   ```python
   """Test du pipeline complet."""
   
   from src.prompt_engineering import PromptEngineer
   from src.tokenizer import Tokenizer
   from src.llm_interaction import LLMInteraction
   from src.parser import Parser
   
   def test_full_pipeline(question: str):
       """Test le pipeline complet."""
       # [À COMPLÉTER]
       pass
   ```

### Livrable

- Pipeline complet fonctionnel
- Tests de validation

---

## Validation finale

### Checklist

- [ ] Fonctions analysées et catégorisées
- [ ] Templates créés pour chaque catégorie
- [ ] Tests effectués avec LLM externe
- [ ] Prompts optimisés
- [ ] Pipeline complet fonctionnel
