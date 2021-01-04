from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup as bs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def log_in(request):
    # if request.method == "POST":
    #     username = request.POST['username']
    #     password = request.POST['password']
    return render(request,
                template_name='log_in.html')


def scrape(request):
    return render(request,
                template_name='enter_url.html')


class details_view(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {"message": "Checking if this works"}
        return Response(content)