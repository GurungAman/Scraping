from django.shortcuts import render, redirect
import requests
import json
import os
from urllib.parse import urlparse, urljoin
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from .site_map import site_map
from .scrap import Scraping
# Create your views here.

def log_in_template(request):
    return render(request,
                template_name="log_in.html")

def scrape_template(request):
    return render(request,
                template_name='enter_url.html')

def complete_template(request):
    return render(request,
                template_name='complete.html')

def log_out(request):   
    pass

def verify(request):
    check_status = is_logged_in(request)
    if check_status['status']:
        response_json ={
            'status' : True,
            'user_id' : check_status['user'].id
        }
        return JsonResponse(response_json)
    else:
        return JsonResponse({
            'status' : False,
            'error' : check_status['exp']
        })

def is_logged_in(request):
    token =  str(request.headers['Authentication']).split(' ')[1]
    try:
        data = VerifyJSONWebTokenSerializer().validate({'token': token})
        return {
            'status' : True,
            'user' : data['user'],
        }
    except Exception as exp:
        print(exp.__dict__)
        return {
            'status' : False,
            'exp' : exp.__dict__
        }

def check_url(request):
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    parsed_url = urlparse(data_json['url'])
    response = {}
    if bool(parsed_url.netloc) and bool(parsed_url.scheme):
        response['status'] = True
        folder_name = data_json['url'].split("/")[2]
        file_path = os.path.join(os.getcwd(), "scraping/files", folder_name, "links/internal_links.txt")
        internal, external = download_urls(data_json['url'])
        reader = open(file_path, "r")
        for links in reader:
            link = links.strip("\n")
            print(f"Current scraping Link: {link}")
            try:
                scrape = Scraping(link)
                scrape.get_images()
                scrape.get_js()
                scrape.get_css()
            except:
                pass
            finally:
                scrape.tear_down()
        # total_files = count_files(folder_name)
        # response["data"] = total_files
        return JsonResponse(response)
    else:
        response['status'] = False
        return JsonResponse(response)



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
        internal_links, external_links = s.count_links()
        return internal_links, external_links
    except:
        pass
    finally:
        s.save_to_file(url)


