import json
import time

from bs4 import BeautifulSoup
from tqdm import tqdm
from numpy.random import normal
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from utils import *

NBR_FILM = 100
N_PAGES = 5


def scrape_films_links(driver, nbr_film):
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    links = soup.find_all('a', class_='ipc-title-link-wrapper')
    title = soup.find_all('h3', class_ = 'ipc-title__text')

    list_film_links = [modify_links(link.get('href')) for link in links][:nbr_film]
    list_film_title = [titles.text.strip() for titles in title][1:nbr_film]

    dictionnary = {title : link for title, link in zip(list_film_title, list_film_links)}

    print("liste des films obtenues ✅")

    return(dictionnary)

def scrape_comments(driver, json_output_file, n_pages):
    for _ in range(0, n_pages):

        try:
            load_more_button = driver.find_element(By.ID, 'load-more-trigger')
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(abs(normal(1, 3)))  # Attendre un peu pour le chargement des commentaires
            driver.implicitly_wait(4)
        except ElementNotInteractableException:
            break
        except NoSuchElementException:
            break

    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    comments_spoil_short = soup.find_all(class_="text show-more__control")
    comment_texts = [comment.text.strip() for comment in comments_spoil_short]

    comments_long = soup.find_all(class_="text show-more__control clickable")
    comments_long_list = [comment.text.strip() for comment in comments_long]

    comment_texts.extend(comments_long_list)

    json_file = {str(i): comment for i, comment in enumerate(comment_texts)}

    with open(json_output_file, 'w', encoding='utf-8') as file:
        json.dump(json_file, file, ensure_ascii=False, indent=4)

def get_dic_of_links():
    driver_link = make_driver()
    login_to_pj(driver_link, url="https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
    dic_links = scrape_films_links(driver_link, nbr_film=NBR_FILM)
    return(dic_links)

def get_comment_film(link, driver, title):
    login_to_pj(driver, link)

    output_file = f"../json_IMDB/commentaires_{title}.json"

    scrape_comments(driver=driver, n_pages =N_PAGES, json_output_file=output_file)

def get_all_the_comments():
    dic_links = get_dic_of_links()
    driver = make_driver()

    for title,link in tqdm(dic_links.items()):
        get_comment_film(link, driver, title)


if __name__ == "__main__":
    get_all_the_comments()