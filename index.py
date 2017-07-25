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


# list of pages
list_of_pages = [
    'http://www.maltapark.com/listings.aspx?category=14&lt=wa',
    'http://www.maltapark.com/listings.aspx?category=14&lt=wa&page=2&nr=5029&wr=63&bn=15',
    'http://www.maltapark.com/listings.aspx?category=14&lt=wa&page=3&nr=5029&wr=63&bn=15'
    'http://www.maltapark.com/listings.aspx?category=14&lt=wa&page=4&nr=5029&wr=63&bn=15'
]

# create new file
file = create_file()


for page in list_of_pages:
    cur_page = get_html(page)
    append_page_items(cur_page, file)


# close
file.close()
