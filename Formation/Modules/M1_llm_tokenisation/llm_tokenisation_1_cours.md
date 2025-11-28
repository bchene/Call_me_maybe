# M1 – Cours Détaillé : Fondamentaux LLM & Tokenisation

## 1. Introduction aux LLMs

### 1.1 Qu'est-ce qu'un LLM ?

Un **Large Language Model (LLM)** est un modèle d'IA entraîné sur d'énormes quantités de texte pour prédire le prochain token (mot ou sous-mot) dans une séquence.

### 1.2 Architecture autoregressive

Les LLMs utilisent une architecture **autoregressive** :
- Ils génèrent un token à la fois
- Chaque token est conditionné par tous les tokens précédents
- Le processus est séquentiel : token₁ → token₂ → token₃ → ...

**Exemple** :
```
Prompt: "Bonjour, comment"
Token 1: "allez"
Token 2: "-"
Token 3: "vous"
Token 4: "?"
```

### 1.3 Chaîne de traitement complète

```
Texte (prompt)
    ↓
Tokenisation
    ↓
input_ids (numpy array)
    ↓
Modèle LLM
    ↓
Logits (probabilités brutes)
    ↓
Sélection du token suivant (greedy/sampling)
    ↓
Ajout au contexte
    ↓
Répétition jusqu'à critère d'arrêt
    ↓
Décodage (input_ids → texte)
    ↓
Texte généré
```

---

## 2. Tokenisation : Du Texte aux Nombres

### 2.1 Pourquoi tokeniser ?

Les LLMs ne comprennent pas directement le texte. Ils travaillent avec des **nombres** (input_ids). La tokenisation convertit le texte en nombres.

### 2.2 Méthodes de tokenisation

#### BPE (Byte Pair Encoding)

**Principe** :
1. Commence avec un vocabulaire de caractères individuels
2. Itère en fusionnant les paires les plus fréquentes
3. Crée un vocabulaire de sous-mots optimisé

**Exemple** :
```
Texte original : "bonjour"
Tokens possibles : ["bon", "jour"] ou ["bonj", "our"] selon le vocabulaire
```

**Avantages** :
- Vocabulaire limité (typiquement 30k-50k tokens)
- Gère les mots inconnus (décomposition en sous-mots)
- Efficace en mémoire

#### Autres méthodes (mention)

- **WordPiece** : Similaire à BPE, utilisé par BERT
- **SentencePiece** : Gère directement les espaces et caractères spéciaux
- **Unigram** : Approche probabiliste

### 2.3 Vocabulaire JSON fourni

Le projet fournit un fichier JSON de vocabulaire avec le mapping :

```json
{
  "token_to_id": {
    "bonjour": 1234,
    "comment": 5678,
    " ": 42,
    ...
  },
  "id_to_token": {
    "1234": "bonjour",
    "5678": "comment",
    "42": " ",
    ...
  }
}
```

**Structure typique** :
- Mapping bidirectionnel : `token → id` et `id → token`
- Tokens spéciaux : BOS (begin of sequence), EOS (end of sequence), PAD (padding)
- Tokens de ponctuation, espaces, caractères spéciaux

### 2.4 Chargement du vocabulaire

**Code Python** :

```python
import json
from pathlib import Path
from typing import Dict

class Vocabulary:
    def __init__(self, vocab_path: str):
        """Charge le vocabulaire depuis un fichier JSON."""
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        
        # Construire les mappings
        self.token_to_id: Dict[str, int] = vocab_data.get('token_to_id', {})
        self.id_to_token: Dict[int, str] = vocab_data.get('id_to_token', {})
        
        # Si id_to_token n'existe pas, le construire depuis token_to_id
        if not self.id_to_token:
            self.id_to_token = {v: k for k, v in self.token_to_id.items()}
    
    def encode_token(self, token: str) -> int:
        """Convertit un token en ID."""
        return self.token_to_id.get(token, self.token_to_id.get('<UNK>', 0))
    
    def decode_id(self, token_id: int) -> str:
        """Convertit un ID en token."""
        return self.id_to_token.get(token_id, '<UNK>')
```

### 2.5 Tokenisation d'un texte

**Stratégie** : Tokeniser en cherchant les plus longs tokens disponibles.

**Algorithme** :

```python
def tokenize_text(text: str, vocab: Vocabulary) -> list[int]:
    """
    Tokenise un texte en utilisant le vocabulaire.
    Stratégie : longest match first.
    """
    tokens = []
    i = 0
    
    while i < len(text):
        # Chercher le plus long token possible
        matched = False
        for length in range(len(text) - i, 0, -1):
            candidate = text[i:i+length]
            if candidate in vocab.token_to_id:
                tokens.append(vocab.token_to_id[candidate])
                i += length
                matched = True
                break
        
        if not matched:
            # Token inconnu : utiliser UNK ou caractère par caractère
            if '<UNK>' in vocab.token_to_id:
                tokens.append(vocab.token_to_id['<UNK>'])
            i += 1
    
    return tokens
```

