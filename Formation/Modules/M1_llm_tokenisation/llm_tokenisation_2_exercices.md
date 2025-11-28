# M1 – Exercices Détaillés : Fondamentaux LLM & Tokenisation

## Instructions générales

- Chaque exercice doit être complété dans l'ordre
- Utiliser les templates fournis dans `M1_llm_tokenisation/templates/`
- Comparer vos résultats avec les exemples dans `M1_llm_tokenisation/exemples/`
- Documenter vos résultats dans `Formation/Notes/m1_exercices.md`

---

## Exercice 1 – Exploration du vocabulaire

### Objectif
Comprendre la structure du vocabulaire JSON et charger les mappings.

### Étapes détaillées

1. **Obtenir le chemin du vocabulaire**
   
   ```python
   from llm_sdk import Small_LLM_Model
   
   model = Small_LLM_Model()
   vocab_path = model.get_path_to_vocabulary_json()
   print(f"Chemin du vocabulaire: {vocab_path}")
   ```

2. **Charger et analyser le vocabulaire**
   
   Créer `scripts/explore_vocab.py` :
   
   ```python
   import json
   from pathlib import Path
   from llm_sdk import Small_LLM_Model
   
   def explore_vocabulary():
       model = Small_LLM_Model()
       vocab_path = model.get_path_to_vocabulary_json()
       
       with open(vocab_path, 'r', encoding='utf-8') as f:
           vocab = json.load(f)
       
       print("=" * 50)
       print("Analyse du vocabulaire")
       print("=" * 50)
       
       # Structure du vocabulaire
       print(f"\nClés disponibles: {list(vocab.keys())}")
       
       # Nombre de tokens
       if 'token_to_id' in vocab:
           token_count = len(vocab['token_to_id'])
           print(f"\nNombre de tokens: {token_count}")
       
       # Afficher les 20 premiers tokens
       if 'token_to_id' in vocab:
           print("\n20 premiers tokens:")
           for i, (token, token_id) in enumerate(list(vocab['token_to_id'].items())[:20]):
               print(f"  {i+1:2d}. '{token}' -> {token_id}")
       
       # Tokens spéciaux
       special_tokens = ['<BOS>', '<EOS>', '<PAD>', '<UNK>', 'BOS', 'EOS', 'PAD', 'UNK']
       print("\nTokens spéciaux trouvés:")
       for special in special_tokens:
           if special in vocab.get('token_to_id', {}):
               print(f"  {special}: {vocab['token_to_id'][special]}")
       
       return vocab
   
   if __name__ == '__main__':
       explore_vocabulary()
   ```

3. **Exécuter le script**
   ```bash
   uv run python scripts/explore_vocab.py > Formation/Notes/vocabulaire_analyse.txt
   ```

### Livrable

- `scripts/explore_vocab.py` : Script d'exploration
- `Formation/Notes/vocabulaire_analyse.txt` : Sortie du script
- `Formation/Notes/vocabulaire.md` : Document récapitulatif avec :
  - Nombre total de tokens
  - Exemples de tokens (20 premiers)
  - Tokens spéciaux identifiés
  - Observations

### Vérification

```bash
# Le script doit s'exécuter sans erreur
uv run python scripts/explore_vocab.py
```

---

## Exercice 2 – Tokenisation manuelle

### Objectif
Comprendre le processus de tokenisation en le faisant manuellement.

### Étapes détaillées

1. **Choisir 3 phrases de test**
   
   Créer `Formation/Notes/m1_phrases_test.txt` :
   ```
   Phrase 1 (FR): "Bonjour, comment allez-vous ?"
   Phrase 2 (EN): "What is the sum of 2 and 3?"
   Phrase 3 (Mixte): "Hello, quelle est la réponse ?"
   ```

2. **Tokenisation manuelle**
   
   Pour chaque phrase :
   - Charger le vocabulaire
   - Identifier les tokens possibles (chercher les plus longs matches)
   - Noter les IDs correspondants
   
   Créer `Formation/Notes/m1_tokenisation_manuelle.md` :
   
   ```markdown
   # Tokenisation manuelle
   
   ## Phrase 1: "Bonjour, comment allez-vous ?"
   
   ### Étape par étape:
   1. Chercher "Bonjour" dans vocab → ID: [À COMPLÉTER]
   2. Chercher "," dans vocab → ID: [À COMPLÉTER]
   3. Chercher " " dans vocab → ID: [À COMPLÉTER]
   4. Chercher "comment" dans vocab → ID: [À COMPLÉTER]
   ...
   
   ### Tokens identifiés:
   - "Bonjour" → [ID]
   - "," → [ID]
   - " " → [ID]
   - "comment" → [ID]
   - ...
   
   ### Liste des IDs:
   [1234, 42, 5678, ...]
   ```

