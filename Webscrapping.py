from selenium import webdriver
from selenium_stealth import stealth
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from numpy.random import normal

def login_to_pj(driver: webdriver.Chrome) -> webdriver.Chrome:
    url = "https://www.rottentomatoes.com/m/avatar_the_way_of_water/reviews?type=user"
    driver.get(url)
    print("La page a été chargée")
    return driver


######## POUR INITIALISER TON DRIVER ##########

def make_driver() -> webdriver:
    """Instantiate the webdriver with Selenium."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless") # tu vas ouvrir une fenetre chrome automatiquement ici

    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1)"
        "AppleWebKit/605.1.15 (KHTML, like Gecko)"
        "Version/16.1 Safari/605.1.15"
    )

    driver = webdriver.Chrome(options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en", "fr"],
        vendor="Google Inc.",
        platform="Win32",
        # webgl_vendor="Intel Inc.",
        # renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    print("Driver créée")
    return driver





def scrape_com(driver, json_output_file, n_pages):
    # Vérifier si le fichier JSON de sortie existe déjà
    try:
        df = pd.read_json(json_output_file, orient='records')
    except FileNotFoundError:
        # Si le fichier n'existe pas, créer un dataframe vide
        df = pd.DataFrame(columns=['comment'])

    for i in range(0, n_pages):
        # Obtenir le contenu de la page avec Selenium
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        # Trouver tous les éléments HTML correspondant à la balise <p> avec la classe et l'attribut spécifiés
        comments = soup.find_all('p', class_='audience-reviews__review js-review-text',
                                 attrs={'data-qa': 'review-text'})

        # Extraire le texte de chaque commentaire
        comment_texts = [comment.text.strip() for comment in comments]

        # Filtrer les commentaires déjà présents dans le dataframe
        new_comments = [comment for comment in comment_texts if comment not in df['comment'].values]

        # Ajouter les commentaires uniques au dataframe
        df = pd.concat([df, pd.DataFrame(new_comments, columns=['comment'])], ignore_index=True)

        # Attendre un certain temps (vous pouvez ajuster cela selon vos besoins)
        time.sleep(abs(normal(1, 3)))

        # Attendre implicitement avant de cliquer sur le bouton "Load More"
        driver.implicitly_wait(4)

        # Cliquer sur le bouton "Load More"
        driver.find_element(By.CSS_SELECTOR, 'rt-button[data-qa="load-more-btn"]').click()

    # Sauvegarder le dataframe au format JSON
    df.to_json(json_output_file, orient='records')


if __name__ == "__main__":
    driver = make_driver()
    login_to_pj(driver)

    output_file = "commentaires_avatar.json"
    scrape_com(driver=driver, n_pages = 200, json_output_file=output_file)