**Exemple** :
```python
text = "bonjour comment allez-vous"
# Tokens : ["bonjour", " ", "comment", " ", "allez", "-", "vous"]
# IDs : [1234, 42, 5678, 42, 9012, 100, 3456]
```

---

## 3. Conversion en input_ids (numpy)

### 3.1 Format numpy.ndarray

Les modèles LLM attendent des tenseurs (arrays numpy) :

```python
import numpy as np

# Convertir une liste d'IDs en numpy array
token_ids = [1234, 42, 5678, 42, 9012]
input_ids = np.array(token_ids, dtype=np.int32)

# Shape : (5,) - unidimensionnel
# Type : int32 (standard pour les IDs de tokens)
```

### 3.2 Gestion des batches (futur)

Pour l'instant, on traite un prompt à la fois. Plus tard, on pourrait avoir des batches :

```python
# Batch de 2 prompts
batch = [
    [1234, 42, 5678],      # Prompt 1
    [9012, 100, 3456, 42]  # Prompt 2
]

# Padding pour avoir la même longueur
max_len = max(len(p) for p in batch)
padded = [p + [0] * (max_len - len(p)) for p in batch]
input_ids = np.array(padded, dtype=np.int32)
# Shape : (2, 4)
```

---

## 4. Interaction avec le LLM

### 4.1 Méthode get_logits_from_input_ids

Le wrapper `Small_LLM_Model` fournit :

```python
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()

# Obtenir les logits pour une séquence
input_ids = np.array([1234, 42, 5678], dtype=np.int32)
logits = model.get_logits_from_input_ids(input_ids)

# logits.shape : (vocab_size,) - un score par token du vocabulaire
# logits[0] : score pour le token ID 0
# logits[1234] : score pour le token ID 1234
```

### 4.2 Comprendre les logits

**Logits** = scores non normalisés (probabilités brutes avant softmax)

```python
# Exemple de logits
logits = np.array([2.5, 1.2, -0.5, 0.8, 3.1])

# Le token avec le logit le plus élevé (3.1) a la plus forte probabilité
# Mais ce ne sont pas encore des probabilités (somme ≠ 1)
```

**Conversion en probabilités** (softmax) :

```python
import numpy as np

def softmax(logits: np.ndarray) -> np.ndarray:
    """Convertit les logits en probabilités."""
    exp_logits = np.exp(logits - np.max(logits))  # Stabilité numérique
    return exp_logits / np.sum(exp_logits)

# Exemple
logits = np.array([2.5, 1.2, -0.5])
probs = softmax(logits)
# probs ≈ [0.73, 0.24, 0.03]  (somme = 1.0)
```

### 4.3 Stratégie de sélection : Greedy

**Greedy** = prendre le token avec le logit le plus élevé (argmax)

```python
def greedy_select(logits: np.ndarray) -> int:
    """Sélectionne le token avec le logit maximum."""
    return int(np.argmax(logits))

# Exemple
logits = np.array([2.5, 1.2, -0.5, 0.8, 3.1])
selected_id = greedy_select(logits)  # = 4 (index du max)
```

**Avantages** :
- Simple et rapide
- Déterministe (même résultat à chaque fois)
- Approprié pour générer du JSON structuré

**Inconvénients** :
- Peut être répétitif
- Moins créatif

### 4.4 Génération token par token

**Boucle de génération** :

```python
def generate_tokens(
    model: Small_LLM_Model,
    initial_prompt_ids: np.ndarray,
    max_length: int = 100,
    eos_token_id: int = 2
) -> list[int]:
    """
    Génère des tokens jusqu'à un critère d'arrêt.
    """
    generated_ids = list(initial_prompt_ids)
    
    for _ in range(max_length):
        # Préparer les input_ids actuels
        current_ids = np.array(generated_ids, dtype=np.int32)
        
        # Obtenir les logits
        logits = model.get_logits_from_input_ids(current_ids)
        
        # Sélectionner le prochain token (greedy)
        next_token_id = greedy_select(logits)
        
        # Ajouter au contexte
        generated_ids.append(next_token_id)
        
        # Vérifier critère d'arrêt
        if next_token_id == eos_token_id:
            break
    
    return generated_ids
```

---

## 5. Décodage : Des Nombres au Texte

### 5.1 Conversion input_ids → texte

**Processus inverse de la tokenisation** :

```python
def decode_ids(token_ids: list[int], vocab: Vocabulary) -> str:
    """Convertit une liste d'IDs en texte."""
    tokens = [vocab.decode_id(token_id) for token_id in token_ids]
    return ''.join(tokens)  # Concaténation directe

# Exemple
token_ids = [1234, 42, 5678, 42, 9012]
# Tokens : ["bonjour", " ", "comment", " ", "allez"]
# Texte : "bonjour comment allez"
```

### 5.2 Gestion des espaces

**Attention** : Certains tokens incluent déjà des espaces, d'autres non.

