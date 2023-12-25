import pandas as pd

trailer_links = pd.read_csv("./data/trailer_links.csv")

notes = pd.read_csv("./data/notes_percentage_positive.csv")
notes["Film"] = notes["Film"].apply(lambda x : x.replace("_", " "))

positive_reviews = pd.read_csv("./data/postive_reviews.csv")
positive_reviews["titre"] = positive_reviews["titre"].apply(lambda x : x.replace("_", " "))

negative_reviews = pd.read_csv("./data/negative_reviews.csv")
negative_reviews["titre"] = negative_reviews["titre"].apply(lambda x : x.replace("_", " "))


def get_link_by_movie_name(movie_name):
    row = trailer_links[trailer_links['Title'] == movie_name]
    if not row.empty:
        return row['TrailerLink'].values[0]
    else:
        return "Pas de lien disponible"

def get_infos_fim(movie_name):
    row = notes[notes['Film'] == movie_name]
    if not row.empty:
        note = row["notes"].values[0]
        pcentage_positif = row["pourcentages_positive"].values[0]
        return (note, pcentage_positif)
    else :
        return(0,0)

def get_example_comments(movie_name) :
    temp = positive_reviews[positive_reviews['avis'].str.len() < 2000]
    index_positive = temp[temp['titre'] == movie_name]["sentiment_score_VADER"].idxmax()
    positive_comments = temp.loc[index_positive, 'avis']

    temp = negative_reviews[negative_reviews['avis'].str.len() < 2000]
    index_negative = temp[temp['titre'] == movie_name]["sentiment_score_VADER"].idxmin()
    negative_comments = temp.loc[index_negative, 'avis']

    return(positive_comments, negative_comments)
