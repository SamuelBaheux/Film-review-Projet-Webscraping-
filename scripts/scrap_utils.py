from selenium import webdriver
from selenium_stealth import stealth

def make_driver() -> webdriver:
    """Instantiate the webdriver with Selenium."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless") # tu vas ouvrir une fenetre chrome automatiquement ici

    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1)"
                                "AppleWebKit/605.1.15 (KHTML, like Gecko)"
                                "Version/16.1 Safari/605.1.15")

    driver = webdriver.Chrome(options=chrome_options)

    stealth(driver,
            languages=["en-US", "en", "fr"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    return driver


def login_to_pj(driver: webdriver.Chrome, url: str) -> webdriver.Chrome:
    """
    Navigue vers l'URL spécifiée en utilisant un pilote de navigateur Chrome.

    Parameters:
    - driver (webdriver.Chrome): Le pilote de navigateur Chrome.
    - url (str): L'URL de la page vers laquelle naviguer.

    Returns:
    - webdriver.Chrome: Le pilote de navigateur Chrome après avoir navigué vers l'URL spécifiée.
    """
    driver.get(url)
    return driver

def modify_links_comments(url):
    """
      Modifie un lien IMDb pour rediriger vers la page des commentaires du film.

      Parameters:
      - url (str): Le lien IMDb original.

      Returns:
      - str: Le lien modifié redirigeant vers la page des commentaires du film.
      """
    extracted_part = url.split("?")[0]
    good_url = "https://www.imdb.com" + extracted_part + "reviews?ref_=tt_urv"
    return(good_url)

def modify_links_image(url):
    """
    Modifie un lien IMDb pour rediriger vers la page d'image du film.

    Parameters:
    - url (str): Le lien IMDb original.

    Returns:
    - str: Le lien modifié redirigeant vers la page d'image du film.
    """
    extracted_part = url.split("?")[0]
    good_url = "https://www.imdb.com" + extracted_part
    return(good_url)