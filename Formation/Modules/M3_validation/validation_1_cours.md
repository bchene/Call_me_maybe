# M3 – Cours Détaillé : Validation JSON & Pydantic

## 1. Introduction à Pydantic

### 1.1 Pourquoi Pydantic ?

**Pydantic** est une bibliothèque Python qui valide les données en utilisant des annotations de type Python.

**Avantages** :
- **Validation déclarative** : Définir le schéma une fois, validation automatique
- **Conversion automatique des types** : `"42"` → `42.0` automatiquement
- **Messages d'erreur clairs** : `e.errors()` donne des détails précis
- **Intégration facile** : Compatible avec FastAPI, JSON, etc.

### 1.2 Installation

```bash
uv add pydantic
# Ou dans pyproject.toml
dependencies = ["pydantic>=2.0.0"]
```

### 1.3 Exemple basique

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int
    email: str

# Validation automatique
user = User(name="Alice", age=30, email="alice@example.com")
print(user.age)  # 30 (int)

# Conversion automatique
user2 = User(name="Bob", age="25", email="bob@example.com")
print(user2.age)  # 25 (int, converti depuis str)

# Erreur de validation
try:
    user3 = User(name="Charlie", age="not_a_number", email="charlie@example.com")
except ValidationError as e:
    print(e.errors())
    # [{'type': 'int_parsing', 'loc': ('age',), 'msg': 'Input should be a valid integer'}]
```

---

## 2. Modèles Pydantic pour le Projet

### 2.1 Structure des données

**Données à valider** :
1. **Function Definitions** : Définitions des fonctions disponibles
2. **Function Call Results** : Résultats d'appels de fonctions (sortie du LLM)

### 2.2 Modèle FunctionDefinition

```python
from pydantic import BaseModel, Field
from typing import Dict, Any

class FunctionArgument(BaseModel):
    """Définition d'un argument de fonction."""
    name: str
    type: str  # "float", "int", "str", "bool", etc.

class FunctionDefinition(BaseModel):
    """Définition complète d'une fonction."""
    name: str
    args: Dict[str, str] = Field(..., description="Arguments: nom -> type")
    return_type: str = Field(..., description="Type de retour")
    
    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> 'FunctionDefinition':
        """Crée depuis un dictionnaire."""
        return cls(
            name=name,
            args=data.get('args', {}),
            return_type=data.get('return_type', 'unknown')
        )
```

### 2.3 Modèle FunctionCallResult

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Any, Optional

class FunctionCallResult(BaseModel):
    """Résultat d'un appel de fonction (sortie du LLM)."""
    prompt: str = Field(..., description="Question originale")
    fn_name: str = Field(..., description="Nom de la fonction")
    args: Dict[str, Any] = Field(..., description="Arguments de la fonction")
    
    @field_validator('fn_name')
    @classmethod
    def validate_fn_name(cls, v: str) -> str:
        """Valide que le nom de fonction n'est pas vide."""
        if not v or not v.strip():
            raise ValueError("fn_name ne peut pas être vide")
        return v.strip()
    
    @model_validator(mode='after')
    def validate_against_definitions(self):
        """Valide contre les définitions de fonctions."""
        # Cette validation sera faite dans le validator externe
        return self
```

---

## 3. Validation Complète

### 3.1 Validator externe

```python
from typing import Dict, Tuple

class FunctionCallValidator:
    """Valide les appels de fonctions contre les définitions."""
    
    def __init__(self, function_definitions: Dict[str, FunctionDefinition]):
        """Initialise avec les définitions de fonctions."""
        self.function_definitions = function_definitions
    
    def validate(self, call_result: FunctionCallResult) -> Tuple[bool, Optional[str]]:
        """
        Valide un appel de fonction.
        
        Returns:
            (is_valid, error_message)
        """
        # Vérifier que la fonction existe
        if call_result.fn_name not in self.function_definitions:
            return False, f"Fonction '{call_result.fn_name}' inconnue"
        
        fn_def = self.function_definitions[call_result.fn_name]
        
        # Vérifier les arguments
        expected_args = fn_def.args
        
        # Vérifier que tous les arguments requis sont présents
        for arg_name, arg_type in expected_args.items():
            if arg_name not in call_result.args:
                return False, f"Argument '{arg_name}' manquant"
            
            # Vérifier le type
            if not self._check_type(call_result.args[arg_name], arg_type):
                return False, f"Type incorrect pour '{arg_name}': attendu {arg_type}"
        
        # Vérifier qu'il n'y a pas d'arguments supplémentaires
        for arg_name in call_result.args:
            if arg_name not in expected_args:
                return False, f"Argument '{arg_name}' non attendu"
        
        return True, None
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Vérifie qu'une valeur correspond au type attendu."""
        type_mapping = {
            'float': (float, int),  # int accepté pour float
            'int': int,
            'str': str,
            'bool': bool,
            'object': dict,
            'list': list,
        }
        
        expected_python_types = type_mapping.get(expected_type.lower(), (object,))
        return isinstance(value, expected_python_types)
```

### 3.2 Conversion automatique des types