3. **Créer un script de tokenisation simple**
   
   Utiliser le template : `M1_llm_tokenisation/templates/tokenizer_simple.py.template`
   
   ```python
   import json
   import numpy as np
   from llm_sdk import Small_LLM_Model
   
   class SimpleTokenizer:
       def __init__(self):
           model = Small_LLM_Model()
           vocab_path = model.get_path_to_vocabulary_json()
           
           with open(vocab_path, 'r', encoding='utf-8') as f:
               vocab_data = json.load(f)
           
           self.token_to_id = vocab_data.get('token_to_id', {})
           self.id_to_token = {
               int(v): k for k, v in self.token_to_id.items()
           }
       
       def encode(self, text: str) -> np.ndarray:
           """Encode un texte en input_ids."""
           # [À COMPLÉTER]
           pass
       
       def decode(self, token_ids: np.ndarray) -> str:
           """Decode des input_ids en texte."""
           # [À COMPLÉTER]
           pass
   
   # Test
   if __name__ == '__main__':
       tokenizer = SimpleTokenizer()
       
       phrases = [
           "Bonjour, comment allez-vous ?",
           "What is the sum of 2 and 3?",
           "Hello, quelle est la réponse ?"
       ]
       
       for phrase in phrases:
           ids = tokenizer.encode(phrase)
           decoded = tokenizer.decode(ids)
           print(f"Original: {phrase}")
           print(f"IDs: {ids}")
           print(f"Decoded: {decoded}")
           print(f"Match: {phrase == decoded}")
           print()
   ```

4. **Comparer les résultats**
   
   Comparer votre tokenisation manuelle avec le résultat du script.

### Livrable

- `Formation/Notes/m1_phrases_test.txt` : Phrases de test
- `Formation/Notes/m1_tokenisation_manuelle.md` : Tokenisation manuelle détaillée
- `scripts/tokenizer_simple.py` : Script de tokenisation
- `Formation/Notes/m1_comparaison.md` : Comparaison manuelle vs script

### Vérification

Le script doit pouvoir encoder et décoder sans perte d'information (pour les tokens connus).

---

## Exercice 3 – Implémentation complète du tokenizer

### Objectif
Créer un tokenizer complet avec gestion des cas limites.

### Étapes détaillées

1. **Créer la classe Vocabulary**
   
   Créer `Dev/src/vocabulary.py` :
   
   ```python
   """Module de gestion du vocabulaire."""
   
   import json
   from pathlib import Path
   from typing import Dict, Optional
   
   
   class Vocabulary:
       """Gère le vocabulaire token <-> ID."""
       
       def __init__(self, vocab_path: str):
           """Charge le vocabulaire depuis un fichier JSON."""
           # [À COMPLÉTER]
           pass
       
       def encode_token(self, token: str) -> int:
           """Convertit un token en ID."""
           # [À COMPLÉTER]
           pass
       
       def decode_id(self, token_id: int) -> str:
           """Convertit un ID en token."""
           # [À COMPLÉTER]
           pass
       
       def get_unk_token_id(self) -> Optional[int]:
           """Retourne l'ID du token UNK si disponible."""
           # [À COMPLÉTER]
           pass
       
       def get_eos_token_id(self) -> Optional[int]:
           """Retourne l'ID du token EOS si disponible."""
           # [À COMPLÉTER]
           pass
   ```

2. **Créer la classe Tokenizer**
   
   Créer `Dev/src/tokenizer.py` :
   
   ```python
   """Module de tokenisation."""
   
   import numpy as np
   from typing import List
   from .vocabulary import Vocabulary
   
   
   class Tokenizer:
       """Tokenise et décode du texte."""
       
       def __init__(self, vocab: Vocabulary):
           """Initialise le tokenizer avec un vocabulaire."""
           self.vocab = vocab
       
       def encode(self, text: str) -> np.ndarray:
           """
           Encode un texte en input_ids.
           
           Stratégie: longest match first.
           """
           # [À COMPLÉTER]
           pass
       
       def decode(self, token_ids: np.ndarray) -> str:
           """Decode des input_ids en texte."""
           # [À COMPLÉTER]
           pass
   ```

