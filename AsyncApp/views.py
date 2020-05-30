from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import FileResponse
import time

def index(request):
	csrf_token = get_token(request)
	print("Hello I am Also Working")
	return render(request,'index.html',{'csrf_token':str(csrf_token)})