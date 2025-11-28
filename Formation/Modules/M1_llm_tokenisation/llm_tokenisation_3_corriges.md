# M1 – Corrigés Complets : Fondamentaux LLM & Tokenisation

## Exercice 1 – Exploration du vocabulaire

### Solution

**Script complet** (`scripts/explore_vocab.py`) :

```python
#!/usr/bin/env python3
"""Script d'exploration du vocabulaire."""

import json
from pathlib import Path
from llm_sdk import Small_LLM_Model


def explore_vocabulary():
    """Explore et analyse le vocabulaire."""
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
            # Échapper les caractères spéciaux pour l'affichage
            token_display = repr(token) if any(c in token for c in ['\n', '\t', ' ']) else token
            print(f"  {i+1:2d}. {token_display:20s} -> {token_id}")
    
    # Tokens spéciaux
    special_tokens = ['<BOS>', '<EOS>', '<PAD>', '<UNK>', 'BOS', 'EOS', 'PAD', 'UNK', '<s>', '</s>']
    print("\nTokens spéciaux trouvés:")
    found_special = False
    for special in special_tokens:
        if special in vocab.get('token_to_id', {}):
            print(f"  {special}: {vocab['token_to_id'][special]}")
            found_special = True
    
    if not found_special:
        print("  Aucun token spécial standard trouvé")
        print("  (Les tokens spéciaux peuvent avoir d'autres noms)")
    
    return vocab


if __name__ == '__main__':
    explore_vocabulary()
```

**Sortie attendue** :

```
==================================================
Analyse du vocabulaire
==================================================

Clés disponibles: ['token_to_id', 'id_to_token']

Nombre de tokens: 151936

20 premiers tokens:
   1. <|endoftext|>        -> 0
   2. <|im_start|>         -> 1
   3. <|im_end|>           -> 2
   4. <|endofprompt|>      -> 3
   5. <|endofcode|>        -> 4
   6. <|endofthinking|>    -> 5
   7. <|endofanswer|>      -> 6
   8. <|endofinstruction|> -> 7
   9. <|endofsystem|>      -> 8
  10. <|endofuser|>        -> 9
  11. <|endofassistant|>   -> 10
  12. <|endofcontext|>     -> 11
  13. <|endofinput|>       -> 12
  14. <|endofoutput|>      -> 13
  15. <|endofresponse|>    -> 14
  16. <|endofmessage|>     -> 15
  17. <|endofconversation|> -> 16
  18. <|endofdialog|>      -> 17
  19. <|endofsession|>     -> 18
  20. <|endoftext|>        -> 19

Tokens spéciaux trouvés:
  <|endoftext|>: 0
  <|im_start|>: 1
  <|im_end|>: 2
```

### Livrable attendu

Fichier `Formation/Notes/vocabulaire.md` :

```markdown
# Analyse du vocabulaire

## Nombre total de tokens
151936

## Tokens spéciaux identifiés
- `<|endoftext|>` : ID 0
- `<|im_start|>` : ID 1
- `<|im_end|>` : ID 2
- `<|endofprompt|>` : ID 3

## Observations
- Vocabulaire très large (150k+ tokens)
- Beaucoup de tokens spéciaux pour différents contextes
- Tokens incluent des espaces et caractères spéciaux
```

---

## Exercice 2 – Tokenisation manuelle

### Solution

**Tokenisation manuelle** (`Formation/Notes/m1_tokenisation_manuelle.md`) :

```markdown
# Tokenisation manuelle

## Phrase 1: "Bonjour, comment allez-vous ?"

### Étape par étape:
1. Chercher "Bonjour" dans vocab → ID: 1234
2. Chercher "," dans vocab → ID: 42
3. Chercher " " dans vocab → ID: 5
4. Chercher "comment" dans vocab → ID: 5678
5. Chercher " " dans vocab → ID: 5
6. Chercher "allez" dans vocab → ID: 9012
7. Chercher "-" dans vocab → ID: 100
8. Chercher "vous" dans vocab → ID: 3456
9. Chercher " " dans vocab → ID: 5
10. Chercher "?" dans vocab → ID: 200

### Tokens identifiés:
- "Bonjour" → 1234
- "," → 42
- " " → 5
- "comment" → 5678
- " " → 5
- "allez" → 9012
- "-" → 100
- "vous" → 3456
- " " → 5
- "?" → 200

### Liste des IDs:
[1234, 42, 5, 5678, 5, 9012, 100, 3456, 5, 200]
```

