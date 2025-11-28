# M5 – Cours Détaillé : Robustesse, QA & Tests

## 1. Gestion d'Erreurs

### 1.1 Stratégie générale

**Principe** : Le programme ne doit **jamais planter**. Toutes les erreurs doivent être gérées.

**Niveaux d'erreur** :
- **Bloquant** : Arrêt du programme (ex: fichier d'entrée manquant)
- **Récupérable** : Log + skip (ex: prompt invalide)
- **Warning** : Log + continuer (ex: token inconnu)

### 1.2 Try/Except ciblés

```python
# ❌ Mauvais
try:
    result = process_all()
except:
    pass  # Trop large

# ✅ Bon
try:
    result = parse_json(text)
except json.JSONDecodeError as e:
    logger.warning(f"JSON invalide: {e}")
    return None
except Exception as e:
    logger.error(f"Erreur inattendue: {e}")
    return None
```

### 1.3 Matrice d'erreurs

| Zone | Erreur | Gravité | Action |
|------|--------|---------|--------|
| Input files | Fichier manquant | Bloquant | Stop + message |
| Tokenisation | Token inconnu | Warning | Log + skip |
| LLM | Timeout | Récupérable | Retry (max 2) |
| Validation | Argument manquant | Récupérable | Log + skip |
| Output | JSON invalide | Récupérable | Retenter formatage |

---

## 2. Logging

### 2.1 Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 2.2 Niveaux de log

- **DEBUG** : Détails techniques (tokens, probabilités)
- **INFO** : Progression normale
- **WARNING** : Situation récupérable
- **ERROR** : Nécessite action utilisateur

### 2.3 Exemple

```python
logger.info("Début du traitement")
logger.debug(f"Token sélectionné: {token_id}")
logger.warning(f"Token inconnu, utilisation de UNK")
logger.error(f"Erreur critique: {error}")
```

---

## 3. Tests Unitaires

### 3.1 Structure

```python
import pytest
from src.tokenizer import Tokenizer

def test_tokenizer_encode():
    """Test l'encodage."""
    tokenizer = Tokenizer(vocab)
    result = tokenizer.encode("hello")
    assert len(result) > 0

def test_tokenizer_unknown_token():
    """Test avec token inconnu."""
    tokenizer = Tokenizer(vocab)
    result = tokenizer.encode("unknown_token_xyz")
    # Ne doit pas planter
    assert result is not None
```

### 3.2 Couverture

- **Tokenisation** : Tokens connus/inconnus
- **Parsing** : JSON valide/invalide
- **Validation** : Arguments présents/manquants, types corrects/incorrects

---

## 4. Tests d'Intégration

### 4.1 Mock du LLM

```python
from unittest.mock import Mock

def test_pipeline_with_mock():
    """Test le pipeline avec un mock."""
    mock_llm = Mock()
    mock_llm.get_logits_from_input_ids.return_value = np.array([[0.1, 0.9, 0.2]])
    
    pipeline = Pipeline(mock_llm, ...)
    result = pipeline.run("Test")
    
    assert result is not None
```

### 4.2 Tests de bout en bout

```python
def test_end_to_end():
    """Test complet du pipeline."""
    # Charger les fichiers réels
    result = pipeline.run("Quelle est la somme de 2 et 3 ?")
    
    # Vérifier le résultat
    assert result.fn_name == "fn_add_numbers"
    assert result.args["a"] == 2.0
    assert result.args["b"] == 3.0
```

---

## 5. CI Locale

### 5.1 Makefile

```make
.PHONY: lint test ci

lint:
	uv run flake8 src --max-line-length=100

test:
	uv run pytest tests/ -v

ci: lint test
	@echo "✓ CI locale réussie"
```

### 5.2 Exécution

```bash
make ci
```

---

## 6. Ressources

- **FR** : [OpenClassrooms – Gérer les erreurs en Python](https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/233326-gerer-les-erreurs)
- **EN** : [Real Python – Python Exceptions](https://realpython.com/python-exceptions/)
- **EN** : [Flake8 documentation](https://flake8.pycqa.org/en/latest/)

---

## Conclusion

Vous devriez maintenant comprendre :
- ✅ Comment gérer les erreurs proprement
- ✅ Comment logger efficacement
- ✅ Comment écrire des tests
- ✅ Comment automatiser la qualité

**Prochaine étape** : Module M6 - Perspectives & Bibliothèques Avancées
