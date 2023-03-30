import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from web_scraper_project import utils_gcs

from dagster import asset
from time import sleep

from dagster._utils import file_relative_path
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_project

DBT_PROJECT_DIR = file_relative_path(__file__, "../../bigquery_scraper")
DBT_PROFILES_DIR = file_relative_path(__file__, "../../bigquery_scraper/config")

# all assets live in the default dbt_schema
dbt_assets = load_assets_from_dbt_project(
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR
)

@asset(key_prefix=["allinone"])
def allinone():
    listings = []

    driver = webdriver.Firefox()

    url = "https://webscraper.io/test-sites/e-commerce/allinone"

    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
    driver.get(url)

    prices = driver.find_elements(By.XPATH,'//*[@class="pull-right price"]')
    products = driver.find_elements(By.XPATH,'//*[@class="title"]')
    descrptions = driver.find_elements(By.XPATH,'//*[@class="description"]')
    ratings = driver.find_elements(By.XPATH,'//*[@class="pull-right"]/following::p[@data-rating]') 


    for product, price, description,rating in zip(products,prices,descrptions,ratings):
        text_product = product.get_attribute('title')
        text_price = price.text
        text_description = description.text
        text_rating = rating.get_attribute('data-rating')
        listin_dict = {"Product": text_product,
                    "Price": float(text_price[1:]),
                    "Description": text_description,
                    "Rating": int(text_rating)}
        listings.append(listin_dict)
    driver.close()
    driver.quit()

    credentials = utils_gcs.get_credentials_from_env()

    listing_df = pd.DataFrame(listings)

    destination_table = 'allinone.allinone'
    project_id = 'dataquerytask'
    
    listing_df.to_gbq(destination_table, project_id, if_exists='replace', location='US', progress_bar=True, credentials=credentials)


@asset(key_prefix=["allinone"])
def allinone_popup():

    listings = []

    driver = webdriver.Firefox()

    url = "https://webscraper.io/test-sites/e-commerce/allinone-popup-links"

    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
    driver.get(url)

    # storing the current window handle to get back to dashboard
    main_page = driver.current_window_handle

    prices = driver.find_elements(By.XPATH,'//*[@class="pull-right price"]')
    products = driver.find_elements(By.XPATH,'//*[@class="title"]') 
    descrptions = driver.find_elements(By.XPATH,'//*[@class="description"]')
    ratings = driver.find_elements(By.XPATH,'//*[@class="pull-right"]/following::p[@data-rating]') 


    for product, price, description,rating in zip(products,prices,descrptions,ratings):
        popup_product = product.click()
        sleep(1)
        for handle in driver.window_handles:
            if handle != main_page:
                product_popup = handle
        driver.switch_to.window(product_popup)
        text_product = driver.find_element(By.XPATH,'//*[@class="pull-right price"]/following::h4').text
        driver.close()
        driver.switch_to.window(main_page)

        text_price = price.text
        text_description = description.text
        text_rating = rating.get_attribute('data-rating')
        listin_dict = {"Product": text_product,
                    "Price": float(text_price[1:]),
                    "Description": text_description,
                    "Rating": int(text_rating)}
        listings.append(listin_dict)
    driver.close()
    driver.quit()

    credentials = utils_gcs.get_credentials_from_env()

    listing_df = pd.DataFrame(listings)

    destination_table = 'allinone.allinone_popup'
    project_id = 'dataquerytask'
    
    listing_df.to_gbq(destination_table, project_id, if_exists='replace', location='US', progress_bar=True, credentials=credentials)
