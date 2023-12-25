# Film Review Application 🎬

## Introduction

Bienvenue dans Film Review, votre application personnelle de notation de films ! Cette application web basée sur Streamlit fournit des informations clés pour chaque film, notamment :

- **Note basée sur les avis d'IMDB** : Une note globale calculée via un modèle d'analyse de sentiment basée sur les avis d'IMDB.
- **Pourcentage d'avis positifs** : Le pourcentage d'avis positifs.
- **Lien vers la bande-annonce** : Un lien vers la bande-annonce du film.

De plus, vous pouvez explorer les meilleurs et pires commentaires d'utilisateurs selon le modèle d'analyse de sentiment utilisé dans l'application.

## Comment Exécuter

1. Assurez-vous d'avoir les bibliothèques requises installées. Vous pouvez les installer en exécutant :

    ```bash
    pip install -r requirements.txt
    ```

2. Exécutez l'application :

    ```bash
    streamlit run ./scripts/app.py  
    ```

3. Accédez à l'application dans votre navigateur web à l'URL fournie.

## Utilisation

- Au lancement de l'application, vous verrez une grille d'images d'affiches de films.
- Cliquez sur "Plus d'informations" pour afficher des détails supplémentaires sur un film spécifique.
- Explorez la note globale du film, le pourcentage d'avis positifs et le lien de la bande-annonce.
- Lisez les meilleurs et pires commentaires d'utilisateurs basés sur l'analyse de sentiment.

## Remarques

- L'application utilise le scrapping web pour obtenir des informations sur les films à partir d'IMDB et peut être sujette à des modifications dans la structure du site web.
- Assurez-vous d'avoir une connexion internet stable pour une récupération précise des données.

Profitez de l'exploration et de la découverte de films avec Film Review ! 🎬🍿