3. **Tests unitaires**
   
   Créer `Dev/tests/test_tokenizer.py` :
   
   ```python
   """Tests pour le tokenizer."""
   
   import pytest
   import numpy as np
   from src.vocabulary import Vocabulary
   from src.tokenizer import Tokenizer
   from llm_sdk import Small_LLM_Model
   
   
   @pytest.fixture
   def vocab():
       """Fixture pour le vocabulaire."""
       model = Small_LLM_Model()
       vocab_path = model.get_path_to_vocabulary_json()
       return Vocabulary(vocab_path)
   
   
   @pytest.fixture
   def tokenizer(vocab):
       """Fixture pour le tokenizer."""
       return Tokenizer(vocab)
   
   
   def test_encode_decode_roundtrip(tokenizer):
       """Test que encode puis decode redonne le texte original."""
       text = "bonjour comment"
       ids = tokenizer.encode(text)
       decoded = tokenizer.decode(ids)
       assert decoded == text
   
   
   def test_empty_string(tokenizer):
       """Test avec une chaîne vide."""
       text = ""
       ids = tokenizer.encode(text)
       assert len(ids) == 0
       decoded = tokenizer.decode(ids)
       assert decoded == ""
   
   
   def test_unknown_tokens(tokenizer):
       """Test avec des tokens inconnus."""
       # [À COMPLÉTER]
       pass
   ```

### Livrable

- `Dev/src/vocabulary.py` : Classe Vocabulary complète
- `Dev/src/tokenizer.py` : Classe Tokenizer complète
- `Dev/tests/test_tokenizer.py` : Tests unitaires
- Tous les tests doivent passer : `uv run pytest Dev/tests/test_tokenizer.py -v`

### Vérification

```bash
# Exécuter les tests
uv run pytest Dev/tests/test_tokenizer.py -v

# Vérifier le linting
make lint
```

---

## Exercice 4 – Analyse des logits et sélection de tokens

### Objectif
Comprendre les logits et implémenter différentes stratégies de sélection.

### Étapes détaillées

1. **Implémenter softmax**
   
   Créer `Dev/src/utils.py` :
   
   ```python
   """Utilitaires pour le traitement des logits."""
   
   import numpy as np
   
   
   def softmax(logits: np.ndarray) -> np.ndarray:
       """
       Convertit les logits en probabilités via softmax.
       
       Args:
           logits: Array de logits (non normalisés)
       
       Returns:
           Array de probabilités (somme = 1.0)
       """
       # [À COMPLÉTER]
       pass
   
   
   def greedy_select(logits: np.ndarray) -> int:
       """
       Sélectionne le token avec le logit maximum (greedy).
       
       Args:
           logits: Array de logits
       
       Returns:
           ID du token sélectionné
       """
       # [À COMPLÉTER]
       pass
   
   
   def sample_with_temperature(
       logits: np.ndarray,
       temperature: float = 1.0
   ) -> int:
       """
       Échantillonne un token selon les probabilités (avec température).
       
       Args:
           logits: Array de logits
           temperature: Contrôle la diversité (1.0 = normal, <1.0 = plus déterministe)
       
       Returns:
           ID du token échantillonné
       """
       # [À COMPLÉTER]
       pass
   ```

2. **Tests et comparaison**
   
   Créer `scripts/compare_selection_strategies.py` :
   
   ```python
   """Compare différentes stratégies de sélection de tokens."""
   
   import numpy as np
   from src.utils import softmax, greedy_select, sample_with_temperature
   
   # Exemple de logits
   logits = np.array([2.5, 1.2, -0.5, 0.8, 3.1])
   
   print("Logits:", logits)
   print()
   
   # Softmax
   probs = softmax(logits)
   print("Probabilités (softmax):", probs)
   print(f"Somme: {np.sum(probs):.6f}")
   print()
   
   # Greedy
   greedy_id = greedy_select(logits)
   print(f"Greedy selection: token ID {greedy_id}")
   print(f"  Probabilité: {probs[greedy_id]:.4f}")
   print()
   
   # Sampling avec différentes températures
   for temp in [0.5, 1.0, 2.0]:
       sampled_id = sample_with_temperature(logits, temperature=temp)
       print(f"Sampling (T={temp}): token ID {sampled_id}")
       print(f"  Probabilité: {probs[sampled_id]:.4f}")
   ```

3. **Tableau comparatif**
   
   Créer `Formation/Notes/m1_comparaison_strategies.md` avec un tableau comparant :
   - Greedy
   - Sampling (T=0.5)
   - Sampling (T=1.0)
   - Sampling (T=2.0)

### Livrable

- `Dev/src/utils.py` : Fonctions utilitaires
- `scripts/compare_selection_strategies.py` : Script de comparaison
- `Formation/Notes/m1_comparaison_strategies.md` : Tableau comparatif

### Vérification

```bash
uv run python scripts/compare_selection_strategies.py
```

