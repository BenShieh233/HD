import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebPage:
    
    def __init__(self, 
                 price = None, 
                 parent_id = None,
                 model = None,
                 sku = None,
                 rating = None,
                 product_name = None,
                 status = None,
                 review_num = None,
                ):
        
        self.price = price
        self.parent_id = parent_id
        self.model = model
        self.sku = sku
        self.rating = rating
        self.product_name = product_name
        self.status = status
        self.review_num = review_num

    @staticmethod
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

    @staticmethod
    def wait_for_element(driver, xpath, timeout=30):
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )    
    
    @classmethod
    def from_web_element(cls, driver):

        price_selector = '//*[@id="standard-price"]/div'
        parent_id_selector = '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[1]/h2/span'
        model_selector = '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[2]/h2/span'
        sku_selector = '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/h2/span'
        product_name_selector = '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div/div[1]/div/div[3]'
        status_selector = '//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div[1]/div/div/div/div[1]'
        rating_selector = '//*[@id="ratings-and-reviews-accordion-title"]/div/div/div/p'

        try:
            price = cls.wait_for_element(driver, price_selector)
            price = price.text.replace('\n', '').strip()
        except Exception as e:
            price = None

        try:
            parent_id = cls.wait_for_element(driver, parent_id_selector)
            parent_id = parent_id.text
        except Exception as e:
            parent_id = None

        try:
            model = cls.wait_for_element(driver, model_selector)
            model = model.text
        except Exception as e:
            model = None
        
        try:
            sku = cls.wait_for_element(driver, sku_selector)
            sku = sku.text
        except Exception as e:
            sku = None

        try:
            product_name = cls.wait_for_element(driver, product_name_selector)
            product_name = product_name.text
        except Exception as e:
            product_name = None

        try:
            status = cls.wait_for_element(driver, status_selector)
            status = status.text

        except Exception as e:
            status = None

        try:
            cls.scroll_slowly(driver)
            rating = cls.wait_for_element(driver, rating_selector)
            rating = rating.text

        except Exception as e:
            rating = None

        return cls(price=price, 
                   parent_id=parent_id, 
                   model=model, 
                   sku=sku,
                   product_name=product_name,
                   status=status,
                   rating=rating)
    
    def __repr__(self):

        return f"Product(price={self.price}, parent_id={self.parent_id}, model={self.model}, sku={self.sku}, product_name={self.product_name}, status={self.status})"
    

if __name__ == "__main__":

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    driver.get('https://www.homedepot.com/p/CARRO-Modena-52-in-Indoor-White-10-Speed-DC-Motor-Flush-Mount-Ceiling-Fan-with-Remote-Control-HC523P-N10-W1-1-FM/321644000')

    webpage = WebPage.from_web_element(driver)
    print(webpage)


            

