import requests
from bs4 import BeautifulSoup


base_url = 'http://quotes.toscrape.com/'

def get_urls(base_url):
    urls = []
    page_number = 1
    page_exists = True
  
    while page_exists:
        url = f'{base_url}page/{page_number}/'
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

# url = 'http://quotes.toscrape.com/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('span', class_='text')
# authors = soup.find_all('small', class_='author')
# tags = soup.find_all('div', class_='tags')

# for i in range(0, len(quotes)):
#     print(quotes[i].text)
#     print('--' + authors[i].text)
#     tagsforquote = tags[i].find_all('a', class_='tag')
#     for tagforquote in tagsforquote:
#         print(tagforquote.text)
#     break


if __name__ == '__main__':
    urls = get_urls(base_url)
    for url in urls:
        print(url)