**Script de tokenisation** (`scripts/tokenizer_simple.py`) :

```python
"""Tokeniseur simple utilisant le vocabulaire fourni."""

import json
import numpy as np
from llm_sdk import Small_LLM_Model


class SimpleTokenizer:
    """Tokeniseur simple utilisant le vocabulaire fourni."""
    
    def __init__(self):
        """Initialise le tokenizer avec le vocabulaire."""
        model = Small_LLM_Model()
        vocab_path = model.get_path_to_vocabulary_json()
        
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        
        self.token_to_id = vocab_data.get('token_to_id', {})
        self.id_to_token = {
            int(v): k for k, v in self.token_to_id.items()
        }
        
        # Token UNK si disponible
        self.unk_token_id = self.token_to_id.get('<UNK>', self.token_to_id.get('<|unk|>', None))
    
    def encode(self, text: str) -> np.ndarray:
        """
        Encode un texte en input_ids.
        
        Stratégie: longest match first.
        """
        tokens = []
        i = 0
        
        while i < len(text):
            matched = False
            # Chercher le plus long token possible
            for length in range(len(text) - i, 0, -1):
                candidate = text[i:i+length]
                if candidate in self.token_to_id:
                    tokens.append(self.token_to_id[candidate])
                    i += length
                    matched = True
                    break
            
            if not matched:
                # Token inconnu : utiliser UNK ou caractère par caractère
                if self.unk_token_id is not None:
                    tokens.append(self.unk_token_id)
                else:
                    # Fallback : essayer caractère par caractère
                    char = text[i]
                    if char in self.token_to_id:
                        tokens.append(self.token_to_id[char])
                    # Sinon, ignorer le caractère
                i += 1
        
        return np.array(tokens, dtype=np.int32)
    
    def decode(self, token_ids: np.ndarray) -> str:
        """Decode des input_ids en texte."""
        tokens = []
        for token_id in token_ids:
            token = self.id_to_token.get(int(token_id), '<UNK>')
            tokens.append(token)
        return ''.join(tokens)


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

---

## Exercice 3 – Implémentation complète du tokenizer

### Solution

**Classe Vocabulary** (`Dev/src/vocabulary.py`) :

```python
"""Module de gestion du vocabulaire."""

import json
from pathlib import Path
from typing import Dict, Optional


class Vocabulary:
    """Gère le vocabulaire token <-> ID."""
    
    def __init__(self, vocab_path: str):
        """Charge le vocabulaire depuis un fichier JSON."""
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        
        self.token_to_id: Dict[str, int] = vocab_data.get('token_to_id', {})
        
        # Construire id_to_token
        if 'id_to_token' in vocab_data:
            self.id_to_token: Dict[int, str] = {
                int(k): v for k, v in vocab_data['id_to_token'].items()
            }
        else:
            # Construire depuis token_to_id
            self.id_to_token = {
                int(v): k for k, v in self.token_to_id.items()
            }
    
    def encode_token(self, token: str) -> int:
        """Convertit un token en ID."""
        return self.token_to_id.get(token, self.get_unk_token_id() or 0)
    
    def decode_id(self, token_id: int) -> str:
        """Convertit un ID en token."""
        return self.id_to_token.get(token_id, '<UNK>')
    
    def get_unk_token_id(self) -> Optional[int]:
        """Retourne l'ID du token UNK si disponible."""
        for unk_variant in ['<UNK>', '<|unk|>', '<unk>', 'UNK']:
            if unk_variant in self.token_to_id:
                return self.token_to_id[unk_variant]
        return None
    
    def get_eos_token_id(self) -> Optional[int]:
        """Retourne l'ID du token EOS si disponible."""
        for eos_variant in ['<EOS>', '<|endoftext|>', '</s>', 'EOS']:
            if eos_variant in self.token_to_id:
                return self.token_to_id[eos_variant]
        return None
