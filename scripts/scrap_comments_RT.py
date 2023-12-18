import time

from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from numpy.random import normal
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from utils import *

def scrape_films_links(driver, n_pages):
    list_film_links = []
    for i in range(0, n_pages):
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        links = soup.find_all('a', class_='js-tile-link', attrs={'data-qa': 'discovery-media-list-item'})

        for link in links:
            link_film = "https://www.rottentomatoes.com" + link.get('href') + "/reviews?type=user"
            list_film_links.append(link_film)

        time.sleep(abs(normal(1, 3)))
        driver.implicitly_wait(4)

        driver.find_element(By.CSS_SELECTOR, 'button[data-qa="dlp-load-more-button"]').click()
    print("liste des films obtenues ✅")
    return(list_film_links)

def scrape_comments(driver, json_output_file, n_pages):
    try:
        df = pd.read_json(json_output_file, orient='records')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['comment'])

    for i in range(0, n_pages):

        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        comments = soup.find_all('p', class_='audience-reviews__review js-review-text',
                                 attrs={'data-qa': 'review-text'})

        comment_texts = [comment.text.strip() for comment in comments]
        new_comments = [comment for comment in comment_texts if comment not in df['comment'].values]

        df = pd.concat([df, pd.DataFrame(new_comments, columns=['comment'])], ignore_index=True)

        time.sleep(abs(normal(1, 3)))
        driver.implicitly_wait(4)

        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, 'rt-button[data-qa="load-more-btn"]')
            load_more_button.click()
        except ElementNotInteractableException :
            print("Le bouton 'charger plus' n'existe pas, sortie de la boucle.")
            break

    df.to_json(json_output_file, orient='records')
    print("commentaires sauvegardés ✅")

def get_list_of_links():
    driver_link = make_driver()
    login_to_pj(driver_link, url="https://www.rottentomatoes.com/browse/movies_in_theaters/")
    list_links = scrape_films_links(driver_link, 1)
    return(list_links)

def get_comment_film(link, driver):
    login_to_pj(driver, link)

    movie_name_part = link.split('/')[4]

    output_file = f"../json/commentaires_{movie_name_part}.json"

    scrape_comments(driver=driver, n_pages = 1, json_output_file=output_file)

def get_all_the_comments():
    list_links = get_list_of_links()
    driver = make_driver()

    for link in list_links:
        get_comment_film(link, driver)


if __name__ == "__main__":
    get_all_the_comments()