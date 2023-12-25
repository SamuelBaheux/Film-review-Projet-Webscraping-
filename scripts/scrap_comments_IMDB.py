import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from numpy.random import normal
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By
from tqdm import tqdm

from scrap_utils import *


class IMDBScraper:
    def __init__(self, nbr_film=100, n_pages=5):
        self.NBR_FILM = nbr_film
        self.N_PAGES = n_pages
        self.trailer_df = pd.DataFrame(columns=["Title", "TrailerLink"])
        self.driver = make_driver()

    def scrape_films_links(self):
        response = self.driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        links = soup.find_all('a', class_='ipc-title-link-wrapper')
        title = soup.find_all('h3', class_='ipc-title__text')

        list_film_links_comments = [modify_links_comments(link.get('href')) for link in links][:self.NBR_FILM]
        list_film_links_images = [modify_links_image(link.get('href')) for link in links][:self.NBR_FILM]

        list_film_title = [titles.text.strip() for titles in title][1:self.NBR_FILM]

        dictionnary_comment = {title: link for title, link in zip(list_film_title, list_film_links_comments)}
        dictionnary_images = {title: link for title, link in zip(list_film_title, list_film_links_images)}

        print("liste des films obtenue ✅")

        return dictionnary_comment, dictionnary_images

    def scrape_comments(self, json_output_file):
        for _ in range(0, self.N_PAGES):
            try:
                load_more_button = self.driver.find_element(By.ID, 'load-more-trigger')
                self.driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(abs(normal(1, 3)))  # Attendre un peu pour le chargement des commentaires
                self.driver.implicitly_wait(4)
            except (ElementNotInteractableException, NoSuchElementException):
                break

        response = self.driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        comments_spoil_short = soup.find_all(class_="text show-more__control")
        comment_texts = [comment.text.strip() for comment in comments_spoil_short]

        comments_long = soup.find_all(class_="text show-more__control clickable")
        comments_long_list = [comment.text.strip() for comment in comments_long]

        comment_texts.extend(comments_long_list)

        json_file = {str(i): comment for i, comment in enumerate(comment_texts)}

        with open(json_output_file, 'w', encoding='utf-8') as file:
            json.dump(json_file, file, ensure_ascii=False, indent=4)

    def scrape_images(self, output_file):
        response = self.driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        div_tag = soup.find('div', class_='ipc-media')
        img_tag = div_tag.find('img')
        image_url = img_tag['src']

        image_link = requests.get(image_url)

        with open(output_file, "wb") as f:
            f.write(image_link.content)

    def scrape_trailer(self, title):
        response = self.driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        a_tag = soup.find('a', class_='ipc-lockup-overlay sc-e4a5af48-0 jkikQB ipc-focusable')

        if a_tag is None:
            self.trailer_df.loc[len(self.trailer_df)] = [title, "Pas de lien disponible"]
        else:
            link = a_tag.get("href")
            full_link = "https://www.imdb.com" + link
            self.trailer_df.loc[len(self.trailer_df)] = [title, full_link]

    def get_dic_of_links(self):
        login_to_pj(self.driver, url="https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
        dic_links_comment, dic_links_image = self.scrape_films_links()
        return dic_links_comment, dic_links_image

    def get_comment_film(self, link, title):
        login_to_pj(self.driver, link)
        output_file = f"../data/json_IMDB1/commentaires_{title}.json"
        self.scrape_comments(json_output_file=output_file)

    def get_images_film(self, link, title):
        login_to_pj(self.driver, link)
        output_file = f"../data/images1/{title}.jpg"
        self.scrape_images(output_file=output_file)

    def get_trailer_film(self, link, title):
        login_to_pj(self.driver, link)
        self.scrape_trailer(title=title)

    def get_all_comments_images(self):
        dic_links, dic_images = self.get_dic_of_links()

        print("Récupération des images et des liens des trailers ...")
        for title, link in tqdm(dic_images.items()):
            self.get_images_film(link, title)
            self.get_trailer_film(link, title)
        print("Images et liens des trailers obtenus ✅")

        print("Récupération des commentaires")
        for title, link in tqdm(dic_links.items()):
            self.get_comment_film(link, title)
        print("Commentaires obtenus ✅")

    def save_trailer_df(self, output_file="../data/trailer_links1.csv"):
        self.trailer_df.to_csv(output_file)


if __name__ == "__main__":
    imdb_scraper = IMDBScraper(nbr_film=100, n_pages=5)
    imdb_scraper.get_all_comments_images()
    imdb_scraper.save_trailer_df()
