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
    driver.get(url)
    return driver

def modify_links_comments(url):
    extracted_part = url.split("?")[0]
    good_url = "https://www.imdb.com" + extracted_part + "reviews?ref_=tt_urv"
    return(good_url)

def modify_links_image(url):
    extracted_part = url.split("?")[0]
    good_url = "https://www.imdb.com" + extracted_part
    return(good_url)