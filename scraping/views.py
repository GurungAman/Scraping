from django.shortcuts import render
import json
import os
from urllib.parse import urlparse
from django.http import JsonResponse
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from scraping.utils import download_urls, count_files, download_files
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
    print(data_json)
    parsed_url = urlparse(data_json['url'])
    response = {}
    if bool(parsed_url.netloc) and bool(parsed_url.scheme):
        response['status'] = True
        # folder_name = data_json['url'].split("/")[2]
        url = data_json['url']
        folder_name = urlparse(url).netloc
        print(folder_name)
        
        
        if data_json['get_links']:
            download_urls(data_json['url'], single_page=False)
        if data_json['single_page']:
            download_urls(data_json['url'], single_page=True)
            print(f"Current scraping Link: {url}")
            download_files(data_json=data_json)
        
        if data_json['whole_site']:
            file_path = os.path.join(os.getcwd(), "scraping/files", folder_name, "links/internal_links.txt")
            try:
                reader = open(file_path, "r")
                download_urls(data_json['url'], single_page=False)
                for links in reader:
                    link = links.strip("\n")
                    print(f"Current scraping Link: {link}")
                    download_files(data_json=data_json)
            except Exception as e:
                print(e.__class__)
            finally:
                reader.close()
        zip_files(folder_name)
        total_files = count_files(folder_name)
        print(total_files)
        response["data"] = total_files
        return JsonResponse(response)
    else:
        response['status'] = False
        return JsonResponse(response)



