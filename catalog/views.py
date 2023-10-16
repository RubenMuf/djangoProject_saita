from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, Group
# Create your views here.
def index(req): # эта самая первая функция загружается на страницу потому что стоит первая в пути нв urls
    numkino = Kino.objects.all().count() # берем количество фильмов из модели и присваиваем в переменную, для вывода на страницу
    numactor = Actor.objects.all().count() # берем количество актеров из модели и присваиваем в переменную, для вывода на страницу
    numfree = Kino.objects.filter(status__kino=1).count() # Находим количество определенного качества фильма из модели через фильтр и присваеваем его в переменную, для вывода на страницу
    if req.user.username:
        user_f_name = req.user.first_name
        user_l_name = req.user.last_name

    else:
        user_f_name = 'Гость'
        user_l_name = ''
    data = {'k1':numkino, 'k2':numactor, 'k3': numfree, 'user_f_name': user_f_name, 'user_l_name': user_l_name} # словарь для непосредственного вывода информации на страницу для пользователя
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
        permission = True
    else:
        print('not ok') # нельзя смотреть фильм
        permission = False
    k1 = Kino.objects.get(id=id1)
    k2 = Group.objects.get(id=status).name
    k3 = Status.objects.get(id=id2).name
    data = {'kino':k1, 'status':k2, 'statuskino':k3, 'prava': permission}
    return render(reg, 'prosmotr.html', data)

def buy(req, type):
    usid = req.user.id # находим текущего пользователя
    user = User.objects.get(id=usid) # находим его в табличке пользователя
    statusnow = user.groups.all()[0].id # берем самую первую запись в группе по связи берем его номер
    grold = Group.objects.get(id=statusnow) # находим эту подписку среди таблица gruop
    grold.user_set.remove(user) # удаляем старую подписку
    grnew = Group.objects.get(id=type) # находим ему новую подписку
    grnew.user_set.add(user) # выписываем новую подписку
    k1 = grnew.name
    data = {'podpiska': k1}
    return render(req, 'buy.html', data)

from .form import SignUpform, Podpiska
from django.contrib.auth import authenticate, login


def registr(req):
    print(1)
    if req.POST:
        print(2)
        anketa = SignUpform(req.POST)
        if anketa.is_valid():
            print(3)
            anketa.save()
            k1 = anketa.cleaned_data.get('username')
            k2 = anketa.cleaned_data.get('password1')
            k3 = anketa.cleaned_data.get('first_name')
            k4 = anketa.cleaned_data.get('last_name')
            k5 = anketa.cleaned_data.get('email')
            user = authenticate(username=k1, password=k2) #сохраняет нового пользоватлея
            man = User.objects.get(username=k1)             #найдем нового юзера
            #заполним поля в таблице
            man.first_name = k3
            man.last_name = k4
            man.email = k5
            man.save()
            login(req, user)
            group = Group.objects.get(id=1) # находим бесплатную подписку
            group.user_set.add(man) # записываем нового пользователя в подписку
            return redirect('home') # входит на сайт
    else:
        anketa = SignUpform()
    data={'regform': anketa}
    return render(req,'registration/registration.html',context=data)

def purchase(req):
    usid = req.user.id # находим текущего пользователя
    user = User.objects.get(id=usid) # находим его в табличке пользователя
    id = Podpiska()
    print(type(len(user.groups.all())), '/*')

    if len(user.groups.all()) == 1:
        statusnow = user.groups.all()[0].id # берем самую первую запись в группе по связи берем его номер
        k1 = Group.objects.get(id=statusnow)
        k2 = len(user.groups.all())
        data = {'podpiska': k1, 'quantity': k2}
    elif len(user.groups.all()) == 2:
        statusnow = user.groups.all()[0].id
        statusnow2 = user.groups.all()[1].id
        k1 = Group.objects.get(id=statusnow)
        k2 = len(user.groups.all())
        k3 = Group.objects.get(id=statusnow2)
        data = {'podpiska': k1, 'quantity': k2, 'podpiska2': k3}

    elif len(user.groups.all()) == 3:
        anketa = Podpiska()
        statusnow = user.groups.all()[0].id
        statusnow2 = user.groups.all()[1].id
        statusnow3 = user.groups.all()[2].id
        k1 = Group.objects.get(id=statusnow)
        k2 = len(user.groups.all())
        k3 = Group.objects.get(id=statusnow2)
        k4 = Group.objects.get(id=statusnow3)
        data = {'podpiska': k1, 'quantity': k2, 'podpiska2': k3, 'podpiska3': k4, 'form': anketa}
    else:
        k1 = 'У вас нет ни одной подписки.'
        print(k1)
        data = {'none': k1, 'form': id}

    return render(req, 'purshase.html', data)

def del_(req, t1):
    usid = req.user.id  # находим текущего пользователя
    user = User.objects.get(id=usid)  # находим его в табличке пользователя
    # statusnow = user.groups.all()[0].id  # берем самую первую запись в группе по связи берем его номер
    grold = Group.objects.get(id=t1)  # находим эту подписку среди таблица gruop
    grold.user_set.remove(user)  # удаляем старую подписку
    k1 = grold.name
    print(k1)
    # grnew = Group.objects.get(id=type)  # находим ему новую подписку
    # grnew.user_set.add(user)  # выписываем новую подписку
    # k1 = grnew.name
    data = {'podpiska': k1}
    return render(req, 'del_.html', data)

def app_(req, type_):
    usid = req.user.id  # находим текущего пользователя
    user = User.objects.get(id=usid)  # находим его в табличке пользователя
    # statusnow = user.groups.all()[0].id  # берем самую первую запись в группе по связи берем его номер
    # grold = Group.objects.get(id=statusnow)  # находим эту подписку среди таблица gruop
    # grold.user_set.remove(user)  # удаляем старую подписку
    grnew = Group.objects.get(id=type_)  # находим ему новую подписку
    grnew.user_set.add(user)  # выписываем новую подписку
    k1 = grnew.name
    data = {'podpiska': k1}
    return render(req, 'buy.html', data)

# def registr(req):
#     print(1)
#     if req.POST:
#         print(2)
#         anketa = SignUpform(req.POST)
#         if anketa.is_valid():
#             print(3)
#             anketa.save()
#             k1 = anketa.cleaned_data.get('username')
#             k2 = anketa.cleaned_data.get('password')
#             k3 = anketa.cleaned_data.get('first_name')
#             k4 = anketa.cleaned_data.get('last_name')
#             k5 = anketa.cleaned_data.get('email')
#             user = authenticate(username=k1, password=k2) # сохраняем нового пользователя
#             man = User.objects.get(username=k1) # найдем нового пользователя
#             man.first_name = k3
#             man.last_name = k4
#             man.email = k5
#             man.save()
#             group = Group.objects.get(id=1) # находим бесплатную подписку
#             group.user_set.add(man) # записываем нового пользователя в подписку
#             login(req, user)
#             return redirect('home')#входит на сайт
#
#     else:
#         anketa = SignUpform()
#     data = {'regform':anketa}
#     return render(req, 'registration/registration.html', context=data)


# def pod(reg, podp):
#     k1 = ''
#     data = {'podp': k1}
#     return render(reg, 'podp', data)