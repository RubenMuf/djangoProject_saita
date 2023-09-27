from django.http import HttpResponse
from django.shortcuts import render
from .models import *
# Create your views here.
def index(req):
    numkino = Kino.objects.all().count()
    numactor = Actor.objects.all().count()
    numfree = Kino.objects.filter(status__kino=1).count()
    data = {'k1':numkino, 'k2':numactor, 'k3': numfree}
    return render(req, 'index.html', context=data)

# def allkino(req):
#     return render(req, 'index.html')

from django.views import  generic
class Kino_list(generic.ListView):
    model = Kino

class Kino_detail(generic.DetailView):
    model = Kino

# def info(req, id):
#     film = Kino.objects.get(id=id)
#     return HttpResponse(film.title)

