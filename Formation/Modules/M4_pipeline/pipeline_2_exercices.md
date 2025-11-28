# M4 – Exercices Détaillés : Interaction LLM & Pipeline Complet

## Instructions générales

- Chaque exercice doit être complété dans l'ordre
- Documenter vos résultats dans `Formation/Notes/m4_exercices.md`

---

## Exercice 1 – Stub du pipeline

### Objectif
Créer la structure de base du pipeline.

### Étapes détaillées

1. **Créer `src/pipeline.py`**
   
   Implémenter une fonction `run_pipeline(prompt: str) -> str` qui :
   - Accepte un prompt
   - Retourne un JSON statique pour l'instant
   - Structure la fonction pour l'intégration future

2. **Tester le stub**
   
   ```python
   result = run_pipeline("Quelle est la somme de 2 et 3 ?")
   assert result == '{"fn_name": "fn_add_numbers", "args": {"a": 2.0, "b": 3.0}}'
   ```

### Livrable

- `Dev/src/pipeline.py` : Stub fonctionnel

---

## Exercice 2 – Implémentation greedy

### Objectif
Implémenter la sélection greedy des tokens.

### Étapes détaillées

1. **Implémenter `greedy_select`**
   
   ```python
   def greedy_select(logits: np.ndarray, allowed_tokens: Optional[List[int]] = None) -> int:
       """Sélectionne le token avec le logit maximum."""
       # [À COMPLÉTER]
   ```

2. **Tester avec différents cas**
   
   - Logits normaux
   - Logits avec tokens autorisés
   - Logits avec un seul token autorisé

### Livrable

- Fonction `greedy_select` fonctionnelle
- Tests unitaires

---

## Exercice 3 – Critères d'arrêt avancés

### Objectif
Implémenter plusieurs critères d'arrêt.

### Étapes détaillées

1. **Implémenter les fonctions**
   
   - `stop_on_eos(ids, eos_id)`
   - `stop_on_length(ids, max_len)`
   - `stop_on_json(text)`

2. **Combiner dans `should_stop`**
   
   La génération s'arrête si **au moins un** critère est satisfait.

### Livrable

- Fonctions de critères d'arrêt
- Fonction `should_stop` combinée

---

## Exercice 4 – Logs

### Objectif
Ajouter du logging détaillé.

### Étapes détaillées

1. **Configurer le logging**
   
   ```python
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   ```

2. **Logger chaque étape**
   
   - Token produit
   - Probabilité
   - Temps par itération

### Livrable

- Logging fonctionnel
- Fichier de log généré

---

## Exercice 5 – Test de bout en bout

### Objectif
Tester le pipeline complet avec mocks.

### Étapes détaillées

1. **Créer un mock du LLM**
   
   ```python
   class MockLLM:
       def get_logits_from_input_ids(self, ids):
           # Retourner des logits déterministes
           pass
   ```

2. **Tester le pipeline**
   
   - Boucle s'arrête correctement
   - Parsing fonctionne
   - Validation réussit

### Livrable

- Mock du LLM
- Tests d'intégration complets

---

## Validation finale

### Checklist

- [ ] Stub du pipeline créé
- [ ] Sélection greedy implémentée
- [ ] Critères d'arrêt fonctionnels
- [ ] Logging ajouté
- [ ] Tests de bout en bout passent
