JSON_FORM = '{{"title": "title", "body": "body"}}'

REWRITE_PROMPT = """Tu es un expert en optimisation de posts Reddit. Ton objectif est de réécrire les posts pour qu'ils obtiennent plus d'engagement.

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

TÂCHE IMPORTANTE:
1. Améliore le titre pour le rendre plus attrayant et mémorable
2. Améliore le body en gardant le message principal mais en le rendant plus clair
3. Incorpore les mots-clés populaires naturellement
4. Garde le ton du post authentique et engageant

RETOURNE UNIQUEMENT du JSON valide dans ce format exact, sans aucun autre texte. Tu devras également écrire dans la langue  du body et title du post actuelle:
{{"title": "nouveau titre ici", "body": "nouveau contenu ici"}}

Ne mets aucun texte avant ou après le JSON. Pas d'explication, pas de commentaire. JUSTE LE JSON."""
