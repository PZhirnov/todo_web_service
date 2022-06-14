from django.contrib import admin
from mainapp.models import Project, ToDo, UserOnProject, Executor
# Register your models here.


admin.site.register(Project)
admin.site.register(ToDo)
admin.site.register(UserOnProject)
admin.site.register(Executor)
