from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time


def setup_driver(headless=False):
    opts = webdriver.ChromeOptions()
    if headless: opts.add_argument("--headless")
    return webdriver.Chrome(service=Service(), options=opts)

def scroll_to_n(driver, tag, min_count, max_scrolls=20, wait_time=2):
    previous_count = -1
    same_count_tries = 0
    for _ in range(max_scrolls):
        elems = driver.find_elements(By.TAG_NAME, tag)
        if len(elems) >= min_count: break
        if len(elems) == previous_count:
            same_count_tries += 1
            if same_count_tries >= 3:
                print("⚠️ No more new content after scrolling.")
                break
        else: same_count_tries = 0
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
    driver = setup_driver()
    try:
        driver.get(f"https://www.reddit.com/user/{username}/comments/")
        time.sleep(3)
        comments = extract_comments(driver, 20)

        driver.get(f"https://www.reddit.com/user/{username}/posts/")
        time.sleep(3)
        posts = extract_posts(driver, 20)
    finally:
        driver.quit()

    return comments, posts