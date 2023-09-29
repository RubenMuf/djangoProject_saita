from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.views import generic

def index(req):
    num_onwers = Owner.objects.all().count()  # создаем переменную для подсчета объектов из таблицы метод count без параметра, так как это джанговский метод.
    # num_animals = Animal.objects.all().count()
    # num_veterinarians = Veterinarian.objects.filter(status__kino=1).count() # через фильтр поис и подсчет
    # data = {'k1':num_onwers, 'k2':num_animals, 'k3': num_veterinarians}
    data = {'k1': num_onwers}
    return render(req, 'index.html', context=data)

# def allkino(req):
#     return render(req, 'index.html')

class Animal_list(generic.ListView): # автомат генерации через джанго списка объектов для показа
    model = Animal  # создаем список из модели кино
    # print(model)

class Owner_list(generic.ListView):
    model = Owner

# def info(req, id):  # старый способ вывода на экран, есть взамен модульна библиотеке generic на классе
#     animal = Animal.objects.get(id=id)
#     return HttpResponse(animal.nickname)

class Animal_detail(generic.DetailView):
    model = Animal



# Create your views here.
# def index(req):
#     return render(req, 'index.html')