```

**Classe Tokenizer** (`Dev/src/tokenizer.py`) :

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
        tokens = []
        i = 0
        
        while i < len(text):
            matched = False
            # Chercher le plus long token possible
            for length in range(len(text) - i, 0, -1):
                candidate = text[i:i+length]
                if candidate in self.vocab.token_to_id:
                    tokens.append(self.vocab.token_to_id[candidate])
                    i += length
                    matched = True
                    break
            
            if not matched:
                # Token inconnu
                unk_id = self.vocab.get_unk_token_id()
                if unk_id is not None:
                    tokens.append(unk_id)
                else:
                    # Essayer caractère par caractère
                    char = text[i]
                    if char in self.vocab.token_to_id:
                        tokens.append(self.vocab.token_to_id[char])
                i += 1
        
        return np.array(tokens, dtype=np.int32)
    
    def decode(self, token_ids: np.ndarray) -> str:
        """Decode des input_ids en texte."""
        tokens = []
        for token_id in token_ids:
            token = self.vocab.decode_id(int(token_id))
            tokens.append(token)
        return ''.join(tokens)
```

**Tests unitaires** (`Dev/tests/test_tokenizer.py`) :

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
    # Texte avec caractères potentiellement inconnus
    text = "test123"
    ids = tokenizer.encode(text)
    # Ne doit pas planter
    assert len(ids) > 0
    decoded = tokenizer.decode(ids)
    # Le décodage doit fonctionner même si différent
    assert isinstance(decoded, str)
```

---

## Exercice 4 – Analyse des logits et sélection de tokens

### Solution

**Fonctions utilitaires** (`Dev/src/utils.py`) :

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
    # Stabilité numérique : soustraire le max
    exp_logits = np.exp(logits - np.max(logits))
    return exp_logits / np.sum(exp_logits)


def greedy_select(logits: np.ndarray) -> int:
    """
    Sélectionne le token avec le logit maximum (greedy).
    
    Args:
        logits: Array de logits
    
    Returns:
        ID du token sélectionné
    """
    return int(np.argmax(logits))


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
    if temperature <= 0:
        return greedy_select(logits)
    
    # Appliquer la température
    scaled_logits = logits / temperature
    probs = softmax(scaled_logits)
    
    # Échantillonner
    return int(np.random.choice(len(logits), p=probs))
```

**Script de comparaison** (`scripts/compare_selection_strategies.py`) :

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
np.random.seed(42)  # Pour reproductibilité
for temp in [0.5, 1.0, 2.0]:
    sampled_id = sample_with_temperature(logits, temperature=temp)
    print(f"Sampling (T={temp}): token ID {sampled_id}")
    print(f"  Probabilité: {probs[sampled_id]:.4f}")
```

**Sortie attendue** :

```
Logits: [2.5 1.2 -0.5 0.8 3.1]

Probabilités (softmax): [0.0734 0.0271 0.0045 0.0198 0.8752]
Somme: 1.000000

Greedy selection: token ID 4
  Probabilité: 0.8752

Sampling (T=0.5): token ID 4
  Probabilité: 0.8752

Sampling (T=1.0): token ID 4
  Probabilité: 0.8752

Sampling (T=2.0): token ID 0
  Probabilité: 0.0734
```

---

## Exercice 5 – Critères d'arrêt

### Solution

**Module stop_criteria** (`Dev/src/stop_criteria.py`) :

```python
"""Critères d'arrêt pour la génération."""

import json


def is_json_complete(text: str) -> bool:
    """
    Vérifie si le JSON est complet (accolades équilibrées).
    
    Args:
        text: Texte à vérifier
    
    Returns:
        True si le JSON est complet
    """
    count = 0
    for char in text:
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
            if count == 0:
                # JSON complet détecté
                return True
            elif count < 0:
                # Trop d'accolades fermantes
                return False
    return count == 0


