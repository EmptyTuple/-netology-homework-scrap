import requests
from bs4 import BeautifulSoup
import re
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all'
BASE_URL = 'https://habr.com'
HEADERS = Headers(os="mac", headers=True).generate()


def get_articles():
    response = requests.get(URL, headers=HEADERS)
    try:
        response.raise_for_status()
    except Exception as ex:
        print(f'Error occured: {str(ex)}')

    text = response.text
    soup = BeautifulSoup(text, features='html.parser')
    row_articles = soup.find_all('article')
    return row_articles

def split_article(text):
    raw_split = re.split('\W+', text)
    full_split = {word for word in raw_split if word}
    return full_split

def search_articles():
    for article in get_articles():
        article_date = article.find('time').attrs['title'].split(', ')[0]
        article_name = article.find('h2').find('span').text
        article_href = article.find('h2').find('a').attrs['href']
        article_link = f'{BASE_URL}{article_href}'
        article_preview = article.find(True, 
                    {"class": ['article-formatted-body article-formatted-body article-formatted-body_version-2',
                    'article-formatted-body article-formatted-body article-formatted-body_version-1']}).text
        if split_article(article_preview) & set(KEYWORDS):
            print(f'{article_date} - {article_name} - {article_link}')
        else:
            res = requests.get(article_link, headers=HEADERS)
            try:
                res.raise_for_status()
            except Exception as ex:
                print(f'Article not found: {str(ex)}')
            full_text = res.text
            fsoup = BeautifulSoup(full_text, features='html.parser')
            article_text = fsoup.select('div[class*="article-formatted-body"]')[0].text
            if split_article(article_text) & set(KEYWORDS):
                print(f'{article_date} - {article_name} - {article_link}')      

def main():
    search_articles()

if __name__ == '__main__':
    main()

# def paginate(url): 
    
#     res = requests.get(url, headers=HEADERS)
#     soup = BeautifulSoup(res.text, 'html.parser')   
#     next_page = soup.find('a', class_='tm-pagination__navigation-link tm-pagination__navigation-link_active', id='pagination-next-page')
#     all_pages = []
#     if next_page != None:
        
#         next_href = next_page.attrs['href']
#         next_link = f'{BASE_URL}{next_href}'
#         all_pages.append(next_link)
#         paginate(next_link)
#     return all_pages
