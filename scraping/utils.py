from .site_map import site_map
from .scrap import Scraping
import os

def download_files(data_json):
    try:
        scrape = Scraping(data_json['url'])
        if data_json['get_images']:
            scrape.get_images()
        if data_json['get_js']:
            scrape.get_js()
        if data_json['get_css']:
            scrape.get_css()
    except Exception as e:
        print(e.__class__)
    finally:
        scrape.tear_down()


def count_files(url):
    folder_names = ["css", "images", "js_files"]
    total_files = {}
    for folder in folder_names:
        file_path = os.getcwd()+f"/scraping/files/{url}/{folder}"
        for root, dirs, files in os.walk(file_path):
            total_files[folder] = len(files)
    return total_files


def download_urls(url):
    try:
        s = site_map()
        s.crawl(url)
        internal_links = s.count_links()
        return internal_links
    except Exception as e:
        print(e.__class__)
    finally:
        s.save_to_file(url)