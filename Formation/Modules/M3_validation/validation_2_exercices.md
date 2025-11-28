# M3 – Exercices Détaillés : Validation JSON & Pydantic

## Instructions générales

- Chaque exercice doit être complété dans l'ordre
- Utiliser les templates fournis dans `M3_validation/templates/`
- Documenter vos résultats dans `Formation/Notes/m3_exercices.md`

---

## Exercice 1 – Création des modèles Pydantic

### Objectif
Créer les modèles Pydantic pour les définitions et appels de fonctions.

### Étapes détaillées

1. **Créer le module `src/validation.py`**
   
   Implémenter :
   - `FunctionDefinition` : Modèle pour une définition de fonction
   - `FunctionCallResult` : Modèle pour un appel de fonction
   - `FunctionCallValidator` : Classe de validation

2. **Tester les modèles**
   
   Créer `tests/test_validation.py` avec des tests unitaires :
   - Test de création d'un `FunctionDefinition`
   - Test de validation d'un `FunctionCallResult` valide
   - Test de validation avec arguments manquants
   - Test de validation avec types incorrects

### Livrable

- `Dev/src/validation.py` : Module de validation complet
- `Dev/tests/test_validation.py` : Tests unitaires

---

## Exercice 2 – Chargement et validation des définitions

### Objectif
Charger `function_definitions.json` dans des modèles Pydantic.

### Étapes détaillées

1. **Créer un loader**
   
   ```python
   def load_function_definitions(path: str) -> Dict[str, FunctionDefinition]:
       """Charge les définitions depuis un fichier JSON."""
       # [À COMPLÉTER]
   ```

2. **Valider le chargement**
   
   Vérifier que toutes les définitions sont valides.

### Livrable

- Fonction `load_function_definitions` fonctionnelle
- Tests de chargement

---

## Exercice 3 – Validation des appels de fonctions

### Objectif
Valider un appel de fonction contre sa définition.

### Étapes détaillées

1. **Implémenter la validation**
   
   - Vérifier que `fn_name` existe
   - Vérifier que tous les arguments requis sont présents
   - Vérifier les types des arguments
   - Convertir les types si nécessaire

2. **Gérer les erreurs**
   
   Retourner des messages d'erreur clairs pour chaque cas d'échec.

### Livrable

- `FunctionCallValidator.validate()` fonctionnel
- Tests de validation (succès et échecs)

---

## Exercice 4 – Conversion automatique des types

### Objectif
Convertir automatiquement les types des arguments (ex: `"42"` → `42.0`).

### Étapes détaillées

1. **Implémenter la conversion**
   
   ```python
   def convert_arg_type(value: Any, expected_type: str) -> Any:
       """Convertit une valeur vers le type attendu."""
       # [À COMPLÉTER]
   ```

2. **Tester les conversions**
   
   - `"42"` → `42.0` (float)
   - `"42"` → `42` (int)
   - `"true"` → `True` (bool)

### Livrable

- Fonction de conversion fonctionnelle
- Tests de conversion

---

## Exercice 5 – Intégration avec le parser

### Objectif
Intégrer la validation avec le parser JSON.

### Étapes détaillées

1. **Modifier le parser**
   
   Faire en sorte que le parser retourne un `FunctionCallResult` validé.

2. **Pipeline complet**
   
   ```python
   def parse_and_validate(text: str, functions: Dict) -> Optional[FunctionCallResult]:
       """Parse et valide en une seule étape."""
       # [À COMPLÉTER]
   ```

### Livrable

- Pipeline parse + validate fonctionnel
- Tests d'intégration

---

## Validation finale

### Checklist

- [ ] Modèles Pydantic créés
- [ ] Chargement des définitions fonctionnel
- [ ] Validation des appels fonctionnelle
- [ ] Conversion de types implémentée
- [ ] Intégration avec le parser complète
