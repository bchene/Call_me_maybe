# M5 – Corrigés Complets : Robustesse, QA & Tests

## Exercice 1 – Matrice d'erreurs

### Solution

Voir `Doc/error_matrix.md` avec 10+ scénarios documentés.

---

## Exercice 2 – Gestion d'exceptions

### Solution

```python
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_exceptions(func):
    """Décorateur qui loggue les exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Erreur dans {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

# Utilisation
@log_exceptions
def parse_json(text: str):
    """Parse un JSON."""
    return json.loads(text)
```

---

## Exercice 3 – Tests unitaires

### Solution

```python
# tests/test_tokenizer.py
import pytest
from src.tokenizer import Tokenizer

def test_tokenizer_encode():
    tokenizer = Tokenizer(vocab)
    result = tokenizer.encode("hello")
    assert len(result) > 0

def test_tokenizer_unknown_token():
    tokenizer = Tokenizer(vocab)
    result = tokenizer.encode("unknown_token_xyz")
    assert result is not None

# tests/test_validator.py
def test_validator_valid():
    validator = FunctionCallValidator(functions)
    result = FunctionCallResult(...)
    is_valid, error = validator.validate(result)
    assert is_valid

def test_validator_missing_arg():
    result = FunctionCallResult(fn_name="test", args={})
    is_valid, error = validator.validate(result)
    assert not is_valid
```

---

## Exercice 4 – Tests d'intégration

### Solution

Voir M4 corrigés pour le mock du LLM et les tests d'intégration.

---

## Exercice 5 – CI locale

### Solution

```make
.PHONY: ci

ci: lint test
	@echo "✓ CI locale réussie"

lint:
	uv run flake8 src --max-line-length=100

test:
	uv run pytest tests/ -v
```
