import os
import re
from io import BytesIO
from urllib.parse import urlparse, urljoin
from PIL import Image
from selenium import webdriver
import requests
from bs4 import BeautifulSoup


internal_urls = set()
external_urls = set()
total_urls_visited = 0

class Scraping:
	def __init__(self, url):
		self.driver = webdriver.Firefox(executable_path='geckodriver', service_log_path=os.devnull)
		self.url = url

	def is_image(self, values):
		image_extensions = r".jpg|.jpeg|.JPEG|.png|.svg"
		match = re.search(image_extensions, values)
		if match == None:
			return False
		else:
			return True
	
	def is_valid(self, link):
		parsed = urlparse(link)
		return bool(parsed.netloc) and bool(parsed.scheme)

	def get_js(self):
		driver = self.driver
		driver.get(self.url)
		script_tags = driver.find_elements_by_tag_name('script')
		js_files = []
		folder_name = self.url.split("/")[2]
		f_path = os.path.join(os.getcwd(), "files", folder_name, "js_files/")
		if not os.path.isdir(os.getcwd()+"/files/"+folder_name+"/js_files/"):
			os.makedirs(os.getcwd()+"/files/"+folder_name+"/js_files/")
		for scripts in script_tags:
			if scripts.get_attribute('type') == "text/javascript" or scripts.get_attribute('type') == "":
					if scripts.get_attribute('src') != "":
						links = scripts.get_attribute('src')
						r = requests.get(links)
						file_name = links.split("/")[-1]
						content = str(r.content)
						with open(f_path + file_name, "w") as f:
							f.write(content)
					else:
						with open(f_path+folder_name+".js", "a+") as f:
							f.write(scripts.get_attribute('innerHTML'))
		return js_files

	def get_images(self):
		driver = self.driver
		driver.get(self.url)
		image_tags = driver.find_elements_by_tag_name("img")
		images = [images.get_attribute("src") for images in image_tags]
		div_tag_images = driver.find_elements_by_tag_name("div")
		css_images = [images.get_attribute("style") for images in div_tag_images]
		regex = r"\(\".*?\"\)|\(\'.*?\'\)"
		for image in css_images:
			search_results = re.finditer(regex, image)
			for items in search_results:
				item = items.group(0) 
				item = item[2:len(item)-2]
				if self.is_image(item) == True:
					images.append(item)   
		folder_name = self.url.split("/")[2]
		file_path = os.path.join(os.getcwd(), "files", folder_name, "images/") 
		if not os.path.isdir(file_path):
			os.makedirs(os.getcwd()+"/files/"+folder_name+"/images/")        
		for image in images:
			r = requests.get(image)
			content = BytesIO(r.content)
			image_name = image.split("/")[-1]
			img = Image.open(content)
			img.save(file_path+image_name)
		return images

	def get_css(self):
		driver = self.driver
		driver.get(self.url)
		css_tags = driver.find_elements_by_tag_name('link')
		folder_name = self.url.split("/")[2]
		file_path = os.path.join(os.getcwd(), "files", folder_name, "css/") 
		css_files = []
		if not os.path.isdir(file_path):
			os.makedirs(os.getcwd()+"/files/"+folder_name+"/css/")
		for css in range(len(css_tags)):
			if css_tags[css].get_attribute("rel") == "stylesheet" or css_tags[css].get_attribute("type") == "text/css":
				links = css_tags[css].get_attribute("href")
				r = requests.get(links)
				content = str(r.content)
				with open(file_path + str(css)+"_file.css", "w") as f:
					f.write(content)
		style_tags = driver.find_elements_by_tag_name("style")
		for css in style_tags:
			if css.get_attribute("type") == "text/css":
				with open(file_path+folder_name+".css", "a+") as f:
					f.write(css.get_attribute("innerHTML"))  
		return css_files

	def get_links(self):
		urls = set()
		domain_name = urlparse(self.url).netloc
		soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
		for a_tag in soup.findAll("a"):
			href = a_tag.attrs.get("href")
			if href == "" or href is None:
				continue
			href = urljoin(self.url, href)
			parsed_href = urlparse(href)
			href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
			if not self.is_valid(href):
				continue
			if href in internal_urls:
				continue
			if domain_name not in href:
				if href not in external_urls:
					external_urls.add(href)
				continue
			if not self.is_image(href):
				urls.add(href)
				internal_urls.add(href)
				print(f"Internal Link: {href}")
		return urls


	def crawl(self, max_urls=30):
		global total_urls_visited
		total_urls_visited += 1
		links = self.get_links()
		for link in links:
			if total_urls_visited > max_urls:
				break
			crawl(link, max_urls=max_urls)

	def tear_down(self):
		self.driver.quit()

	
if __name__ == "__main__":
	url="https://miteritreks.com/"
	scrap = Scraping(url)
	try:
		# folder_name = url.split("/")[2]
		# file_path = os.path.join(os.getcwd(), "files", folder_name, "links/internal_links.txt") 
		# f = open(file_path, "r")
		# links = f.read().splitlines()
		# for link in links:
		# 	scrap.get_js()
		# f.close()
	finally:
		scrap.tear_down()
