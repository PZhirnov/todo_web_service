from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.serializers import AppUsersSerializer
from .models import Project, ToDo, UserOnProject, Executor
from authapp.serializers import ShortUserSerializer


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
    # user_on_project = serializers.StringRelatedField(many=True)
    user_on_project = ShortUserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectModelSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name']


class UserOnProjectSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(many=False)
    # project = ProjectModelSerializer(many=False)
    user = ShortUserSerializer()

    class Meta:
        model = UserOnProject
        fields = '__all__'


class UserOnProjectSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = UserOnProject
        fields = ['id', 'user']


class UserOnProjectSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(many=False)
    # project = ProjectModelSerializer(many=False)
    user = ShortUserSerializer()

    class Meta:
        model = UserOnProject
        fields = '__all__'


class UserOnProjectSerializerShort(serializers.ModelSerializer):
    user = ShortUserSerializer()
    # project = ProjectSerializerBase()

    class Meta:
        model = UserOnProject
        fields = '__all__'


class ExecutorToDoModelSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class ExecutorToDoModelSerializer(serializers.ModelSerializer):
    user_on_project = UserOnProjectSerializerBase()

    class Meta:
        model = Executor
        fields = '__all__'


class TodoModelSerializerBase(serializers.ModelSerializer):
    # user_on_todo = UserOnProjectSerializerBase()

    class Meta:
        model = ToDo
        fields = '__all__'


class TodoModelSerializer(serializers.ModelSerializer):
    project_id = ProjectModelSerializerShort()
    # project_id = serializers.StringRelatedField(many=False)
    # user_on_todo = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    user_on_todo = UserOnProjectSerializerShort(many=True)

    class Meta:
        model = ToDo
        fields = '__all__'


