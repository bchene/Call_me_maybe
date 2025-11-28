# M4 – Cours Détaillé : Interaction LLM & Pipeline Complet

## 1. Vue d'ensemble du Pipeline

### 1.1 Flux complet

```
Question (str)
    ↓
Prompt Engineering (str)
    ↓
Tokenisation (input_ids: np.ndarray)
    ↓
LLM.get_logits_from_input_ids() (logits: np.ndarray)
    ↓
Sélection du token (token_id: int)
    ↓
Ajout à la séquence (input_ids)
    ↓
Décodage (text: str)
    ↓
Critères d'arrêt ? → Oui → Parsing JSON
    ↓                              ↓
    Non ←──────────────────────────┘
    ↓
Validation Pydantic
    ↓
Résultat final (FunctionCallResult)
```

### 1.2 Composants du pipeline

1. **Prompt Engineering** : Construction du prompt
2. **Tokenisation** : Conversion texte → tokens
3. **Génération** : Boucle avec le LLM
4. **Parsing** : Extraction du JSON
5. **Validation** : Vérification avec Pydantic

---

## 2. Interaction avec Small_LLM_Model

### 2.1 API disponible

```python
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()

# Obtenir les logits
input_ids = np.array([1, 2, 3, 4], dtype=np.int32)
logits = model.get_logits_from_input_ids(input_ids)
# logits.shape = (len(input_ids), vocab_size)

# Obtenir le vocabulaire
vocab_path = model.get_path_to_vocabulary_json()
```

### 2.2 Structure des logits

- **Shape** : `(sequence_length, vocab_size)`
- **Valeur** : Probabilités non normalisées (logits)
- **Utilisation** : Prendre `logits[-1]` pour le prochain token

### 2.3 Exemple basique

```python
import numpy as np
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()

# Tokeniser un prompt
prompt = "Bonjour"
input_ids = tokenizer.encode(prompt)  # [1234, 5678]

# Obtenir les logits
logits = model.get_logits_from_input_ids(input_ids)
# logits.shape = (2, vocab_size)

# Sélectionner le prochain token (greedy)
next_token_logits = logits[-1]  # Logits pour le dernier token
next_token_id = np.argmax(next_token_logits)

# Ajouter au contexte
new_input_ids = np.append(input_ids, next_token_id)
```

---

## 3. Boucle de Génération

### 3.1 Algorithme greedy

```python
def generate_greedy(
    prompt: str,
    tokenizer: Tokenizer,
    model: Small_LLM_Model,
    max_length: int = 100
) -> str:
    """Génère du texte avec sélection greedy."""
    # Encoder le prompt
    input_ids = tokenizer.encode(prompt)
    generated_ids = list(input_ids)
    
    # Boucle de génération
    for _ in range(max_length):
        # Obtenir les logits
        current_ids = np.array(generated_ids, dtype=np.int32)
        logits = model.get_logits_from_input_ids(current_ids)
        
        # Sélectionner le prochain token (greedy)
        next_token_id = int(np.argmax(logits[-1]))
        
        # Ajouter à la séquence
        generated_ids.append(next_token_id)
        
        # Décoder pour vérifier les critères d'arrêt
        generated_text = tokenizer.decode(np.array(generated_ids, dtype=np.int32))
        
        # Vérifier critères d'arrêt
        if should_stop(generated_text, len(generated_ids)):
            break
    
    # Décoder le résultat final
    return tokenizer.decode(np.array(generated_ids, dtype=np.int32))
```

### 3.2 Critères d'arrêt

```python
def should_stop(
    text: str,
    current_length: int,
    max_length: int = 100,
    eos_token: str = "<|endoftext|>"
) -> bool:
    """Vérifie si la génération doit s'arrêter."""
    # Longueur maximale
    if current_length >= max_length:
        return True
    
    # Token EOS
    if eos_token in text:
        return True
    
    # JSON complet
    if is_json_complete(text):
        return True
    
    return False
```

---

## 4. Pipeline Complet

### 4.1 Classe Pipeline

