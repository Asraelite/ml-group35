import requests
from bs4 import BeautifulSoup
import json

class Webscraper:
    def __init__(self):
        self.scraped_data = {}

    def scrape_indpendent_co_uk_website(self):
        URL = "https://www.independent.co.uk/life-style/gadgets-and-tech/crypto-price-update-bitcoin-ethereum-b1950457.html"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        date = ''
        for e in soup.find('div', class_="sc-gmuVcf jygeSc").text.split()[8:11]:
            date = date + e.split(',')[0] + ' '

        text_body = []
        text_body.append(soup.find('h2', class_="sc-iRjPif sc-jEAxDh liPMkz casxcE").text)

        p_text = []
        for text in soup.find_all('p'):
            p_text.append(text.text)

        for index in [2, 4, 5, 7, 8, 9]:
            text_body.append(p_text[index])

        self.scraped_data['1'] = {
            'source': URL,
            'date': date[:-1],
            'text': ' '.join(text_body),
        }

    def scrape_theconversation_website(self):
        URL = 'https://theconversation.com/ethereum-the-transformation-that-could-see-it-overtake-bitcoin-170316'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        for p in soup.find_all('p'):
            if p.text.startswith('Either'):
                self.scraped_data['2'] = {
                    'source': URL,
                    'date': ' '.join(soup.find_all('time')[0].text.split()[:-2]),
                    'text': ' '.join(p.text.split()[2:]),
                }
                break

    def scrape_jeangalea_website(self):
        URL = 'https://jeangalea.com/ethereum-staking/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        text_body = []

        for text in soup.find_all('span'):
            if text.text.startswith('Ethereum 2.0 is a major network upgrade') or text.text.startswith(
                    'ETH 2.0 will also fundamentally'):
                text_body.append(text.text)

        self.scraped_data['3'] = {
            'source': URL,
            'date': soup.find('p', class_='entry-meta').find('time').text,
            'text': ''.join(text_body),
        }

    def write_data_to_json(self):
        with open('scraped_data.json', 'w') as outfile:
            json.dump(self.scraped_data, outfile, indent=4)

scarper = Webscraper()
scarper.scrape_indpendent_co_uk_website()
scarper.scrape_theconversation_website()
scarper.scrape_jeangalea_website()
scarper.write_data_to_json()

