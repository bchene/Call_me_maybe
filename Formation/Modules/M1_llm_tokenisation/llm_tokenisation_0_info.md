# Module 01 – Fondamentaux LLM & Tokenisation

## Objectifs pédagogiques
- Comprendre le pipeline complet d’un LLM autoregressif.
- Maîtriser les notions de tokens, vocabulaire, `input_ids`, logits.
- Expérimenter la tokenisation fournie avec le projet.

## Plan de travail
1. **Vision générale** : revoir le schéma `Prompt → Tokens → Input_Ids → LLM → Logits → Next_Token`.
2. **Tokenisation théorique** : explorer BPE / WordPiece, rôle du vocabulaire.
3. **Atelier** : écrire un script `tokenizer.py` minimal qui charge le vocabulaire JSON et convertit un texte.
4. **Débrief** : identifier les pièges (tokens inconnus, normalisation, espaces).

## Ressources
- Fiche cours : `Formation/Modules/M1_llm_tokenisation/cours.md`
- Exercices : `Formation/Modules/M1_llm_tokenisation/exercices.md`
- Corrigés : `Formation/Modules/M1_llm_tokenisation/corriges.md`

| Langue | Lien | Notes |
|--------|------|-------|
| FR (texte) | [Interstices – « Comment fonctionnent les modèles de langage ? »](https://interstices.info/comment-fonctionnent-les-modeles-de-langage/) | Explication vulgarisée. |
| FR (vidéo) | [ScienceEtonnante – « GPT-3 : comment ça marche ? »](https://www.youtube.com/watch?v=R5b4wIYNojQ) | Vue d’ensemble. |
| EN (texte) | [Hugging Face – « What are BPE tokens? »](https://huggingface.co/course/en/chapter6/5) | Introduction pratique. |
| EN (vidéo) | [Andrej Karpathy – « Let’s build GPT: from scratch »](https://www.youtube.com/watch?v=wjZofJX0v4M) | Architecture complète. |
| EN (vidéo) | [Andrej Karpathy – « Byte Pair Encoding »](https://www.youtube.com/watch?v=zduSFxRajkE) | Focus BPE. |

## Exercices
1. Tokeniser 3 phrases différentes (fr/en) et lister les tokens obtenus.
2. Reconstituer le texte à partir des `input_ids` (décodage).
3. Documenter les différences observées (accents, ponctuation).

## Livrables
- Notebook ou script démontrant la tokenisation et le décodage.
- Carte mentale des concepts LLM (format libre).

## Critères de réussite
- Capacité à expliquer la différence entre texte, token, `input_id`.
- Script fonctionnel couvrant au moins 5 cas de test (accents, nombres, symboles).

