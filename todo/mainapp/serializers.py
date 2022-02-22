from rest_framework.serializers import HyperlinkedModelSerializer
from mainapp.models import AppUsers

class AppUsersSerializers(HyperlinkedModelSerializer):
    class Meta:
        model = AppUsers
        field = '__all__'
