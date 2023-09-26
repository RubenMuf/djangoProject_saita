from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Nickname(models.Model):
    name = models.CharField(max_length=20, verbose_name='Кличка')

    def __str__(self):
        return self.name

class Type_of_animal(models.Model):
    VIBOR = (('Собака', 'Собака'), ('Кошка', 'Кошка'), ('Бобер', 'Бобер'))
    name = models.CharField(max_length=20, choices=VIBOR, verbose_name='Вид питомца')

    def __str__(self):
        # return f'{self.lname} {self.fname}'
        return self.name

class Owner(models.Model):
    fname = models.CharField(max_length=20, verbose_name='Имя')
    lname = models.CharField(max_length=20, verbose_name='Фамилия')
    tel = models.CharField(max_length=13, verbose_name='Телефон')

class Age(models.Model):
    year = models.IntegerField(verbose_name='Возраст')

    def __str__(self):
        return self.year

class Weight(models.Model):
    kilo = models.FloatField(verbose_name='Вес')

    def __str__(self):
        return self.kilo

class Veterinarian(models.Model):
    specialist = models.CharField(max_length=20, verbose_name='Специалист')
    fname = models.CharField(max_length=20, verbose_name='Имя')
    lname = models.CharField(max_length=20, verbose_name='Фамилия')
    experience = models.IntegerField(verbose_name='Стаж врачевания')

    def __str__(self):
        return self.specialist

class Animal(models.Model):
    nickname = models.CharField(max_length=20, verbose_name='Кличка')
    type_of_animal = models.ForeignKey(Type_of_animal, on_delete=models.SET_DEFAULT, default=1, verbose_name='Тип животного')
    onwer = models.ForeignKey(Owner, verbose_name='Хозяин')
    age = models.IntegerField(verbose_name='Возраст')
    weight = models.FloatField(verbose_name='Вес')
    veterinarian = models.ManyToManyField(Veterinarian, verbose_name='Ветеринар - специалист')
    summary = models.TextField(max_length=500, verbose_name='Описание')

    # def __str__(self):
    #     return self.nickname
    #
    # def display_actors(self):
    #     res = ''
    #     for a in self.actor.all():
    #         res += a.lname + ' '
    #     return res
    # display_actors.short_description='Актеры'
