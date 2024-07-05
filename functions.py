from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython.display import display, Image
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By

def scroll_down(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

def wait_for_element(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(selector)
        )
        return element
    except Exception as e:
        print("访问超时")
    
def wait_until_located(driver, locator, timeout=10, freq = 0.5):
    try:
        wait = WebDriverWait(driver, timeout, freq)
        element = wait.until(EC.presence_of_element_located(locator))
        return element
    
    except Exception as e:
        print("访问超时")

def wait_for_visible_elements(driver, selector, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        return element
    except Exception as e:
        print("页面元素加载出错")

def show_screen(driver):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    driver.save_screenshot(filename)
    display(Image(filename))