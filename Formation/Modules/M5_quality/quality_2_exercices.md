# M5 – Exercices Détaillés : Robustesse, QA & Tests

## Instructions générales

- Documenter vos résultats dans `Formation/Notes/m5_exercices.md`

---

## Exercice 1 – Matrice d'erreurs

### Objectif
Documenter tous les scénarios d'erreur possibles.

### Étapes détaillées

1. **Créer `Doc/error_matrix.md`**
   
   Documenter au moins 10 scénarios avec :
   - Zone d'erreur
   - Type d'erreur
   - Gravité
   - Message d'erreur
   - Action à prendre

### Livrable

- `Doc/error_matrix.md` : Matrice complète

---

## Exercice 2 – Gestion d'exceptions

### Objectif
Ajouter des try/except dans tous les modules.

### Étapes détaillées

1. **Créer un décorateur `log_exceptions`**
   
   ```python
   def log_exceptions(func):
       """Décorateur qui loggue les exceptions."""
       # [À COMPLÉTER]
   ```

2. **Appliquer dans tous les modules**

### Livrable

- Décorateur fonctionnel
- Modules protégés

---

## Exercice 3 – Tests unitaires

### Objectif
Créer des tests pour chaque module.

### Étapes détaillées

1. **Créer `tests/test_tokenizer.py`**
2. **Créer `tests/test_validator.py`**
3. **Créer `tests/test_parser.py`**

### Livrable

- Tests unitaires complets
- Couverture > 80%

---

## Exercice 4 – Tests d'intégration

### Objectif
Tester le pipeline complet.

### Étapes détaillées

1. **Créer un mock du LLM**
2. **Tester le pipeline end-to-end**
3. **Vérifier les fichiers de sortie**

### Livrable

- Tests d'intégration
- Mock fonctionnel

---

## Exercice 5 – CI locale

### Objectif
Automatiser lint + test.

### Étapes détaillées

1. **Ajouter `make ci` au Makefile**
2. **Documenter dans `Formation/Notes/ci_local.md`**

### Livrable

- `make ci` fonctionnel
- Documentation

---

## Validation finale

### Checklist

- [ ] Matrice d'erreurs complète
- [ ] Gestion d'exceptions partout
- [ ] Tests unitaires créés
- [ ] Tests d'intégration passent
- [ ] CI locale fonctionnelle