```python
# Exemple de vocabulaire
vocab = {
    "bonjour": 1234,
    " ": 42,
    "comment": 5678,
    " allez": 9012  # Espace inclus
}

# Décodage
ids = [1234, 42, 5678, 9012]
tokens = ["bonjour", " ", "comment", " allez"]
text = "bonjour comment allez"  # Espace correctement géré
```

---

## 6. Critères d'Arrêt

### 6.1 Token EOS (End of Sequence)

```python
EOS_TOKEN_ID = 2  # À vérifier dans le vocabulaire

if next_token_id == EOS_TOKEN_ID:
    break  # Arrêter la génération
```

### 6.2 Longueur maximale

```python
MAX_LENGTH = 100  # Limite de sécurité

if len(generated_ids) >= MAX_LENGTH:
    break  # Arrêter pour éviter les boucles infinies
```

### 6.3 Détection de JSON complet

```python
def is_json_complete(text: str) -> bool:
    """Vérifie si le JSON est complet (accolades équilibrées)."""
    count = 0
    for char in text:
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
            if count == 0:
                return True  # JSON complet
    return False

# Utilisation
generated_text = decode_ids(generated_ids, vocab)
if is_json_complete(generated_text):
    break  # JSON complet, arrêter
```

---

## 7. Exemple Complet

### 7.1 Code complet d'un tokenizer simple

```python
import json
import numpy as np
from typing import Dict, List
from pathlib import Path

class SimpleTokenizer:
    def __init__(self, vocab_path: str):
        """Initialise le tokenizer avec le vocabulaire."""
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        
        self.token_to_id = vocab_data.get('token_to_id', {})
        self.id_to_token = {
            int(v): k for k, v in self.token_to_id.items()
        }
    
    def encode(self, text: str) -> np.ndarray:
        """Encode un texte en input_ids."""
        tokens = []
        i = 0
        
        while i < len(text):
            matched = False
            for length in range(len(text) - i, 0, -1):
                candidate = text[i:i+length]
                if candidate in self.token_to_id:
                    tokens.append(self.token_to_id[candidate])
                    i += length
                    matched = True
                    break
            
            if not matched:
                # Fallback : caractère par caractère ou UNK
                if '<UNK>' in self.token_to_id:
                    tokens.append(self.token_to_id['<UNK>'])
                i += 1
        
        return np.array(tokens, dtype=np.int32)
    
    def decode(self, token_ids: np.ndarray) -> str:
        """Decode des input_ids en texte."""
        tokens = [self.id_to_token.get(int(id_), '<UNK>') for id_ in token_ids]
        return ''.join(tokens)

# Utilisation
vocab_path = model.get_path_to_vocabulary_json()
tokenizer = SimpleTokenizer(vocab_path)

# Encoder
text = "bonjour comment allez-vous"
input_ids = tokenizer.encode(text)
print(f"Texte: {text}")
print(f"IDs: {input_ids}")

# Décoder
decoded = tokenizer.decode(input_ids)
print(f"Décodé: {decoded}")
```

---

## 8. Points d'Attention

### 8.1 Performance

- **Charger le vocabulaire une seule fois** : Ne pas recharger à chaque tokenisation
- **Cache les mappings** : Construire `id_to_token` une fois au démarrage
- **Optimiser la recherche** : Utiliser des structures de données efficaces (dict)

### 8.2 Gestion des erreurs

- **Token inconnu** : Utiliser `<UNK>` ou caractère par caractère
- **Vocabulaire invalide** : Vérifier le format JSON
- **Décodage incorrect** : Vérifier que les IDs existent dans le vocabulaire

### 8.3 Tests

Toujours tester avec des cas limites :
- Texte vide
- Caractères spéciaux
- Tokens inconnus
- Longues séquences

---

## 9. Ressources Complémentaires

### 9.1 Documentation

- **FR** : [Interstices – Comment fonctionnent les modèles de langage ?](https://interstices.info/comment-fonctionnent-les-modeles-de-langage/)
- **FR** : [Mistral AI – Comprendre le token](https://mistral.ai/fr/blog/tokens-guide)
- **EN** : [Hugging Face – Tokenization](https://huggingface.co/course/en/chapter6/5)
- **EN** : [OpenAI Cookbook – Tokenization](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)

### 9.2 Vidéos

- **FR** : [ScienceEtonnante – Les modèles de langage](https://www.youtube.com/watch?v=...) (à rechercher)
- **EN** : [Andrej Karpathy – Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY)

---

## Conclusion

Vous devriez maintenant comprendre :
- ✅ Comment fonctionnent les LLMs autoregressifs
- ✅ Le processus de tokenisation (texte → tokens → input_ids)
- ✅ Comment interagir avec le modèle (get_logits_from_input_ids)
- ✅ La sélection greedy des tokens
- ✅ Le décodage (input_ids → texte)
- ✅ Les critères d'arrêt

**Prochaine étape** : Module M2 - Function Calling & Prompt Engineering
