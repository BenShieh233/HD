from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class Product:
    brand_counts = {}

    def __init__(self, NO = None, label=None, price=None, brand=None, title=None, href=None, review_num = None, first_review = None, first_review_date = None):
        self.NO = NO
        self.label = label
        self.price = price
        self.brand = brand
        self.title = title
        self.href = href
        self.review_num = review_num
        self.first_review = first_review
        self.first_review_date = first_review_date

        # Update brand counts when brand is present
        if self.brand:
            self.update_brand_count()

    def update_brand_count(self):
        if self.brand in Product.brand_counts:
            Product.brand_counts[self.brand] += 1
        else:
            Product.brand_counts[self.brand] = 1

    def to_dict(self):
        return {
            'Number': self.NO,
            'Label': self.label,
            'Brand': self.brand,
            'Title': self.title,
            'price': self.price,
            'Review_Number': self.review_num,
            'href': self.href
        }

    @classmethod
    def get_brand_counts(cls):
        return cls.brand_counts

    @classmethod 
    def from_web_element(cls, box, NO):

        try:
            # Extract label
            label_element = 'div.sui-absolute.sui-flex.sui-z-10.sui-left-0[data-testid="pod-sticker"] div.sui-pl-1.sui-pt-2'
            label_block = box.find_element(By.CSS_SELECTOR, label_element)
            label = label_block.text.strip()
        except Exception as e:
            label = None

        try: 
            # Extract price
            price_element = '.price-format__main-price'
            price_block = box.find_element(By.CSS_SELECTOR, price_element)
            price = price_block.text.replace('\n', '').strip()
        except Exception as e:
            price = None

        try:
            # Extract brandname
            brand_element = 'p[data-testid="attribute-brandname-above"].sui-text-primary.sui-font-w-bold'
            brand_block = box.find_element(By.CSS_SELECTOR, brand_element)
            brand = brand_block.text.strip()
        except Exception as e:
            brand = None

        try:
            # Extract title
            title_element = 'span.sui-text-primary.sui-font-regular.sui-mb-1.sui-line-clamp-5.sui-text-ellipsis.sui-inline'
            title_block = box.find_element(By.CSS_SELECTOR, title_element)
            title = title_block.text.strip()
        except Exception as e:
            title = None

        try:
            review_num_element = 'span.sui-font-regular.sui-text-xs.sui-leading-tight.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-text-primary'
            review_num_block = box.find_element(By.CSS_SELECTOR, review_num_element)
            review_num = review_num_block.text.strip("()")
        except Exception as e:
            review_num = None

        try:
            # Extract href link
            href_element = 'a.sui-font-regular.sui-text-base.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-text-primary.focus-visible\\:sui-bg-focus.focus-visible\\:sui-outline-none.hover\\:sui-underline'
            href_block = box.find_element(By.CSS_SELECTOR, href_element)
            href = href_block.get_attribute('href')
        except Exception as e:
            href = None

        return cls(NO = NO, label=label, price=price, brand=brand, title=title, review_num=review_num, href=href)
    


    def __repr__(self):
        return f"Product(NO={self.NO}, brand={self.brand}, title={self.title}, price={self.price}, label={self.label}, review_number = {self.review_num}, href={self.href})"

