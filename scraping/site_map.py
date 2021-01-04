import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re

internal_urls = set()
external_urls = set()

total_urls_visited = 0

def is_image(values):
    image_extensions = r".jpg|.jpeg|.JPEG|.png|.svg|.JPG"
    match = re.search(image_extensions, values)
    if match == None:
        return False
    else:
        return True


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                external_urls.add(href)
            continue
        if not is_image(href):
            print(f"Internal Link: {href}")
            urls.add(href)
            internal_urls.add(href)
    return urls


def crawl(url, max_urls=30):
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

crawl("https://miteritreks.com/")
print(internal_urls)
print(external_urls)