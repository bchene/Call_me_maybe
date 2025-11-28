# Décisions de Conception - Call Me Maybe

Ce document enregistre les décisions de conception prises lors de la Phase 2, avec leurs justifications et alternatives considérées.

---

## 1. Architecture Modulaire

### Décision
Adopter une architecture modulaire avec séparation claire des responsabilités.

### Justification
- Facilité de test (chaque module peut être testé indépendamment)
- Maintenabilité (modifications isolées)
- Compréhension claire du système
- Réutilisabilité des composants

### Alternatives Considérées
- Architecture monolithique : Rejetée car moins maintenable
- Architecture orientée objet avec classes : Considérée mais architecture fonctionnelle choisie pour simplicité

---

## 2. Prompt Engineering avec Exemples

### Décision
Utiliser un prompt avec 2-3 exemples représentatifs plutôt que d'inclure toutes les définitions de fonctions.

### Justification
- Respecte la contrainte du sujet (pas de définitions complètes)
- Permet au LLM d'apprendre le pattern sans surcharger le prompt
- Exemples variés couvrent différents cas d'usage
- Prompt plus court = moins de tokens = plus rapide

### Alternatives Considérées
- Inclure toutes les définitions : Interdit par le sujet
- Pas d'exemples : Rejetée car le LLM ne comprendrait pas le format attendu
- Plus d'exemples (5-10) : Rejetée car surcharge le prompt

### Risques
- Le LLM pourrait ne pas généraliser correctement
- Mitigation : Tests itératifs et ajustements du prompt

---

## 3. Génération Token par Token (Greedy)

### Décision
Utiliser une stratégie greedy (token avec probabilité maximale) pour la sélection des tokens.

### Justification
- Simplicité d'implémentation
- Cohérence des résultats (déterministe)
- Approprié pour générer du JSON structuré
- Pas besoin de sampling complexe pour ce cas d'usage

### Alternatives Considérées
- Sampling avec température : Considérée mais complexité inutile
- Beam search : Trop complexe pour ce projet
- Top-k sampling : Pas nécessaire pour JSON structuré

### Risques
- Peut générer des séquences répétitives
- Mitigation : Critères d'arrêt appropriés

---

## 4. Parsing Flexible avec Correction

### Décision
Implémenter un parsing flexible qui peut extraire du JSON même s'il est entouré de texte, avec correction automatique.

### Justification
- Le LLM peut générer du texte avant/après le JSON
- Les erreurs JSON courantes peuvent être corrigées automatiquement
- Augmente le taux de succès du parsing

### Alternatives Considérées
- Parsing JSON strict uniquement : Rejetée car trop fragile
- Re-génération en cas d'erreur : Considérée mais complexité ajoutée
- Extraction manuelle avec regex : Considérée comme fallback

### Risques
- Correction automatique peut introduire des erreurs
- Mitigation : Validation stricte après parsing

---

## 5. Validation avec Pydantic

### Décision
Utiliser Pydantic pour toutes les validations de données.

### Justification
- Obligatoire selon le sujet
- Validation automatique des types
- Messages d'erreur clairs
- Intégration naturelle avec Python

### Alternatives Considérées
- Validation manuelle : Rejetée (non conforme au sujet)
- Autres bibliothèques de validation : Rejetées (pydantic obligatoire)

---

## 6. Gestion d'Erreurs : Skip et Continue

### Décision
En cas d'erreur sur un prompt, skip ce prompt et continuer avec les suivants.

### Justification
- Robustesse : une erreur ne bloque pas tout le traitement
- Permet de traiter le maximum de prompts
- Logs clairs pour identifier les problèmes

### Alternatives Considérées
- Arrêt complet en cas d'erreur : Rejetée (pas robuste)
- Retry automatique : Considérée mais peut boucler indéfiniment
- Correction automatique : Utilisée quand possible, skip sinon

---

## 7. Structure de Fichiers par Module

### Décision
Un fichier Python par module/responsabilité.

### Justification
- Organisation claire
- Facilite la navigation
- Correspond à la séparation des responsabilités
- Facilite les tests unitaires

### Alternatives Considérées
- Tous les modules dans un seul fichier : Rejetée (illisible)
- Regroupement par couche : Considérée mais moins claire

---

## 8. Chargement Unique du Vocabulaire

### Décision
Charger le vocabulaire JSON une seule fois au démarrage et le réutiliser.

### Justification
- Performance : évite de recharger à chaque tokenisation
- Simplicité : un seul point de chargement
- Efficacité mémoire : chargement unique

### Alternatives Considérées
- Rechargement à chaque utilisation : Rejetée (inefficace)
- Cache avec rechargement : Inutile pour ce projet

---

## 9. Critères d'Arrêt de Génération

