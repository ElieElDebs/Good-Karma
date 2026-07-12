JSON_FORM = '{"title" : title, "body" : body}'

REWRITE_PROMPT = """
Tu es un expert en optimisation de posts Reddit.

### Post ACTUEL:
Title: {draft_title}
Body: {draft_body}

### KPI ET FORCES/FAIBLESSES:
{weakness_and_strength}

### CONSEILS D'AMÉLIORATION:
{advices}

### POSTS EXEMPLAIRES (À étudier):
{examples}

### PATTERNS DE SUCCÈS pour r/{subreddit}:
- Longueur titre idéale: {ideal_title_length}
- Mots-clés populaires: {ideal_words_to_use}

TÂCHE: Réécris le post en AMÉLIORANT les faiblesses identifiées. 
Retourne UNIQUEMENT le nouveau titre et body au format JSON et rien d'autre.

Format de réponse: 

title : title
body : body
"""
