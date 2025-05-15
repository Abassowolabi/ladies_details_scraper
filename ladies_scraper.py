import json
import random
import logging
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# --- Chrome Setup ---
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(executable_path='C:/Users/user/Desktop/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# --- Function to verify valid profile page ---
def is_profile_page(driver):
    try:
        driver.find_element(By.XPATH, '//strong[@itemprop="telephone"]')
        driver.find_element(By.XPATH, '//h2[contains(@class, "kuenstlername")]')
        return True
    except:
        return False

# --- Navigate to Homepage ---
driver.get("https://www.ladies.de/")
driver.maximize_window()

# --- Accept Cookies ---
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[(text())="Alle akzeptieren"]'))
    ).click()
    logging.info("✅ Accepted cookies")
    sleep(3)
except Exception:
    logging.warning("Cookies already accepted or not found")

# --- Search for "Alle Regionen" ---
try:
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'plzort')))
    search_box.send_keys('Alle Regionen')
    sleep(2)
    driver.find_element(By.XPATH, '//*[@role="menuitem"]').click()
    logging.info("✅ Selected 'Alle Regionen'")
    sleep(5)
except Exception:
    logging.error("❌ Search or region selection failed")

# --- Close Banner (if exists) ---
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="ladiesStars-close-button" and contains(@onclick, "closeLadiesStarsBanner")]'))
    ).click()
    logging.info("✅ Closed promotional banner")
    sleep(2)
except Exception:
    logging.info("⏭ No banner to close or already closed")

# --- Click "zu den Anzeigen" ---
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[normalize-space(text())="zu den Anzeigen"]'))
    ).click()
    logging.info("✅ Navigated to ad listings")
    sleep(5)
except Exception:
    logging.error("❌ Navigation to ads failed")

# --- Start Scraping ---
results = []
max_pages = 10
base_url = "https://www.ladies.de/sex-anzeigen"

for page in range(1, max_pages + 1):
    page_url = f"{base_url}?page={page}"
    driver.get(page_url)
    logging.info(f"\n📄 Scraping Page {page}: {page_url}")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "ordered") and contains(@class, "popunder_element")]'))
        )
        sel = Selector(text=driver.page_source)
        profile_links = sel.xpath('//a[contains(@class, "ordered") and contains(@class, "popunder_element")]/@href').extract()
        full_urls = [urljoin(base_url, href) for href in profile_links]

        for url in full_urls:
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//strong[@itemprop="telephone"]'))
                )

                if is_profile_page(driver):
                    name = driver.find_element(By.XPATH, '//h2[contains(@class, "kuenstlername")]').text
                    phone = driver.find_element(By.XPATH, '//strong[@itemprop="telephone"]').text

                    results.append({
                        'user_name': name,
                        'phone_number': phone
                    })
                    logging.info(f"✔ {name} - {phone}")
                else:
                    logging.info(f"⏭ Skipped invalid page: {url}")

                sleep(random.uniform(2, 5))

            except Exception:
                logging.warning(f"❌ Failed to scrape profile {url}:")
                continue

    except Exception as e:
        logging.error(f"❌ Failed to load page {page}: {e}")

# --- Save to JSON ---
try:
    with open('scraped_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    logging.info(f"\n✅ Successfully saved {len(results)} profiles to scraped_data.json")
except Exception as e:
    logging.error("❌ Failed to save JSON:", e)

# --- Close Browser ---
driver.quit()
