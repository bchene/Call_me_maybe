#!/bin/bash
# Test : Vérification de l'installation de uv

echo "Test : Vérification de l'installation de uv"
echo "=============================================="

# Vérifier que uv est installé
if command -v uv &> /dev/null; then
    echo "✓ uv est installé"
    uv --version
else
    echo "✗ uv n'est pas installé"
    exit 1
fi

# Vérifier que uv fonctionne
if uv --help &> /dev/null; then
    echo "✓ uv fonctionne correctement"
else
    echo "✗ uv ne fonctionne pas"
    exit 1
fi

echo ""
echo "✓ Tous les tests sont passés"

