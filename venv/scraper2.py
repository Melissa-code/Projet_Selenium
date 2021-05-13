"""Module scraper2 :
1. Scrape the 4 pages of the Sephora website with Beautiful Soup and Selenium
2. Print the result of the 12 download first products (make-up bases) of each page in a csv2 file

1. Inspect the elements of a website to know the tags and the classes (Chrome DevTools)
2. Scrape data of the website with Beautifoul Soup:
    - open the browser by using the dynamic method : driver.get('url')
    - get the page_source by using the method : driver.page_source
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
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from time import sleep


results = []
listeUrl = [
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=1",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=2",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=3",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=4"
]


def write_in_csv():
    """
    Print the result in a csv file
    """
    df = pd.DataFrame({'Fonds de teint : ': results})
    df.to_csv('./csv/csv2.csv', index=False, encoding='utf-8')


def scrape(website=None, tag=None, class_=None):
    """Scrape a website with tag and class

    Args:
        website (list): The url list
        tag (str): all the tags to scrape
        class_ (str) : the specific class_ to scrape
    """
    if not (website and tag and class_) is None:
        try:
            # Create a webdriver object
            driver = webdriver.Chrome(executable_path="/Applications/chromedriver")
            for liste in listeUrl:
                # Print each url of the Sephora website
                print(liste)
                data = []
                # To don't have a empty list
                while len(data) < 12:
                    # Open the browser and get the website
                    driver.get(liste)
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