from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.serializers import AppUsersSerializer
from .models import Project, ToDo, UserOnProject, Executor


class ProjectSerializerBase(serializers.ModelSerializer):
    '''
        Используется для добавления нового проекта
    '''
    class Meta:
        model = Project
        fields = '__all__'
        # extra_kwargs = {'user_on_project': {'required': False}}

    # def get_field_names(self, declared_fields, info):
    #     s = super(ProjectSerializerBase, self).get_field_names(declared_fields, info)
    #     print(info)
    #     return s



class ProjectModelSerializer(serializers.ModelSerializer):
    user_on_project = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class UserOnProjectSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(many=False)

    # project = ProjectModelSerializer(many=False)
    # user = serializers.ManyRelatedField(many=True)

    class Meta:
        model = UserOnProject
        fields = '__all__'


class ExecutorToDoModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class TodoModelSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'


class TodoModelSerializer(serializers.ModelSerializer):
    # project_id = ProjectModelSerializer()
    # project_id = serializers.StringRelatedField(many=False)
    user_on_todo = serializers.StringRelatedField(many=True)

    class Meta:
        model = ToDo
        fields = '__all__'


