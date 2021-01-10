import os
import re
from io import BytesIO
from urllib.parse import urlparse, urljoin
from PIL import Image
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import cairosvg


class Scraping:
	def __init__(self, url):
		options = Options()
		options.headless = True
		self.driver = webdriver.Firefox(options=options, executable_path='geckodriver', service_log_path=os.devnull)
		self.url = url
		self.custom_css = 0
		self.custom_js = 0

	def is_image(self, values):
		image_extensions = r".jpg|.jpeg|.JPEG|.png|.svg|.gif"
		match = re.search(image_extensions, values)
		if match == None:
			return False
		else:
			return True

	def is_file(self, file):
		if os.path.isfile(file):
			return True
		else:
			return False

	def get_js(self):
		driver = self.driver
		driver.get(self.url)
		script_tags = driver.find_elements_by_tag_name('script')
		js_files = []
		folder_name = self.url.split("/")[2]
		f_path = os.path.join(os.getcwd(), "scraping", "files", folder_name, "js_files/")
		if not os.path.isdir(os.getcwd()+"/scraping/files/"+folder_name+"/js_files/"):
			os.makedirs(os.getcwd()+"/scraping/files/"+folder_name+"/js_files/")
		for scripts in script_tags:
			if scripts.get_attribute('type') == "text/javascript" or scripts.get_attribute('type') == "":
					if scripts.get_attribute('src') != "":
						links = scripts.get_attribute('src')
						r = requests.get(links)
						file_name = links.split("/")[-1]
						content = str(r.content.decode("utf-8"))
						if not self.is_file(f_path+file_name):
							with open(f_path + file_name, "w") as f:
								print(f"Downloading {file_name}.js")
								f.write(content)
						else:
							continue
					else:
						with open(f_path+folder_name+f" {self.custom_js}.js", "w+") as f:
							self.custom_js += 1
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
		file_path = os.path.join(os.getcwd(), "scraping", "files", folder_name, "images/") 
		if not os.path.isdir(file_path):
			os.makedirs(os.getcwd()+"/scraping/files/"+folder_name+"/images/")        
		for image in images:
			try:  
				image_name = image.split("/")
				image_name = image_name[-2]+"-"+image_name[-1].split(".")[0]+".png"
				if ".svg" in image:
					if not self.is_file(file_path+image_name):
						print(f"Downloading image: {image_name}")
						cairosvg.svg2png(url=image, write_to=file_path+image_name)
					else:
						continue
				else:
					r = requests.get(image)
					content = BytesIO(r.content)
					image_name = image.split("/")[-1]+".png"
					if not self.is_file(file_path+image_name):
						print(f"Downloading image: {image_name}")
						img = Image.open(content)
						img.save(file_path+image_name)
					else:
						continue
			except Exception as e:
				print(f"{e}")
		return images

	def get_css(self):
		driver = self.driver
		driver.get(self.url)
		css_tags = driver.find_elements_by_tag_name('link')
		folder_name = self.url.split("/")[2]
		file_path = os.path.join(os.getcwd(), "scraping", "files", folder_name, "css/") 
		css_files = []
		if not os.path.isdir(file_path):
			os.makedirs(os.getcwd()+"/scraping/files/"+folder_name+"/css/")
		for css in css_tags:
			if css.get_attribute("rel") == "stylesheet" or css.get_attribute("type") == "text/css":
				links = css.get_attribute("href")
				css_file_name = links.split("/")[-1]
				if len(css_file_name) > 50:
					css_file_name = links.split("/")[-1][-40:]
				r = requests.get(links)
				content = str(r.content.decode("utf-8"))
				if not self.is_file(file_path+css_file_name+".css"):
					with open(file_path + css_file_name+".css", "w") as f:
						print(f"Downloading {css_file_name}")
						f.write(content)
				else:
					continue
		style_tags = driver.find_elements_by_tag_name("style")
		for css in style_tags:
			if css.get_attribute("type") == "text/css":
				if not self.is_file(file_path+f"{self.custom_css}_file.css"):
					with open(file_path+folder_name+f" {self.custom_css}_file.css", "w+") as f:
						print(f"Downloading {self.count_css}_file")
						self.custom_css+=1
						f.write(css.get_attribute("innerHTML"))  
		return css_files

	def tear_down(self):
		self.driver.quit()