---

## Exercice 5 – Critères d'arrêt

### Objectif
Implémenter les différents critères d'arrêt pour la génération.

### Étapes détaillées

1. **Détection de JSON complet**
   
   Créer `Dev/src/stop_criteria.py` :
   
   ```python
   """Critères d'arrêt pour la génération."""
   
   def is_json_complete(text: str) -> bool:
       """
       Vérifie si le JSON est complet (accolades équilibrées).
       
       Args:
           text: Texte à vérifier
       
       Returns:
           True si le JSON est complet
       """
       # [À COMPLÉTER]
       pass
   
   
   def has_eos_token(text: str, eos_token: str = "<EOS>") -> bool:
       """Vérifie si le texte contient un token EOS."""
       # [À COMPLÉTER]
       pass
   
   
   def check_stop_criteria(
       text: str,
       max_length: int,
       current_length: int,
       eos_token: str = "<EOS>"
   ) -> tuple[bool, str]:
       """
       Vérifie tous les critères d'arrêt.
       
       Returns:
           (should_stop, reason)
       """
       # [À COMPLÉTER]
       pass
   ```

2. **Tests**
   
   Créer `Dev/tests/test_stop_criteria.py` :
   
   ```python
   """Tests pour les critères d'arrêt."""
   
   import pytest
   from src.stop_criteria import is_json_complete, check_stop_criteria
   
   
   def test_json_complete():
       """Test avec JSON complet."""
       text = '{"fn_name": "test", "args": {}}'
       assert is_json_complete(text) is True
   
   
   def test_json_incomplete():
       """Test avec JSON incomplet."""
       text = '{"fn_name": "test", "args": {'
       assert is_json_complete(text) is False
   
   
   def test_max_length():
       """Test avec longueur maximale atteinte."""
       text = "a" * 100
       should_stop, reason = check_stop_criteria(
           text, max_length=50, current_length=100
       )
       assert should_stop is True
       assert "max_length" in reason
   ```

3. **Exemples de test**
   
   Créer `Formation/Notes/m1_tests_stop_criteria.md` avec :
   - 3 exemples de JSON complet
   - 3 exemples de JSON incomplet
   - Résultats des tests

### Livrable

- `Dev/src/stop_criteria.py` : Fonctions de critères d'arrêt
- `Dev/tests/test_stop_criteria.py` : Tests unitaires
- `Formation/Notes/m1_tests_stop_criteria.md` : Documentation des tests

### Vérification

```bash
uv run pytest Dev/tests/test_stop_criteria.py -v
```

---

## Exercice 6 – Intégration complète

### Objectif
Créer un script qui génère des tokens en utilisant tout ce qui a été appris.

### Étapes détaillées

1. **Créer un générateur simple**
   
   Créer `scripts/simple_generator.py` :
   
   ```python
   """Générateur simple utilisant le LLM."""
   
   import numpy as np
   from llm_sdk import Small_LLM_Model
   from src.vocabulary import Vocabulary
   from src.tokenizer import Tokenizer
   from src.utils import greedy_select
   from src.stop_criteria import check_stop_criteria
   
   def generate_simple(prompt: str, max_length: int = 50):
       """
       Génère du texte à partir d'un prompt.
       
       Args:
           prompt: Texte de départ
           max_length: Longueur maximale
       
       Returns:
           Texte généré
       """
       # [À COMPLÉTER]
       pass
   
   if __name__ == '__main__':
       prompt = "Bonjour"
       generated = generate_simple(prompt)
       print(f"Prompt: {prompt}")
       print(f"Généré: {generated}")
   ```

2. **Tester avec différents prompts**
   
   Créer `Formation/Notes/m1_tests_generation.md` avec les résultats pour :
   - "Bonjour"
   - "What is"
   - "La somme de"

### Livrable

- `scripts/simple_generator.py` : Générateur complet
- `Formation/Notes/m1_tests_generation.md` : Résultats des tests

---

## Validation finale

### Checklist

- [ ] Vocabulaire exploré et compris
- [ ] Tokenisation manuelle effectuée
- [ ] Tokenizer implémenté et testé
- [ ] Logits compris et stratégies de sélection implémentées
- [ ] Critères d'arrêt implémentés et testés
- [ ] Générateur simple fonctionnel

### Test final

```bash
# Tous les tests doivent passer
uv run pytest Dev/tests/ -v

# Le générateur doit fonctionner
uv run python scripts/simple_generator.py
```

---

## Prochaine étape

Une fois tous les exercices complétés, vous pouvez passer au **Module M2 - Function Calling & Prompt Engineering**.
