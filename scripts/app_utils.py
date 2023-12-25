import pandas as pd

trailer_links = pd.read_csv("./data/trailer_links.csv")

notes = pd.read_csv("./data/notes_percentage_positive.csv")
notes["Film"] = notes["Film"].apply(lambda x : x.replace("_", " "))

positive_reviews = pd.read_csv("./data/postive_reviews.csv")
positive_reviews["titre"] = positive_reviews["titre"].apply(lambda x : x.replace("_", " "))

negative_reviews = pd.read_csv("./data/negative_reviews.csv")
negative_reviews["titre"] = negative_reviews["titre"].apply(lambda x : x.replace("_", " "))


def get_link_by_movie_name(movie_name):
    """
    Recherche le lien de la bande-annonce d'un film dans un DataFrame.

    Parameters:
    - movie_name (str): Le nom du film pour lequel on souhaite obtenir le lien de la bande-annonce.

    Returns:
    - str: Le lien de la bande-annonce du film s'il est trouvé dans le DataFrame.
           Si le film n'est pas trouvé, la fonction renvoie "Pas de lien disponible".
    """
    row = trailer_links[trailer_links['Title'] == movie_name]
    if not row.empty:
        return row['TrailerLink'].values[0]
    else:
        return "Pas de lien disponible"

def get_infos_fim(movie_name):
    """
    Récupère les informations sur un film à partir d'un DataFrame.

    Parameters:
    - movie_name (str): Le nom du film pour lequel on souhaite obtenir les informations.

    Returns:
    - tuple: Un tuple contenant les informations du film.
      - Si le film est trouvé dans le DataFrame, le tuple contient la note du film et le pourcentage positif.
      - Si le film n'est pas trouvé, le tuple contient (0, 0).
    """
    row = notes[notes['Film'] == movie_name]
    if not row.empty:
        note = row["notes"].values[0]
        pcentage_positif = row["pourcentages_positive"].values[0]
        return (note, pcentage_positif)
    else :
        return(0,0)

def get_example_comments(movie_name) :
    """
    Obtient des commentaires exemples positifs et négatifs sur un film à partir de DataFrames de critiques.

    Parameters:
    - movie_name (str): Le nom du film pour lequel on souhaite obtenir des commentaires exemples.

    Returns:
    - tuple: Un tuple contenant les commentaires exemples positifs et négatifs du film.
      - Si des commentaires sont disponibles, le tuple contient le commentaire le plus positif et le plus négatif.
      - Si aucun commentaire n'est trouvé, le tuple contient (None, None).
    """
    temp = positive_reviews[positive_reviews['avis'].str.len() < 2000]
    index_positive = temp[temp['titre'] == movie_name]["sentiment_score_VADER"].idxmax()
    positive_comments = temp.loc[index_positive, 'avis']

    temp = negative_reviews[negative_reviews['avis'].str.len() < 2000]
    index_negative = temp[temp['titre'] == movie_name]["sentiment_score_VADER"].idxmin()
    negative_comments = temp.loc[index_negative, 'avis']

    return(positive_comments, negative_comments)
