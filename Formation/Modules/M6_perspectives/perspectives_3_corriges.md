# M6 – Corrigés Complets : Perspectives & Bibliothèques Avancées

## Exercice 1 – Tableau comparatif

### Solution

Voir `Doc/perspectives/bibliotheques_avancees.md` avec la grille complète.

---

## Exercice 2 – Prototype transformers

### Solution

```python
# notebook_prototype.ipynb
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-0.5B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-0.5B")

prompt = "Quelle est la somme de 2 et 3 ?"
inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    inputs.input_ids,
    max_length=100,
    do_sample=True,
    temperature=0.7
)

result = tokenizer.decode(outputs[0])
print(result)
```

**Comparaison** :
- **Maison** : ~100 lignes pour la boucle de génération
- **Transformers** : ~10 lignes, mais moins de contrôle

---

## Exercice 3 – Prompt orchestration

### Solution

```python
# script_langchain.py
from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["examples", "question"],
    template="""Exemples:
{examples}

Question: {question}
Réponse:"""
)

prompt = template.format(
    examples="...",
    question="Quelle est la somme de 2 et 3 ?"
)
```

**Comparaison** :
- **Maison** : F-strings, moins structuré
- **LangChain** : Plus structuré, réutilisable

---

## Exercice 4 – Plan de migration

### Solution

Voir `Doc/perspectives/plan_migration.md` avec les 3 étapes détaillées.

---

## Exercice 5 – Veille

### Solution

Voir `Formation/Notes/veille_function_calling.md` avec les articles résumés.

---

## Conclusion

Tous les modules sont maintenant enrichis et prêts pour la réalisation du projet !
