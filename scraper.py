from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython.display import display, Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import pandas as pd

from product_class import Product

class Scraper:

    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = None
        self.products = []
        self.n = 1

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dve-shm-uage')
        self.driver = webdriver.Chrome(options=options)

    def visit_page(self, url):
        self.driver.get(url)
        time.sleep(5)

    def get_products(self):
        grids = self.driver.find_elements(By.CSS_SELECTOR, '[id^="browse-search-pods-"]')
        for grid in grids:
            # Scroll into view to ensure boxes are loaded
            actions = ActionChains(self.driver)
            actions.move_to_element(grid).perform()
            time.sleep(1)
            boxes = grid.find_elements(By.CLASS_NAME, 'browse-search__pod')
            for box in boxes:
                product = Product.from_web_element(box, self.n)
                self.n += 1
                self.products.append(product)   


    def next_page(self, page_num):
        pagination_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@class, 'hd-pagination__link') and contains(text(), {str(page_num)})]"))
        )
        href = pagination_link.get_attribute('href')
        self.driver.get(href)

    def scrape(self, start_page=1, end_page=5):
        self.setup_driver()
        self.visit_page(self.base_url)
        self.get_products()
        for page_num in range(start_page + 1, end_page + 1):
            self.next_page(page_num)
            self.get_products()
            
        self.driver.quit()


    def to_dataframe(self):
        product_dicts = [product.to_dict() for product in self.products]
        df = pd.DataFrame(product_dicts).set_index('Number')
        df = df[(df['Label'] != 'Sponsored') & 
                 (~df['Brand'].isin(['Hampton Bay', 'Home Decorators Collection']))]
        return df


# if __name__ == "__main__":
