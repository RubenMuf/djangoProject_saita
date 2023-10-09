from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
# Create your views here.
def index(req): # эта самая первая функция загружается на страницу потому что стоит первая в пути нв urls
    numkino = Kino.objects.all().count() # берем количество фильмов из модели и присваиваем в переменную, для вывода на страницу
    numactor = Actor.objects.all().count() # берем количество актеров из модели и присваиваем в переменную, для вывода на страницу
    numfree = Kino.objects.filter(status__kino=1).count() # Находим количество определенного качества фильма из модели через фильтр и присваеваем его в переменную, для вывода на страницу
    if req.user.username:
        username = req.user.first_name
    else:
        username = 'Гость'
    data = {'k1':numkino, 'k2':numactor, 'k3': numfree, 'username': username} # словарь для непосредственного вывода информации на страницу для пользователя
    # user = User.objects.create_user('User2', 'user2@mail.ru', 'useruser')
    # user.first_name = 'Владислав'
    # user.last_name = 'Петросянский'
    # user.save()
    return render(req, 'index.html', context=data) # возврат запроса на на какую страницу и какую информацию вывести

# def allkino(req):
#     return render(req, 'index.html')

from django.views import  generic
class Kino_list(generic.ListView): # модель на классе на модели метод весь список
    model = Kino
    paginate_by = 3 # джанговская функция по сколько фильмов выводить на страницу, работает в связке с остальным кодом на файле HTML

class Kino_detail(generic.DetailView): # модель на классе на модели метод один объект из списка
    model = Kino

class Actor_list(generic.ListView):
    model = Actor
    paginate_by = 3  # джанговская функция по сколько фильмов выводить на страницу, работает в связке с остальным кодом на файле HTML

class Actor_detail(generic.DetailView): # модель на классе на модели метод один объект из списка
    model = Actor

class Director_list(generic.ListView):
    model = Director
    paginate_by = 3  # джанговская функция по сколько фильмов выводить на страницу, работает в связке с остальным кодом на файле HTML

class Director_detail(generic.DetailView): # модель на классе на модели метод один объект из списка
    model = Director

# def info(req, id):
#     film = Kino.objects.get(id=id)
#     return HttpResponse(film.title)

def status(req):
    k1 = Status.objects.all()
    data = {'podpiska': k1}
    return render(req, 'podpiska.html',context=data)

def prosmotr(reg, id1, id2, id3):
    print(id1, id2, id3)
    mas = ['Бесплатная', 'Базовая', 'Супер'] # kino id2
    mas2 = ['free', 'based', 'super'] # user id3
    status = 0
    if id3 != 0:
        status = User.objects.get(id=id3) # нашли пользователя
        print(status)
        status = status.groups.all() # нашли его подписки
        print(status)
        status = status[0].id #  нашли его id
        print(status)
    else:
        if id3 == 0: #  выдаёт гостю подписку №1 бесплатную
            status = 1
    if status >= id2: #  сравнение статуса на разрешение просмотра фильма
        print('ok')
    else:
        print('not ok') # нельзя смотреть фильм

    return render(reg, 'index.html')
