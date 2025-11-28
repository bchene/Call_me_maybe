# M3 – Corrigés Complets : Validation JSON & Pydantic

## Exercice 1 – Création des modèles Pydantic

### Solution

**Module complet** (`Dev/src/validation.py`) :

```python
"""Module de validation avec Pydantic."""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError, field_validator

class FunctionDefinition(BaseModel):
    """Définition d'une fonction."""
    name: str
    args: Dict[str, str] = Field(..., description="Arguments: nom -> type")
    return_type: str = Field(default="unknown", description="Type de retour")

class FunctionCallResult(BaseModel):
    """Résultat d'un appel de fonction."""
    prompt: str = Field(..., description="Question originale")
    fn_name: str = Field(..., description="Nom de la fonction")
    args: Dict[str, Any] = Field(..., description="Arguments")
    
    @field_validator('fn_name')
    @classmethod
    def validate_fn_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("fn_name ne peut pas être vide")
        return v.strip()

class FunctionCallValidator:
    """Valide les appels de fonctions."""
    
    def __init__(self, function_definitions: Dict[str, FunctionDefinition]):
        self.function_definitions = function_definitions
    
    def validate(self, call_result: FunctionCallResult) -> Tuple[bool, Optional[str]]:
        """Valide un appel de fonction."""
        if call_result.fn_name not in self.function_definitions:
            return False, f"Fonction '{call_result.fn_name}' inconnue"
        
        fn_def = self.function_definitions[call_result.fn_name]
        
        for arg_name, arg_type in fn_def.args.items():
            if arg_name not in call_result.args:
                return False, f"Argument '{arg_name}' manquant"
            
            if not self._check_type(call_result.args[arg_name], arg_type):
                return False, f"Type incorrect pour '{arg_name}'"
        
        return True, None
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Vérifie le type."""
        type_mapping = {
            'float': (float, int),
            'int': int,
            'str': str,
            'bool': bool,
        }
        expected_python_types = type_mapping.get(expected_type.lower(), (object,))
        return isinstance(value, expected_python_types)
```

---

## Exercice 2 – Chargement des définitions

### Solution

```python
def load_function_definitions(path: str) -> Dict[str, FunctionDefinition]:
    """Charge les définitions depuis un fichier JSON."""
    with open(path, 'r') as f:
        data = json.load(f)
    
    functions = {}
    for name, def_data in data.items():
        functions[name] = FunctionDefinition(
            name=name,
            args=def_data.get('args', {}),
            return_type=def_data.get('return_type', 'unknown')
        )
    
    return functions
```

---

## Exercice 3 – Validation complète

### Solution

Voir `FunctionCallValidator.validate()` dans l'exercice 1.

---

## Exercice 4 – Conversion de types

### Solution

```python
def convert_arg_type(value: Any, expected_type: str) -> Any:
    """Convertit une valeur vers le type attendu."""
    if expected_type == 'float':
        return float(value)
    elif expected_type == 'int':
        return int(value)
    elif expected_type == 'str':
        return str(value)
    elif expected_type == 'bool':
        if isinstance(value, bool):
            return value
        return str(value).lower() in ('true', '1', 'yes', 'on')
    return value
```

---

## Exercice 5 – Intégration

### Solution

```python
def parse_and_validate(text: str, functions: Dict) -> Optional[FunctionCallResult]:
    """Parse et valide en une seule étape."""
    from src.parser import FlexibleParser
    
    parser = FlexibleParser()
    parsed = parser.parse(text)
    
    if not parsed:
        return None
    
    try:
        result = FunctionCallResult(**parsed)
        validator = FunctionCallValidator(functions)
        is_valid, error = validator.validate(result)
        
        if not is_valid:
            return None
        
        return result
    except ValidationError:
        return None
```
