from scraper import Scraper
from product_class import Product

import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import sqlalchemy
import uuid

from concurrent.futures import ThreadPoolExecutor, as_completed

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dve-shm-uage')

def log_progress(message, filename='exceptions.txt'):
    with open(filename, 'a') as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def log_exception(exception, message, filename='exceptions.txt'):
    """Log an exception to a text file."""
    with open(filename, 'a') as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message} - {str(exception)}\n")

def click_element(driver, element):
    """Click an element using JavaScript."""
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)  # Wait for the click to be processed

def scroll_slowly(driver, direction='down'):
    """
    Function to scroll the page slowly in the specified direction ('down' or 'up').
    """
    scroll_pause_time = 0.5
    screen_height = driver.execute_script("return window.innerHeight;")  # get the screen height of the web
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    
    if direction == 'down':
        for i in range(0, scroll_height, screen_height):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(scroll_pause_time)
    elif direction == 'up':
        for i in range(scroll_height, 0, -screen_height):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(scroll_pause_time)
    else:
        raise ValueError("Direction must be 'down' or 'up'.")
    
def scroll_to_element(driver, element):
    """Scroll the page to the specific element."""
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
    time.sleep(2)  # Wait for the scrolling to complete

def wait_for_element(driver, xpath, timeout=10):
    """Wait for an element to be present and return it."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException as e:
        log_exception(e, "Timeout to wait for the element, please retry")
        return None

def scrape_product(driver):
    try:
        model_selector = '//*[@id="product-overview-desktop-content"]/div/div[1]/div[3]/div/div/div[2]/h2/span'
        model_element = wait_for_element(driver, model_selector)
        scroll_to_element(driver, model_element)
        model = model_element.text
    except Exception as e:
        log_exception(e, "failed to locate the model number on the webpage")
        model = None
        pass

    try:
        SKU_selector = '//*[@id="product-overview-desktop-content"]/div/div[1]/div[3]/div/div/div[3]/h2/span'
        SKU_element = wait_for_element(driver, SKU_selector)
        SKU = SKU_element.text
    except Exception as e:
        log_exception(e, "failed to locate the SKU number on the webpage")
        SKU = None
        pass

    try:
        int_selector = '//*[@id="product-overview-desktop-content"]/div/div[1]/div[3]/div/div/div[1]/h2/span' 
        int_element = wait_for_element(driver, int_selector)
        int_num = int_element.text
        # print("find the internet number")
    except Exception as e:
        log_exception(e, "failed to locate the Internet Number on the webpage")
        int_num = None
        pass

    return {'SKU':SKU, 'Model':model, 'Internet_Number': int_num}

def scrape_reviews(driver):
    try:
        rating_selector = '//*[@id="ratings-and-reviews"]/div[1]/div[1]/ul/li[1]/div/span[1]' 
        rating_element = wait_for_element(driver, rating_selector)
        scroll_to_element(driver, rating_element)
        rating = rating_element.text

    except Exception as e:
        log_exception(e, "failed to locate Rating on the webpage")
        rating = None
        pass 

    try:
        dropdown = Select(driver.find_element(By.CLASS_NAME, "drop-down__select"))
        dropdown.select_by_value("oldest")
        time.sleep(5)
        review_date_selector = '//*[@id="ratings-and-reviews"]/div[5]/div[1]/div[1]/div[1]/div/span'
        review_date_element = wait_for_element(driver, review_date_selector)
        review_date = review_date_element.text

    except Exception as e:
        log_exception(e, "failed to locate Review Date on the webpage")
        review_date = None

    try:
        first_review_selector = '//*[@id="ratings-and-reviews"]/div[5]/div[1]/div[1]/div[2]/div/div/div[1]'
        review_content_element = driver.find_element(By.XPATH, first_review_selector)
        review_content = review_content_element.text

    except Exception as e:
        log_exception(e, "failed to locate any review content on this webpage")
        review_content = None


    return {'Rate':rating, 'Review_Date':review_date, 'Review_Content': review_content}

def fetch_detail(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    log_progress(f"Now visiting url: {url}")
    scroll_slowly(driver)

    product_details = {}
    review_details = {}
    try:
        product_selector = '//*[@id="product-section-overview"]/div/div[1]'
        product_element = wait_for_element(driver, product_selector)
        scroll_to_element(driver, product_element)
        time.sleep(2)
        click_element(driver, product_element)
        product_details = scrape_product(driver)
        if all(value is None for value in product_details.values()):
            driver.refresh()
            time.sleep(5)
            product_element = wait_for_element(driver, product_selector)
            scroll_to_element(driver, product_element)
            time.sleep(2)
            click_element(driver, product_element)
            product_details = scrape_product(driver)

        else:
            log_progress("Successfully located product element.")

    except Exception as e:
        log_exception(e, "failed to locate product element on the webpage")
        pass

    try:
        review_selector = '//*[@id="product-section-rr"]/div/div[1]'
        review_element = wait_for_element(driver, review_selector)
        scroll_to_element(driver, review_element)
        time.sleep(2)
        click_element(driver, review_element)
        review_details = scrape_reviews(driver)
        if all(value is None for value in review_details.values()):
            driver.refresh()
            time.sleep(5)
            review_element = wait_for_element(driver, review_selector)
            scroll_to_element(driver, review_element)
            time.sleep(2)
            click_element(driver, review_element)
            review_details = scrape_reviews(driver)
        else:
            log_progress("Successfully located review element.")

    except Exception as e:
        log_exception(e, "failed to locate the review element on the webpage")
        pass
    
    # Combine product_details and review_details
    details = {**product_details, **review_details}
    if any(value is None for value in details.values()):
        log_progress(f"failed to scrape the information for product url:{url}")
        
    driver.close()
    driver.quit()

    return details

def fetch_details_for_all_rows(df):
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_detail, row['href']): index for index, row in df.iterrows()}
        for future in as_completed(future_to_url):
            index = future_to_url[future]
            try:
                detail_info = future.result()
                df.at[index, 'SKU'] = detail_info['SKU']
                df.at[index, 'Model'] = detail_info['Model']
                df.at[index, 'OMSID'] = detail_info['Internet_Number']
                df.at[index, 'Rating'] = detail_info['Rate']
                df.at[index, 'Date_of_first_review'] = detail_info['Review_Date']
                df.at[index, 'Review_content'] = detail_info['Review_Content']
                log_progress(f"Currently processing row {index}")
            except Exception as e:
                log_exception(e, f"Error processing row {index}")
    return df

def get_table(url):
    scraper = Scraper(url)
    scraper.scrape(start_page=1, end_page=5)
    df = scraper.to_dataframe()

    df['Rating'] = None
    df['SKU'] = None
    df['Model'] = None
    df['OMSID'] = None
    df['Date_of_first_review'] = None
    df['Review_content'] = None

    df_details = fetch_details_for_all_rows(df).reset_index()

    return df_details




def main():

    conn = sqlalchemy.create_engine(
        'mysql+mysqlconnector://root:0803@localhost:3306/hd_products')
    # Function to insert data into the table
    def insert_data(df, table_name):
        df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df.to_sql(table_name, con=conn, if_exists='append', index=False)


    current_time = time.strftime('%Y-%m-%d_%H-%M-%S')

    base_url_1 = 'https://www.homedepot.com/b/Lighting-Ceiling-Fans-Ceiling-Fans-With-Lights/N-5yc1vZcjnu?NCNI-5&searchRedirect=ceiling%20fan%20with%20lights&semanticToken=k27r10r00f22000000000e_202407051741572580635995840_us-central1-bz9l%20k27r10r00f22000000000e%20%3E%20st%3A%7Bceiling%20fan%20with%20lights%7D%3Ast%20ml%3A%7B24%7D%3Aml%20nr%3A%7Bceiling%20fan%20with%20lights%7D%3Anr%20nf%3A%7Bn%2Fa%7D%3Anf%20qu%3A%7Bceiling%20fan%20with%20lights%7D%3Aqu%20ie%3A%7B0%7D%3Aie%20qr%3A%7Bceiling%20fan%20with%20lights%7D%3Aqr'
    filename1 = f"{current_time}_ceiling_fans_with_lights.xlsx"
    df1 = get_table(base_url_1)
    df1.to_excel(filename1, index=False)
    insert_data(df1, 'ceiling_fans_with_lights')

    base_url_2 = 'https://www.homedepot.com/b/Lighting-Ceiling-Fans/N-5yc1vZbvlq?catStyle=ShowProducts'
    filename2 = f"{current_time}_ceiling_fans.xlsx"
    df2 = get_table(base_url_2)
    df2.to_excel(filename2, index=False)
    insert_data(df1, 'ceiling_fans')

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)

    upload_file_1 = filename1
    upload_file_2 = filename2
    gfile1 = drive.CreateFile({'parents':[{'id':'1tiu74hnlyNGhVOBYQN8SNdnmbKXBr_th'}]})
    gfile1.SetContentFile(upload_file_1)
    gfile1.Upload()

    gfile2 = drive.CreateFile({'parents':[{'id':'1tiu74hnlyNGhVOBYQN8SNdnmbKXBr_th'}]})
    gfile2.SetContentFile(upload_file_2)
    gfile2.Upload()



if __name__ == '__main__':
    main()