import requests
import re

from bs4 import BeautifulSoup


def get_page_urls(base_url: str):
    urls = []
    page_number = 1
    page_exists = True
  
    while page_exists:
        url = f'{base_url}/page/{page_number}/'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                next_button = soup.find('li', class_='next')
                record = soup.find('div', class_='quote')
                if not next_button and not record:
                    break
                urls.append(url)
                page_number += 1
                continue
        except Exception:
            print('Page processing error')
            page_exists = False
    return urls


def get_author_urls(page_urls: list(str), base_url: str):
    author_urls = []
    
    for url in page_urls:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        links = soup.select("div[class=quote] span a")
        for link in links:
            author_urls.append(base_url + link["href"] + '/')       
    return set(author_urls)
            

def get_author_info(author_urls: list):
    authors = []
    
    for url in author_urls:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        fullname = soup.find('h3', class_='author-title').get_text()
        born_date = soup.find('span', class_='author-born-date').get_text()
        born_location = soup.find('span', class_='author-born-location').get_text()[3:]
        description = soup.find('div', class_='author-description').get_text().replace('\n', '').strip().replace('\\', '')
        author = {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }
        authors.append(author)
    return authors


def tags_to_string(soup_object):
    tagsforquote = soup_object.find_all('a', class_='tag')
    tag_list = [tagforquote.text for tagforquote in tagsforquote]
    return tag_list


def spider(urls: list):
    authors = []
    quotes = []
    
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags_object = soup.find_all('div', class_='tags')
        tags = tags_to_string(tags_object)

# for i in range(0, len(quotes)):
#     print(quotes[i].text)
#     print('--' + authors[i].text)
#     tagsforquote = tags[i].find_all('a', class_='tag')
#     for tagforquote in tagsforquote:
#         print(tagforquote.text)
#     break


if __name__ == '__main__':
    
    base_url = 'http://quotes.toscrape.com'
    
    page_urls = get_page_urls(base_url)
    author_urls = get_author_urls(page_urls, base_url)
    authors = get_author_info(author_urls)
    
    
    