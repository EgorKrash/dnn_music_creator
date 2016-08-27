from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
import os

def home(request):
    a = request.GET.get('a', '')
    context = dict()
    context['a'] = a
    return render(request, 'sender/index.html', context)

def api_music(request):
	a = request.GET.get('a', '')
	if os.path.exists('static/music/' + a + '.mp3') == True:
		return JsonResponse({'a': a, 'status': "OK", 'url': 'static/' + a +'.mp3'})
	else:
		return JsonResponse({'a': a, 'status':"FAIL jj"})
	

def about(request):
    return HttpResponse("Yo are at 'about' page")

def music(request):
    return render(request, 'sender/music.html')

def github(request):
    return HttpResponse("Yo are at 'github' page")