### Décision
Arrêter la génération sur :
1. Token de fin de séquence (EOS)
2. Longueur maximale atteinte
3. Détection de fin de JSON valide

### Justification
- Évite les générations infinies
- Optimise la longueur des réponses
- Détecte la fin naturelle du JSON

### Alternatives Considérées
- Uniquement EOS token : Rejetée (peut être trop long)
- Uniquement longueur max : Rejetée (peut couper le JSON)
- Combinaison : Choisie pour robustesse

---

## 10. Format de Prompt avec Exemples JSON

### Décision
Inclure des exemples de questions/réponses en format JSON dans le prompt.

### Justification
- Montre clairement le format attendu
- Le LLM apprend par imitation
- Format JSON explicite guide la génération

### Alternatives Considérées
- Exemples en texte libre : Rejetée (pas assez structuré)
- Exemples en format différent : Rejetée (confusion)

---

## 11. Pas de Retry Automatique par Défaut

### Décision
Ne pas implémenter de retry automatique systématique, mais permettre un retry manuel si nécessaire.

### Justification
- Simplicité : évite les boucles infinies
- Performance : pas de temps perdu sur prompts problématiques
- Clarté : erreurs visibles immédiatement

### Alternatives Considérées
- Retry automatique avec limite : Considérée mais complexité ajoutée
- Retry avec prompt modifié : Considérée pour Phase 5 si nécessaire

---

## 12. Validation Progressive

### Décision
Valider les données à chaque étape (parsing, types, structure) plutôt qu'une seule validation finale.

### Justification
- Détection précoce des erreurs
- Messages d'erreur plus précis
- Évite de traiter des données invalides

### Alternatives Considérées
- Validation unique à la fin : Rejetée (moins informative)
- Validation partielle : Choisie (progressive)

---

## 13. Gestion des Tokens Inconnus

### Décision
En cas de token inconnu dans le vocabulaire, utiliser une stratégie de fallback (skip ou remplacement).

### Justification
- Robustesse face aux tokens inconnus
- Permet de continuer même avec des problèmes de vocabulaire
- Évite les crashes

### Alternatives Considérées
- Erreur fatale : Rejetée (pas robuste)
- Ignorer le token : Choisie comme fallback

---

## 14. Écriture Incrémentale vs Batch

### Décision
Collecter tous les résultats et écrire en une fois à la fin.

### Justification
- Simplicité : une seule écriture
- Atomicité : tout ou rien
- Performance : une seule opération I/O

### Alternatives Considérées
- Écriture incrémentale : Considérée mais complexité ajoutée
- Écriture par prompt : Rejetée (peut corrompre le JSON)

---

## 15. Pas de Caching des Prompts Construits

### Décision
Ne pas mettre en cache les prompts construits, les reconstruire à chaque fois.

### Justification
- Simplicité : pas de gestion de cache
- Les prompts peuvent varier légèrement
- Overhead de cache non justifié pour ce projet

### Alternatives Considérées
- Cache des prompts : Considérée mais complexité inutile
- Templates de prompts : Utilisés mais pas de cache

---

## 16. Structure de Sortie JSON Strict

### Décision
Respecter strictement le format JSON de sortie avec exactement les clés : prompt, fn_name, args.

### Justification
- Conformité au sujet
- Validation facile
- Format standardisé

### Alternatives Considérées
- Format flexible : Rejetée (non conforme)
- Clés supplémentaires : Interdites par le sujet

---

## 17. Logging des Erreurs

### Décision
Logger toutes les erreurs avec des messages clairs, mais ne pas arrêter le programme.

### Justification
- Débogage facilité
- Traçabilité des problèmes
- Continuation du traitement

### Alternatives Considérées
- Pas de logging : Rejetée (difficile à déboguer)
- Logging avec arrêt : Rejetée (pas robuste)

---

## 18. Pas de Parallélisation

### Décision
Traiter les prompts séquentiellement, pas de parallélisation.

### Justification
- Simplicité : pas de gestion de threads/processus
- Le LLM est appelé de manière synchrone
- Pas de gain de performance significatif attendu

### Alternatives Considérées
- Parallélisation : Considérée mais complexité ajoutée
- Traitement asynchrone : Considérée mais non nécessaire

---

## Résumé des Décisions Clés

1. ✅ Architecture modulaire
2. ✅ Prompt engineering avec exemples
3. ✅ Génération greedy token par token
4. ✅ Parsing flexible avec correction
5. ✅ Validation Pydantic
6. ✅ Skip et continue en cas d'erreur
7. ✅ Structure de fichiers par module
8. ✅ Chargement unique du vocabulaire
9. ✅ Critères d'arrêt multiples
10. ✅ Format JSON strict

---

*Document créé lors de la Phase 2 - Conception et Architecture*  
*Date : [À compléter]*

