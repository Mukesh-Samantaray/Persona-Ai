from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options

def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=en-US")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(), options=options)

def wait_for_articles(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
    except:
        # Save screenshot and raise clearer error
        driver.save_screenshot("debug_headless_error.png")
        raise RuntimeError("Timeout: Reddit content not loading in headless. Screenshot saved.")


def scroll_to_n(driver, tag, min_count, max_scrolls=20, wait_time=2):
    previous_count = -1
    same_count_tries = 0
    for _ in range(max_scrolls):
        elems = driver.find_elements(By.TAG_NAME, tag)
        if len(elems) >= min_count:
            break
        if len(elems) == previous_count:
            same_count_tries += 1
            if same_count_tries >= 3:
                print("⚠ No more new content after scrolling.")
                break
        else:
            same_count_tries = 0
        previous_count = len(elems)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)

def extract_comments(driver, limit=20):
    scroll_to_n(driver, "article", limit)
    data = []
    for art in driver.find_elements(By.TAG_NAME, "article")[:limit]:
        soup = BeautifulSoup(art.get_attribute("outerHTML"), "html.parser")
        dt = soup.select_one("time")
        date = dt["datetime"] if dt else ""
        p = soup.select_one("div#-post-rtjson-content p")
        text = p.get_text(strip=True) if p else ""
        if text:
            data.append((date, text))
    return data

def extract_posts(driver, limit=20):
    scroll_to_n(driver, "article", limit * 2)
    data = []
    for art in driver.find_elements(By.TAG_NAME, "article"):
        soup = BeautifulSoup(art.get_attribute("outerHTML"), "html.parser")
        body = soup.select_one("div[id$='-post-rtjson-content'] p")
        title = soup.select_one("a[slot='title']")
        if title and body:
            dt = soup.select_one("time")
            date = dt["datetime"] if dt else ""
            data.append((date, title.get_text(strip=True), body.get_text(strip=True)))
        if len(data) >= limit:
            break
    return data

def scrape_user_data(username):
    driver = setup_driver(headless=True)
    try:
        # Scrape comments
        driver.get(f"https://www.reddit.com/user/{username}/comments/")
        wait_for_articles(driver)
        comments = extract_comments(driver, 20)

        # Scrape posts
        driver.get(f"https://www.reddit.com/user/{username}/posts/")
        wait_for_articles(driver)
        posts = extract_posts(driver, 20)
    finally:
        driver.quit()

    return comments, posts