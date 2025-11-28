#!/bin/bash
# Test du tokenizer

echo "Test du tokenizer..."

# Vérifier que le tokenizer existe
if [ ! -f "Dev/src/tokenizer.py" ]; then
    echo "✗ tokenizer.py non trouvé"
    exit 1
fi

# Test d'encodage simple
echo "Test d'encodage..."
uv run python -c "
from src.tokenizer import Tokenizer
from src.vocabulary import Vocabulary
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
vocab = Vocabulary(model.get_path_to_vocabulary_json())
tokenizer = Tokenizer(vocab)

text = 'hello world'
ids = tokenizer.encode(text)
print(f'✓ Encodage réussi: {len(ids)} tokens')

decoded = tokenizer.decode(ids)
print(f'✓ Décodage réussi: {decoded}')
"

if [ $? -eq 0 ]; then
    echo "✓ Tous les tests sont passés"
else
    echo "✗ Certains tests ont échoué"
    exit 1
fi

