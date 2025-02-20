#import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

def load_dynamic(url):

    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()

        #parse
        soup = BeautifulSoup(response.html.html, "html.parser")
        print(soup.prettify())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


load_dynamic("https://www.google.com/search?q=intext:@%22yahoo%7Cgmail%7Chotmail%22.com+ext:csv+%7C+ext:txt&start=0")
