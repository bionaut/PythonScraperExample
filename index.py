from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen


def create_file():
    filename = 'someFile.csv'
    f = open(filename, 'w')
    headers = 'product, link\n'
    f.write(headers)
    return f


def append_page_items(page, file):
    items = page.find_all(class_='item')
    for item in items:
        link = item.find('a').get('href')
        try:
            title = item.find(class_='title').get_text().replace('WANTED: ', '').replace(',', '|')
        except AttributeError:
            title = None
        finally:
            if title is not None:
                file.write(title + ',' + link + '\n')


def get_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    conn = urlopen(req)
    page_html = conn.read()
    conn.close()
    return bs(page_html, 'html.parser')

# get page
page = get_html('http://www.maltapark.com/listings.aspx?category=14&lt=wa')

# create new file
file = create_file()

# parse items and write them
append_page_items(page, file)

# close
file.close()