```python
from pydantic import field_validator

class FunctionCallResult(BaseModel):
    # ... autres champs ...
    
    @field_validator('args', mode='before')
    @classmethod
    def convert_args_types(cls, v: Dict[str, Any], info) -> Dict[str, Any]:
        """Convertit les types des arguments."""
        # Cette conversion sera faite après validation de fn_name
        # On la fera dans le validator externe
        return v
```

**Conversion dans le validator** :

```python
def convert_and_validate_args(
    args: Dict[str, Any],
    fn_def: FunctionDefinition
) -> Dict[str, Any]:
    """Convertit et valide les arguments."""
    converted = {}
    
    for arg_name, arg_type in fn_def.args.items():
        value = args[arg_name]
        
        # Conversion selon le type
        if arg_type == 'float':
            converted[arg_name] = float(value)
        elif arg_type == 'int':
            converted[arg_name] = int(value)
        elif arg_type == 'str':
            converted[arg_name] = str(value)
        elif arg_type == 'bool':
            converted[arg_name] = bool(value) if isinstance(value, bool) else str(value).lower() == 'true'
        else:
            converted[arg_name] = value
    
    return converted
```

---

## 4. Gestion des Erreurs de Validation

### 4.1 Messages d'erreur structurés

```python
from pydantic import ValidationError

def validate_function_call(
    parsed_json: Dict[str, Any],
    function_definitions: Dict[str, FunctionDefinition]
) -> Tuple[Optional[FunctionCallResult], Optional[str]]:
    """
    Valide un appel de fonction.
    
    Returns:
        (result, error_message)
    """
    try:
        # Créer le modèle Pydantic
        call_result = FunctionCallResult(**parsed_json)
        
        # Valider contre les définitions
        validator = FunctionCallValidator(function_definitions)
        is_valid, error = validator.validate(call_result)
        
        if not is_valid:
            return None, error
        
        # Convertir les types des arguments
        fn_def = function_definitions[call_result.fn_name]
        call_result.args = convert_and_validate_args(call_result.args, fn_def)
        
        return call_result, None
        
    except ValidationError as e:
        errors = e.errors()
        error_msg = "; ".join([f"{err['loc']}: {err['msg']}" for err in errors])
        return None, f"Erreur de validation: {error_msg}"
    except Exception as e:
        return None, f"Erreur inattendue: {str(e)}"
```

### 4.2 Logging des erreurs

```python
import logging

logger = logging.getLogger(__name__)

def validate_with_logging(parsed_json: Dict, functions: Dict) -> Optional[FunctionCallResult]:
    """Valide avec logging des erreurs."""
    result, error = validate_function_call(parsed_json, functions)
    
    if error:
        logger.warning(f"Validation échouée: {error}")
        logger.debug(f"JSON reçu: {parsed_json}")
        return None
    
    logger.info(f"Validation réussie: {result.fn_name}")
    return result
```

---

## 5. Exemple Complet

### 5.1 Module de validation complet

```python
"""Module de validation avec Pydantic."""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError

class FunctionDefinition(BaseModel):
    """Définition d'une fonction."""
    name: str
    args: Dict[str, str]
    return_type: str

class FunctionCallResult(BaseModel):
    """Résultat d'un appel de fonction."""
    prompt: str
    fn_name: str
    args: Dict[str, Any]

class Validator:
    """Valide les appels de fonctions."""
    
    def __init__(self, definitions_path: str):
        """Charge les définitions de fonctions."""
        with open(definitions_path, 'r') as f:
            data = json.load(f)
        
        self.functions = {
            name: FunctionDefinition(name=name, **def_data)
            for name, def_data in data.items()
        }
    
    def validate(self, call_result: FunctionCallResult) -> Tuple[bool, Optional[str]]:
        """Valide un appel de fonction."""
        if call_result.fn_name not in self.functions:
            return False, f"Fonction '{call_result.fn_name}' inconnue"
        
        fn_def = self.functions[call_result.fn_name]
        
        # Vérifier les arguments
        for arg_name, arg_type in fn_def.args.items():
            if arg_name not in call_result.args:
                return False, f"Argument '{arg_name}' manquant"
        
        return True, None

# Utilisation
validator = Validator('Dev/input/function_definitions.json')

parsed = {"prompt": "Test", "fn_name": "fn_add_numbers", "args": {"a": 2.0, "b": 3.0}}
result = FunctionCallResult(**parsed)
is_valid, error = validator.validate(result)
```

---

## 6. Ressources Complémentaires

### 6.1 Documentation

- **FR** : [Real Python (FR) – Pydantic : validez vos données](https://realpython.com/fr/python-pydantic/)
- **EN** : [Pydantic documentation officielle](https://docs.pydantic.dev/latest/)
- **EN** : [FastAPI docs – Using Pydantic](https://fastapi.tiangolo.com/tutorial/body/)

### 6.2 Vidéos

- **EN** : [Corey Schafer – Python Pydantic Tutorial](https://www.youtube.com/watch?v=...) (à rechercher)

---

## Conclusion

Vous devriez maintenant comprendre :
- ✅ Comment utiliser Pydantic pour la validation
- ✅ Comment créer des modèles pour les données du projet
- ✅ Comment valider les appels de fonctions
- ✅ Comment gérer les erreurs de validation

**Prochaine étape** : Module M4 - Interaction LLM & Pipeline Complet
