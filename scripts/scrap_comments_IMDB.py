import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from numpy.random import normal
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from utils import *

NBR_FILM = 100
N_PAGES = 5

trailer_df = pd.DataFrame(columns = ["Title", "TrailerLink"])

def scrape_films_links(driver, nbr_film):
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    links = soup.find_all('a', class_='ipc-title-link-wrapper')
    title = soup.find_all('h3', class_ = 'ipc-title__text')

    list_film_links_comments = [modify_links_comments(link.get('href')) for link in links][:nbr_film]
    list_film_links_images = [modify_links_image(link.get('href')) for link in links][:nbr_film]

    list_film_title = [titles.text.strip() for titles in title][1:nbr_film]

    dictionnary_comment = {title : link for title, link in zip(list_film_title, list_film_links_comments)}
    dictionnary_images = {title : link for title, link in zip(list_film_title, list_film_links_images)}

    print("liste des films obtenues ✅")

    return(dictionnary_comment, dictionnary_images)

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

def scrape_images(driver, output_file):
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    div_tag = soup.find('div', class_='ipc-media')
    img_tag = div_tag.find('img')
    image_url = img_tag['src']

    image_link = requests.get(image_url)

    with open(output_file, "wb") as f:
        f.write(image_link.content)

def scrape_trailer(driver, title ):
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    a_tag = soup.find('a', class_='ipc-lockup-overlay sc-e4a5af48-0 jkikQB ipc-focusable')

    if a_tag is None :
        trailer_df.loc[len(trailer_df)] = [title, "Pas de lien disponible"]
    else :
        link = a_tag.get("href")

        full_link = "https://www.imdb.com" + link

        trailer_df.loc[len(trailer_df)] = [title, full_link]


def get_dic_of_links():
    driver_link = make_driver()
    login_to_pj(driver_link, url="https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
    dic_links_comment, dic_links_image = scrape_films_links(driver_link, nbr_film=NBR_FILM)
    return(dic_links_comment, dic_links_image)

def get_comment_film(link, driver, title):
    login_to_pj(driver, link)

    output_file = f"../json_IMDB/commentaires_{title}.json"

    scrape_comments(driver=driver, n_pages =N_PAGES, json_output_file=output_file)

def get_images_film(link, driver, title):
    login_to_pj(driver, link)

    output_file = f"../images/{title}.jpg"

    scrape_images(driver=driver, output_file = output_file)

def get_trailer_film(link, driver, title):
    login_to_pj(driver, link)

    scrape_trailer(driver=driver, title = title)

def get_all_comments_images():
    dic_links, dic_images = get_dic_of_links()
    driver = make_driver()

    for title,link in tqdm(dic_images.items()):
        get_images_film(link, driver, title)
        get_trailer_film(link, driver, title)

    for title,link in tqdm(dic_links.items()):
        get_comment_film(link, driver, title)


if __name__ == "__main__":
    get_all_comments_images()
    trailer_df.to_csv("../data/trailer_links.csv")