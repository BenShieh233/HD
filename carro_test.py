import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

if __name__ == "__main__":
    print("hello world")
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    driver.get('https://www.homedepot.com/p/CARRO-Modena-52-in-Indoor-White-10-Speed-DC-Motor-Flush-Mount-Ceiling-Fan-with-Remote-Control-HC523P-N10-W1-1-FM/321644000')
    