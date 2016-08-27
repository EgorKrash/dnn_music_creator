from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
import os

def home(request):
    a = request.GET.get('a', '')
    context = dict()
    context['a'] = a
    return render(request, 'sender/index.html', context)


exec_dict = {}
def api_music(request):
	a = request.GET.get('a', '')
	if os.path.exists('static/music/' + a + '.mp3') == True:
		return JsonResponse({'a': a, 'status': "OK", 'url': 'static/' + a +'.mp3'})
	else:
		if not a in exec_dict:
			exec_dict[a] = 1
			os.system('python ../../gym/generate_text.py /root/Hathor/static/music/'+ a +'.mp3')
		return JsonResponse({'a': a, 'status':"FAIL jj"})
	

def about(request):
    return HttpResponse("Yo are at 'about' page")

def music(request):
    return render(request, 'sender/music.html')

def github(request):
    return HttpResponse("Yo are at 'github' page")