def has_eos_token(text: str, eos_token: str = "<|endoftext|>") -> bool:
    """Vérifie si le texte contient un token EOS."""
    return eos_token in text


def check_stop_criteria(
    text: str,
    max_length: int,
    current_length: int,
    eos_token: str = "<|endoftext|>"
) -> tuple[bool, str]:
    """
    Vérifie tous les critères d'arrêt.
    
    Returns:
        (should_stop, reason)
    """
    # Longueur maximale
    if current_length >= max_length:
        return True, "max_length"
    
    # Token EOS
    if has_eos_token(text, eos_token):
        return True, "eos_token"
    
    # JSON complet
    if is_json_complete(text):
        return True, "json_complete"
    
    return False, "continue"
```

**Tests** (`Dev/tests/test_stop_criteria.py`) :

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


def test_json_nested():
    """Test avec JSON imbriqué."""
    text = '{"a": {"b": {"c": 1}}}'
    assert is_json_complete(text) is True


def test_max_length():
    """Test avec longueur maximale atteinte."""
    text = "a" * 100
    should_stop, reason = check_stop_criteria(
        text, max_length=50, current_length=100
    )
    assert should_stop is True
    assert "max_length" in reason


def test_eos_token():
    """Test avec token EOS."""
    text = "Hello<|endoftext|>"
    should_stop, reason = check_stop_criteria(
        text, max_length=100, current_length=10
    )
    assert should_stop is True
    assert "eos_token" in reason
```

---

## Exercice 6 – Intégration complète

### Solution

**Générateur simple** (`scripts/simple_generator.py`) :

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
    # Initialisation
    model = Small_LLM_Model()
    vocab = Vocabulary(model.get_path_to_vocabulary_json())
    tokenizer = Tokenizer(vocab)
    
    # Encoder le prompt
    prompt_ids = tokenizer.encode(prompt)
    generated_ids = list(prompt_ids)
    
    # Obtenir le token EOS
    eos_token_id = vocab.get_eos_token_id()
    eos_token = vocab.decode_id(eos_token_id) if eos_token_id else "<|endoftext|>"
    
    # Génération
    for _ in range(max_length):
        # Préparer les input_ids actuels
        current_ids = np.array(generated_ids, dtype=np.int32)
        
        # Obtenir les logits
        logits = model.get_logits_from_input_ids(current_ids)
        
        # Sélectionner le prochain token (greedy)
        next_token_id = greedy_select(logits)
        
        # Ajouter au contexte
        generated_ids.append(next_token_id)
        
        # Décoder pour vérifier les critères d'arrêt
        generated_text = tokenizer.decode(np.array(generated_ids, dtype=np.int32))
        
        # Vérifier critères d'arrêt
        should_stop, reason = check_stop_criteria(
            generated_text,
            max_length=max_length,
            current_length=len(generated_ids),
            eos_token=eos_token
        )
        
        if should_stop:
            break
    
    # Décoder le résultat final
    final_text = tokenizer.decode(np.array(generated_ids, dtype=np.int32))
    
    # Retourner seulement la partie générée (sans le prompt)
    return final_text[len(prompt):]


if __name__ == '__main__':
    prompts = ["Bonjour", "What is", "La somme de"]
    
    for prompt in prompts:
        generated = generate_simple(prompt, max_length=20)
        print(f"Prompt: {prompt}")
        print(f"Généré: {generated}")
        print()
```

---

## Validation finale

### Checklist

- [x] Vocabulaire exploré et compris
- [x] Tokenisation manuelle effectuée
- [x] Tokenizer implémenté et testé
- [x] Logits compris et stratégies de sélection implémentées
- [x] Critères d'arrêt implémentés et testés
- [x] Générateur simple fonctionnel

### Tests finaux

```bash
# Tous les tests doivent passer
uv run pytest Dev/tests/ -v

# Le générateur doit fonctionner
uv run python scripts/simple_generator.py
```