```python
"""Pipeline complet de function calling."""

from typing import Optional
from src.prompt_engineering import PromptEngineer
from src.tokenizer import Tokenizer
from src.llm_interaction import LLMGenerator
from src.parser import FlexibleParser
from src.validation import FunctionCallValidator

class FunctionCallingPipeline:
    """Pipeline complet pour le function calling."""
    
    def __init__(
        self,
        function_definitions_path: str,
        vocab_path: str,
        model: Small_LLM_Model
    ):
        """Initialise le pipeline."""
        # Charger les définitions
        with open(function_definitions_path, 'r') as f:
            functions = json.load(f)
        
        # Initialiser les composants
        self.prompt_engineer = PromptEngineer(functions)
        self.tokenizer = Tokenizer(Vocabulary(vocab_path))
        self.generator = LLMGenerator(model, self.tokenizer)
        self.parser = FlexibleParser()
        self.validator = FunctionCallValidator(functions)
    
    def run(self, question: str) -> Optional[FunctionCallResult]:
        """Exécute le pipeline complet."""
        # 1. Construire le prompt
        prompt = self.prompt_engineer.build_prompt(question)
        
        # 2. Générer avec le LLM
        generated_text = self.generator.generate(prompt, max_length=100)
        
        # 3. Parser le JSON
        parsed_json = self.parser.parse(generated_text)
        if not parsed_json:
            return None
        
        # 4. Valider
        try:
            result = FunctionCallResult(prompt=question, **parsed_json)
            is_valid, error = self.validator.validate(result)
            
            if not is_valid:
                return None
            
            return result
        except Exception as e:
            return None
```

### 4.2 Utilisation

```python
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
pipeline = FunctionCallingPipeline(
    function_definitions_path='Dev/input/function_definitions.json',
    vocab_path=model.get_path_to_vocabulary_json(),
    model=model
)

result = pipeline.run("Quelle est la somme de 2 et 3 ?")
if result:
    print(f"Fonction: {result.fn_name}")
    print(f"Arguments: {result.args}")
```

---

## 5. Instrumentation et Logging

### 5.1 Logging des étapes

```python
import logging
import time

logger = logging.getLogger(__name__)

def generate_with_logging(prompt: str, ...) -> str:
    """Génère avec logging détaillé."""
    logger.info(f"Début génération pour: {prompt[:50]}...")
    
    start_time = time.perf_counter()
    input_ids = tokenizer.encode(prompt)
    
    for step in range(max_length):
        step_start = time.perf_counter()
        
        logits = model.get_logits_from_input_ids(input_ids)
        next_token_id = int(np.argmax(logits[-1]))
        
        step_time = time.perf_counter() - step_start
        logger.debug(f"Step {step}: token_id={next_token_id}, time={step_time:.4f}s")
        
        input_ids = np.append(input_ids, next_token_id)
        
        # Vérifier arrêt
        if should_stop(...):
            logger.info(f"Arrêt à l'étape {step}")
            break
    
    total_time = time.perf_counter() - start_time
    logger.info(f"Génération terminée en {total_time:.2f}s")
    
    return tokenizer.decode(input_ids)
```

---

## 6. Gestion des Erreurs

### 6.1 Erreurs possibles

- **Tokenisation** : Token inconnu
- **LLM** : Timeout, erreur de calcul
- **Parsing** : JSON invalide
- **Validation** : Arguments manquants, types incorrects

### 6.2 Stratégie de gestion

```python
def run_with_error_handling(question: str) -> Optional[FunctionCallResult]:
    """Exécute le pipeline avec gestion d'erreurs."""
    try:
        # Prompt engineering
        prompt = prompt_engineer.build_prompt(question)
    except Exception as e:
        logger.error(f"Erreur prompt engineering: {e}")
        return None
    
    try:
        # Génération
        generated = generator.generate(prompt)
    except Exception as e:
        logger.error(f"Erreur génération: {e}")
        return None
    
    try:
        # Parsing
        parsed = parser.parse(generated)
        if not parsed:
            logger.warning("Parsing échoué")
            return None
    except Exception as e:
        logger.error(f"Erreur parsing: {e}")
        return None
    
    try:
        # Validation
        result = FunctionCallResult(**parsed)
        is_valid, error = validator.validate(result)
        if not is_valid:
            logger.warning(f"Validation échouée: {error}")
            return None
        return result
    except Exception as e:
        logger.error(f"Erreur validation: {e}")
        return None
```

---

## 7. Ressources Complémentaires

- **FR** : [NUMA – Comment fonctionnent les grands modèles de langage](https://numa.co/fr/blog/grands-modeles-de-langage-explications)
- **EN** : [Stability AI – Autoregressive decoding explained](https://stability.ai/blog/understanding-autoregressive-text-generation)
- **EN** : [OpenAI Cookbook – Sampling strategies](https://cookbook.openai.com/examples/how_to_sample_from_language_models)

---

## Conclusion

Vous devriez maintenant comprendre :
- ✅ Comment interagir avec Small_LLM_Model
- ✅ Comment implémenter une boucle de génération
- ✅ Comment construire un pipeline complet
- ✅ Comment instrumenter et logger

**Prochaine étape** : Module M5 - Robustesse, QA & Tests
