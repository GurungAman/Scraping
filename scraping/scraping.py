import os
import re
from io import BytesIO
from selenium import webdriver
import requests
from PIL import Image

url1 = 'https://miteritreks.com/'
url2 = "https://himalayanmerch.com/"
url3 = "http://www.macpokhara.edu.np/"


def is_image(values):
    image_extensions = r".jpg|.jpeg|.JPEG|.png|.svg"
    match = re.search(image_extensions, values)
    if match == None:
        return False
    else:
        return True


def link_type(url, values):
    if url in values and '#' not in values:
        return "internal_link"
    elif url not in values:
        return "external_link"


def get_links(url):
    try:
        driver = webdriver.Firefox(executable_path='geckodriver', service_log_path=os.devnull)
        driver.get(url)
        link_tag = driver.find_elements_by_tag_name('a')
        links = [link.get_attribute('href') for link in link_tag]
        external_links = set()
        internal_links = set()
        for link in links:
            if link_type(url, link) == "internal_link" and is_image(link) == False:
                internal_links.add(link)
                print(link)
            elif link_type(url, link) == "external_link":
                external_links.add(link)
        # for values in internal_links:
        #     driver.get(values)
        #     link_tag = driver.find_elements_by_tag_name('a')
        #     links = [link.get_attribute('href') for link in link_tag]
        #     for values in links:
        #         if link_type(url, link) == "internal_link" and is_image(link) == False:
        #             internal_links.append(link)
        #         elif link_type(url, link) == "external_link":
        #             external_links.append(link)
        return internal_links, external_links
    finally:
        driver.quit()


def get_js(url):
    try:
        driver = webdriver.Firefox(service_log_path=os.devnull)
        driver.get(url)
        script_tags = driver.find_elements_by_tag_name('script')
        js_files = []
        folder_name = url.split("/")[2]
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
    finally:
        driver.quit()  

def get_images(url):
    try:
        driver = webdriver.Firefox(service_log_path=os.devnull)
        driver.get(url)
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
                if is_image(item) == True:
                    images.append(item)   
        folder_name = url.split("/")[2]
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
    finally:
        driver.quit()

def get_css(url):
    try:
        driver = webdriver.Firefox(service_log_path=os.devnull)
        driver.get(url)
        css_tags = driver.find_elements_by_tag_name('link')
        folder_name = url.split("/")[2]
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
    finally:
        driver.quit()


total_urls_visited = 0
def crawl(url, max_urls=30):
    global total_urls_visited
    total_urls_visited += 1
    links, _ = get_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

url = "https://miteritreks.com/"
crawl(url)