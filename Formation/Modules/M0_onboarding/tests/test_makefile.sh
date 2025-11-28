#!/bin/bash
# Test : Vérification du Makefile

echo "Test : Vérification du Makefile"
echo "================================="

cd "$(dirname "$0")/../../.." || exit 1
cd Dev || exit 1

# Vérifier que le Makefile existe
if [ ! -f "Makefile" ]; then
    echo "✗ Makefile n'existe pas"
    exit 1
fi

echo "✓ Makefile existe"

# Vérifier les cibles essentielles
targets=("install" "run" "lint" "clean" "doc")

for target in "${targets[@]}"; do
    if grep -q "^${target}:" Makefile || grep -q "	${target}:" Makefile; then
        echo "✓ Cible 'make ${target}' trouvée"
    else
        echo "✗ Cible 'make ${target}' manquante"
        exit 1
    fi
done

echo ""
echo "✓ Tous les tests sont passés"

