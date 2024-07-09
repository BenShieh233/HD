from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython.display import display, Image
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from product_class import Product

def visit_page(driver, url):
    driver.get(url)
    time.sleep(5)


def get_products(driver, products, n):
    grids = driver.find_elements(By.CSS_SELECTOR, '[id^="browse-search-pods-"]')
    for grid in grids:
        # Scroll into view to ensure boxes are loaded
        actions = ActionChains(driver)
        actions.move_to_element(grid).perform()
        time.sleep(1)
        boxes = grid.find_elements(By.CLASS_NAME, 'browse-search__pod')
        for box in boxes:
            product = Product.from_web_element(box, n) 
            n += 1
            products.append(product)
    return n

def next_page(driver, page_num):
    pagination_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[contains(@class, 'hd-pagination__link') and contains(text(), {str(page_num)})]"))
    )

    href = pagination_link.get_attribute('href')
    driver.get(href)

def show_screen(driver):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    driver.save_screenshot(filename)
    display(Image(filename))