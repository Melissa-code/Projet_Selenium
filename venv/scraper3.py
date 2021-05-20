"""Module scraper3 :
- Print 210/211 make-up bases with their prices and their descriptions

Copyright (c) 2021 Melissa BENARD
All Rights Reserved.
Released under the MIT license

"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from time import sleep
import csv


listeUrl = [
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=1",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=2",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=3",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=4"
]
driver = webdriver.Chrome(executable_path="/Applications/chromedriver")
total_infos_products = []


def scroll_page():
    """
    Handle dynamic page content loading - using Selenium
    """
    # define the initial page height for 'while' loop
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # scroll the page to the bottom
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
        sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_product_info(a_list):
    """Get all information for a given product's DOM

    :return: name, price, description_subdiv
    """
    sleep(5)
    for index, link in enumerate(a_list):
        print(index, "URL: ", link['href'])
        driver.get(link['href'])
        scroll_page()
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        name = soup.find('a', class_='css-nc375s')
        print(name.text)

        price = soup.find('b', class_='css-0') or soup.find('b', class_='css-5fq4jh')
        print(price.text)

        description = soup.find('div', class_='css-cnj3lw') or soup.find('div', class_='css-1mzu3ip') or soup.find(
            'div', class_='css-m5jpyl') or soup.find('div', class_='css-10bjc73') or soup.find('div', class_='css-1bropq9')
        description_subdiv = description.div
        print(description_subdiv.text)

        image = soup.find('img', class_='css-1rovmyu')
        print(image)

        print("------------------------------------------------------")

        write_to_csv(name, price, description_subdiv, image)
    return name, price, description_subdiv, image


def scrape(website, tag1, class_1):
    """Scrape a website with tag and class

    Args:
        :param website:  The url list
        :param class_1: the specific class_ to scrape
        :param tag1: all the tags to scrape
    """
    try:
        # maximisation du navigateur Web via le webdriver
        driver.maximize_window()
        sleep(5)
        for url in listeUrl:
            # Print each url of the Sephora website
            print(url)
            a_list = []
            # To don't have a empty list
            while len(a_list) < 12:
                # Open the browser and get the website
                driver.get(url)
                scroll_page()
                page = driver.page_source
                # Pass the website across BS
                soup = BeautifulSoup(page, 'html.parser')
                # Scrape the tags and the class_
                a_list = soup.find_all(tag1, class_1)
                # Pass a list of a tag :
                get_product_info(a_list)

        driver.close()

    except Exception as e:
        print('Not successful', e)


def write_to_csv(name, price, description_subdiv, image):
    """Print the infos about each product to a csv file

    :param name
    :param price
    :param description_subdiv
    :param image
    """
    name = name.text
    price = price.text
    description_subdiv = description_subdiv.text
    image = image.text
    infos = [name, price, description_subdiv, image]
    for info in infos:
        if infos not in total_infos_products:
            total_infos_products.append(info)

    df = pd.DataFrame(total_infos_products)
    df.to_csv('./csv/csv3.csv', index=False, encoding='utf-8')


def main():
    """The main function
    """
    try:
        scrape(listeUrl, 'a', 'css-ix8km1')
    except Exception as e:
        print('Not successful', e)


if __name__ == '__main__':
    main()
