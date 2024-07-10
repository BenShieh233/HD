from scraper import Scraper
import time

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from IPython.display import display, Image
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# import time
# import pandas as pd

# from product_class import Product

# def visit_page(driver, url):
#     driver.get(url)
#     time.sleep(5)


# def get_products(driver, products, n):
#     grids = driver.find_elements(By.CSS_SELECTOR, '[id^="browse-search-pods-"]')
#     for grid in grids:
#         # Scroll into view to ensure boxes are loaded
#         actions = ActionChains(driver)
#         actions.move_to_element(grid).perform()
#         time.sleep(1)
#         boxes = grid.find_elements(By.CLASS_NAME, 'browse-search__pod')
#         for box in boxes:
#             product = Product.from_web_element(box, n) 
#             n += 1
#             products.append(product)
#     return n

# def next_page(driver, page_num):
#     pagination_link = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, f"//a[contains(@class, 'hd-pagination__link') and contains(text(), {str(page_num)})]"))
#     )

#     href = pagination_link.get_attribute('href')
#     driver.get(href)

# def show_screen(driver):
#     timestamp = time.strftime("%Y%m%d-%H%M%S")
#     filename = f"screenshot_{timestamp}.png"
#     driver.save_screenshot(filename)
#     display(Image(filename))


# def main(options):
#     products = []
#     n = 1
#     driver = webdriver.Chrome(options=options)
#     initial_url = 'https://www.homedepot.com/b/Lighting-Ceiling-Fans-Ceiling-Fans-With-Lights/N-5yc1vZcjnu?NCNI-5&searchRedirect=ceiling%20fan%20with%20lights&semanticToken=k27r10r00f22000000000e_202407051741572580635995840_us-central1-bz9l%20k27r10r00f22000000000e%20%3E%20st%3A%7Bceiling%20fan%20with%20lights%7D%3Ast%20ml%3A%7B24%7D%3Aml%20nr%3A%7Bceiling%20fan%20with%20lights%7D%3Anr%20nf%3A%7Bn%2Fa%7D%3Anf%20qu%3A%7Bceiling%20fan%20with%20lights%7D%3Aqu%20ie%3A%7B0%7D%3Aie%20qr%3A%7Bceiling%20fan%20with%20lights%7D%3Aqr'
#     visit_page(driver, initial_url)
#     n = get_products(driver, products, n)
#     for page_num in range(2, 6):
#         next_page(driver, page_num)
#         n = get_products(driver, products, n)
#     driver.quit()

#     product_dicts = [product.to_dict() for product in products]
#     df = pd.DataFrame(product_dicts).set_index('Number')
#     df.to_csv('HD_products.csv')


if __name__ == '__main__':

    base_url = 'https://www.homedepot.com/b/Lighting-Ceiling-Fans-Ceiling-Fans-With-Lights/N-5yc1vZcjnu?NCNI-5&searchRedirect=ceiling%20fan%20with%20lights&semanticToken=k27r10r00f22000000000e_202407051741572580635995840_us-central1-bz9l%20k27r10r00f22000000000e%20%3E%20st%3A%7Bceiling%20fan%20with%20lights%7D%3Ast%20ml%3A%7B24%7D%3Aml%20nr%3A%7Bceiling%20fan%20with%20lights%7D%3Anr%20nf%3A%7Bn%2Fa%7D%3Anf%20qu%3A%7Bceiling%20fan%20with%20lights%7D%3Aqu%20ie%3A%7B0%7D%3Aie%20qr%3A%7Bceiling%20fan%20with%20lights%7D%3Aqr'
    scraper = Scraper(base_url)
    scraper.scrape(start_page=1, end_page=5)
    df = scraper.to_dataframe()
    df.to_csv('HD_products.csv')