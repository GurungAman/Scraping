import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
import re

class site_map:
	def __init__(self):
		# self.url = url
		self.internal_urls = set()
		self.external_urls = set()
		self.total_urls_visited = 0
	
	def count_links(self):
		return len(self.internal_urls), len(self.external_urls)

	def is_image(self, values):
		image_extensions = r".jpg|.jpeg|.JPEG|.png|.svg|.JPG|.gif"
		match = re.search(image_extensions, values)
		if match == None:
			return False
		else:
			return True

	def is_valid(self, url):
		parsed = urlparse(url)
		return bool(parsed.netloc) and bool(parsed.scheme)

	def link_type(self, url, values):
		if url in values and '#' not in values:
			return "internal_link"
		elif url not in values:
			return "external_link"

	def get_all_website_links(self, url):
		self.urls = set()
		domain_name = urlparse(url).netloc
		soup = BeautifulSoup(requests.get(url).content, "html.parser")
		for a_tag in soup.findAll("a"):
			href = a_tag.attrs.get("href")
			if href == "" or href is None:
				continue
			href = urljoin(url, href)
			parsed_href = urlparse(href)
			href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
			if not self.is_valid(href):
				continue
			if href in self.internal_urls:
				continue
			if domain_name not in href:
				if href not in self.external_urls:
					self.external_urls.add(href)
				continue
			if not self.is_image(href):
				print(f"Internal Link: {href}")
				self.urls.add(href)
				self.internal_urls.add(href)
		return self.urls

	def crawl(self, url, max_urls=20):
		self.total_urls_visited += 1
		links = self.get_all_website_links(url)
		for link in links:
			if int(self.total_urls_visited) > max_urls:
				break
			self.crawl(link)

	def save_to_file(self, url):
		folder_name = url.split("/")[2]
		file_path = os.path.join(os.getcwd(), "scraping", "files", folder_name, "links/") 
		if not os.path.isdir(file_path):
			os.makedirs(os.getcwd()+"/scraping/files/"+folder_name+"/links/")
		try:
			external_link_file = open(file_path+"extenal_links.txt", "w+")
			internal_link_file = open(file_path+"internal_links.txt", "w+")
			for link in self.internal_urls:
				internal_link_file.write(link+"\n")
			for link in self.external_urls:
				external_link_file.write(link+"\n")
		finally:
			internal_link_file.close()
			external_link_file.close()

