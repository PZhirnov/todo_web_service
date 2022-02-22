from django.contrib import admin
from mainapp.models import AppUsers
# Register your models here.

# Красивый вывод данных в таблице
class AppUsersAdmin(admin.ModelAdmin):
    list_display = ('uid', 'username', 'email', 'first_name', 'last_name', 'birthday', 'is_active', 'add_datetime')


admin.site.register(AppUsers, AppUsersAdmin)
