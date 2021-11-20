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

    def reviews(self):
        URL = "https://www.gartner.com/reviews/market/blockchain-platforms/vendor/ethereum-foundation/product/ethereum/reviews"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.find('ul', class_='all-reviews'))
        string_to_consider = ''
        for text in soup.find_all('script'):
            if text.contents:
                if text.contents[0].strip().startswith('var pre'):
                    string_to_consider = text.contents[0].strip()
                    x = text.contents[0].strip()
        text = 'go'
        index_1 = 0
        start = 0
        all_reviews = []
        while text != "":
            index_1 = string_to_consider.find('reviewHeadline', index_1 + start)
            index_2 = string_to_consider.find('reviewHeadline', index_1 + 1)
            text = string_to_consider[index_1: index_2]
            all_reviews.append(text)
            start = 1
            print(string_to_consider[index_1: index_2])

        for review in all_reviews:
            print(review)
        del all_reviews[0]
        del all_reviews[5]
        del all_reviews[5]
        del all_reviews[5]
        del all_reviews[5]
        del all_reviews[5]
        reviews_list = {}
        c=1
        for review in all_reviews:
            # print(review)
            print()
            print()
            for parts in review.split('",'):
                # if 'Headline' in parts.split(':')[0]:
                #     print(parts.split(':')[0][:-2])
                #     print(parts.split(':')[1].split('"')[1][:-2])
                if 'Summary' in parts.split(':')[0]:
                    # print(parts.split(':')[0].split('"')[1][:-1])
                    # print(parts.split(':')[1].split('"')[1][:-2])
                    reviews_list[str(c)] = parts.split(':')[1].split('"')[1][:-2]
                    c += 1

        print(reviews_list)
        with open('scraped_reviews.json', 'w') as outfile:
            json.dump(reviews_list, outfile, indent=4)


    def reviews_1(self):
        URL = "https://www.gartner.com/reviews/market/blockchain-platforms/vendor/ethereum-foundation/product/ethereum/likes-dislikes"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        print(soup.prettify())
        string_to_consider = ''
        for text in soup.find_all('script'):
            if text.contents:
                if text.contents[0].strip().startswith('var pre'):
                    string_to_consider = text.contents[0].strip()
                    x = text.contents[0].strip()

        print(string_to_consider)
        text = 'go'
        index_1 = 0
        start = 0
        all_likes = []
        while text != "":
            index_1 = string_to_consider.find('lessonslearned-like-most', index_1 + start)
            index_2 = string_to_consider.find('lessonslearned-like-most', index_1 + 1)
            text = string_to_consider[index_1: index_2]
            all_likes.append(text.split('}')[0])
            start = 1
            print(string_to_consider[index_1: index_2].split('}')[0])
        text = 'go'
        index_1 = 0
        start = 0
        all_dislikes = []
        while text != "":
            index_1 = string_to_consider.find('lessonslearned-dislike-most', index_1 + start)
            index_2 = string_to_consider.find('lessonslearned-dislike-most', index_1 + 1)
            text = string_to_consider[index_1: index_2]
            all_dislikes.append(text.split('}')[0])
            start = 1
            print(string_to_consider[index_1: index_2].split('}')[0])

        all_reviews = {}
        likes = []
        for like in all_likes[:-1]:
            print(like.split(':')[1].split('"')[1][0:-1].strip())
            likes.append(like.split(':')[1].split('"')[1][0:-1].strip())
        dislikes = []
        for dislike in all_dislikes[:-1]:
            print(dislike.split(':')[1].split('"')[1][0:-1].strip())
            dislikes.append(dislike.split(':')[1].split('"')[1][0:-1].strip())
        all_reviews['Likes'] = likes

        all_reviews['DisLikes'] = dislikes

        with open('likes_and_dislikes.json', 'w') as outfile:
            json.dump(all_reviews, outfile, indent=4)


    def write_data_to_json(self):
        with open('scraped_data.json', 'w') as outfile:
            json.dump(self.scraped_data, outfile, indent=4)


scarper = Webscraper()
# scarper.scrape_indpendent_co_uk_website()
# scarper.scrape_theconversation_website()
# scarper.scrape_jeangalea_website()
# scarper.write_data_to_json()
scarper.reviews_1()
