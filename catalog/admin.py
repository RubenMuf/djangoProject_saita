from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Genre)
# admin.site.register(Director)
# admin.site.register(Actor)
admin.site.register(AgeRate)
# admin.site.register(Status)
# admin.site.register(Kino)
admin.site.register(Country)

class Actoradmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'born', 'country') # название столбиков в панеле админа
    list_display_links = ('fname', 'lname') # названия работают как ссылки
admin.site.register(Actor, Actoradmin) # регистрируем модель актер

class Directoradmin(admin.ModelAdmin):
    list_display = ('fname', 'lname') # название столбиков в панеле админа
    list_display_links = ('fname', 'lname') # названия работают как ссылки
admin.site.register(Director, Directoradmin) # регистрируем модель режиссер

class Kinoadmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'display_actors')
    list_filter = ('title', 'year', 'director')
    fieldsets = (('О фильме', {'fields': ('title', 'summary', 'actor')}),
                 ('Рейтинг', {'fields': ('rating', 'ager', 'status')}),
                 ('Остальное', {'fields': ('genre', 'country', 'director', 'year')}))
admin.site.register(Kino, Kinoadmin)

class Stinline(admin.TabularInline):
    model = Kino

class Statusadmin(admin.ModelAdmin):
    inlines = [Stinline]
admin.site.register(Status, Statusadmin)