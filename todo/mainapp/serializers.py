from rest_framework.serializers import HyperlinkedModelSerializer
from mainapp.models import AppUsers


class AppUsersSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AppUsers
        # fields = '__all__'
        fields = ['username', 'first_name', 'last_name', 'email']
