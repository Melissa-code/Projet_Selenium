"""Module scraper1 :
1. Scrape the 4 pages of the Sephora website with Beautiful Soup and requests
2. Print the result of the 12 download first products of each page in a csv file

Libraries - Installations required:
- pip install beautifulsoup4 pandas selenium,
- pip install requests
- pip install lxml
and use Chrome DevTools

1. Inspect the elements of a website to know the tags and the classes (Chrome DevTools)
2. Scrape data of the website with Beautifoul Soup:
    - get the website with the get request (requests.get('url')
    - then pass it across BS which reads the content as Html or Xml file using its built-in XML or HTML parser
    - print the content without this elements: print(soup.text)
    - scrape all the 'a' tags and his class with: soup.find_all('a', class_='css-ix8km1')
    - print the result in a csv1 file

Copyright (c) 2021 Melissa BENARD
All Rights Reserved.
Released under the MIT license

"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


results = []
listeUrl = [
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=1",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=2",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=3",
    "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=4"
]


def scrape(website=None, tag=None, class_=None):
    """Scrape a website with tag and class

    Args:
        website (str): The url string
        tag (str): all the tags to scrape
        class_ (str) : the specific class_ to scrape
    """
    if not (website and tag and class_) is None:
        try:
            for liste in listeUrl:
                # Print each url of the Sephora website
                print(liste)
                data = []
                # To don't have a empty list
                while len(data) < 12:
                    # Get the website
                    page = requests.get(liste)
                    # Pass the website across BS
                    soup = BeautifulSoup(page.content, 'html.parser')
                    # Scrape the tags and the class_
                    data = soup.find_all(tag, class_)
                print(data)
                print("----------------------------------------------")
                for element in data:
                    if element not in results:
                        results.append(element.text)
                print(len(results))

                # Print the result in a csv file
                df = pd.DataFrame({'Fonds de teint : ': results})
                df.to_csv('./csv/csv1.csv', index=False, encoding='utf-8')
        except Exception as e:
            print('Not successful', e)
    else:
        print('Please, enter a website')


def main():
    """The main function
    """
    try:
        scrape(listeUrl, tag='a', class_='css-ix8km1')
    except Exception as e:
        print('Not successful', e)


if __name__ == '__main__':
    main()