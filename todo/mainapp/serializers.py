from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.serializers import AppUsersSerializer
from .models import Project, ToDo # UserOnProject, Executor


class ProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields ='__all__'


class UserOnProjectSerializer(serializers.ModelSerializer):
    # project = serializers.StringRelatedField(many=False)
    # user = AppUsersSerializer()

    class Meta:
        model = Project.user_on_project
        fields = '__all__'


class ExecutorToDoModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ToDo.user_on_todo
        fields = '__all__'


class TodoModelSerializer(serializers.ModelSerializer):
   #  project = ProjectModelSerializer()

    class Meta:
        model = ToDo
        fields = '__all__'


