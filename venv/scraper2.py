"""Module scraper2 :
1. Scrape the 4 pages of the Sephora website with Selenium and Beautiful Soup
2. Print the result of the 210 or 211 make-up bases of each page in a csv2 file

1. Inspect the elements of a website to know the tags and the classes (Chrome DevTools)
2. Scrape dynamic data of the website with Beautifoul Soup and Selenium :
    - open the browser by using the dynamic method : driver.get('url')
    - get the page_source by using the method : driver.page_source
    - scroll the 4 pages
    - then pass it across BS which reads the content as Html or Xml file using its built-in XML or HTML parser
    - print the content without this elements: print(soup.text)
    - scrape all the 'a' tags and his class with: soup.find_all('a', class_='css-ix8km1')
    - print the result in a csv2 file

Copyright (c) 2021 Melissa BENARD
All Rights Reserved.
Released under the MIT license

"""

from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep


results = []
listeUrl = [
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=1",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=2",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=3",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=4"
]
driver = webdriver.Chrome(executable_path="/Applications/chromedriver")


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


def scrape(website=None, tag=None, class_=None):
    """Scrape a website with tag and class

    Args:
        website (list): The url list
        tag (str): all the tags to scrape
        class_ (str) : the specific class_ to scrape
    """
    if not (website and tag and class_) is None:
        try:
            # maximisation du navigateur Web via le webdriver
            driver.maximize_window()
            sleep(5)
            for liste in listeUrl:
                # Print each url of the Sephora website
                print(liste)
                data = []
                # To don't have a empty list
                while len(data) < 12:
                    # Open the browser and get the website
                    driver.get(liste)
                    scroll_page()
                    page = driver.page_source
                    # Pass the website across BS
                    soup = BeautifulSoup(page, 'html.parser')
                    # Scrape the tags and the class_
                    data = soup.find_all(tag, class_)
                print(data)
                for element in data:
                    if element not in results:
                        results.append(element.text)
                print("----------------------------------------------")
            print(len(results))
            driver.close()

        except Exception as e:
            print('Not successful', e)
    else:
        print('Please, enter a website')


def write_in_csv():
    """
    Print the result in a csv file
    """
    df = pd.DataFrame({'Make-up bases : ': results})
    df.to_csv('./csv/csv2.csv', index=False, encoding='utf-8')


def main():
    """The main function
    """
    try:
        scrape(listeUrl, tag='a', class_='css-ix8km1')
        write_in_csv()
    except Exception as e:
        print('Not successful', e)


if __name__ == '__main__':
    main()