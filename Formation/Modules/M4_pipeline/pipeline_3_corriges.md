# M4 – Corrigés Complets : Interaction LLM & Pipeline Complet

## Exercice 1 – Stub du pipeline

### Solution

```python
"""Pipeline de function calling."""

def run_pipeline(prompt: str) -> str:
    """Stub du pipeline."""
    # Pour l'instant, retourner un JSON statique
    return '{"fn_name": "fn_add_numbers", "args": {"a": 2.0, "b": 3.0}}'
```

---

## Exercice 2 – Implémentation greedy

### Solution

```python
import numpy as np
from typing import Optional, List

def greedy_select(logits: np.ndarray, allowed_tokens: Optional[List[int]] = None) -> int:
    """Sélectionne le token avec le logit maximum."""
    if allowed_tokens is not None:
        # Filtrer les logits aux tokens autorisés
        filtered_logits = np.full_like(logits, -np.inf)
        filtered_logits[allowed_tokens] = logits[allowed_tokens]
        return int(np.argmax(filtered_logits))
    else:
        return int(np.argmax(logits))
```

---

## Exercice 3 – Critères d'arrêt

### Solution

```python
def stop_on_eos(ids: np.ndarray, eos_id: int) -> bool:
    """Vérifie si le token EOS est présent."""
    return eos_id in ids

def stop_on_length(ids: np.ndarray, max_len: int) -> bool:
    """Vérifie si la longueur maximale est atteinte."""
    return len(ids) >= max_len

def stop_on_json(text: str) -> bool:
    """Vérifie si le JSON est complet."""
    count = 0
    for char in text:
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
            if count == 0:
                return True
    return False

def should_stop(text: str, ids: np.ndarray, eos_id: int, max_len: int) -> bool:
    """Vérifie si la génération doit s'arrêter."""
    return (
        stop_on_eos(ids, eos_id) or
        stop_on_length(ids, max_len) or
        stop_on_json(text)
    )
```

---

## Exercice 4 – Logs

### Solution

```python
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_with_logging(prompt: str, ...) -> str:
    """Génère avec logging."""
    logger.info(f"Début génération: {prompt[:50]}...")
    
    start_time = time.perf_counter()
    input_ids = tokenizer.encode(prompt)
    
    for step in range(max_length):
        step_start = time.perf_counter()
        
        logits = model.get_logits_from_input_ids(input_ids)
        next_token_id = greedy_select(logits[-1])
        prob = softmax(logits[-1])[next_token_id]
        
        step_time = time.perf_counter() - step_start
        logger.debug(
            f"Step {step}: token_id={next_token_id}, "
            f"prob={prob:.4f}, time={step_time:.4f}s"
        )
        
        input_ids = np.append(input_ids, next_token_id)
        
        if should_stop(...):
            logger.info(f"Arrêt à l'étape {step}")
            break
    
    total_time = time.perf_counter() - start_time
    logger.info(f"Génération terminée en {total_time:.2f}s")
    
    return tokenizer.decode(input_ids)
```

---

## Exercice 5 – Test de bout en bout

### Solution

```python
import numpy as np
from unittest.mock import Mock

class MockLLM:
    """Mock du LLM pour les tests."""
    
    def __init__(self, vocab_size: int = 1000):
        self.vocab_size = vocab_size
        self.call_count = 0
    
    def get_logits_from_input_ids(self, input_ids: np.ndarray) -> np.ndarray:
        """Retourne des logits déterministes."""
        self.call_count += 1
        # Logits déterministes : le token suivant est toujours input_ids[-1] + 1
        logits = np.zeros((len(input_ids), self.vocab_size))
        if len(input_ids) > 0:
            next_id = (input_ids[-1] + 1) % self.vocab_size
            logits[-1, next_id] = 10.0  # Logit élevé pour ce token
        return logits

def test_full_pipeline():
    """Test le pipeline complet."""
    mock_llm = MockLLM()
    # ... initialiser les autres composants ...
    
    result = pipeline.run("Test question")
    
    assert result is not None
    assert result.fn_name is not None
    assert result.args is not None
```
