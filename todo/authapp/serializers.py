from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.models import User


class AppUsersSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['uid',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'add_datetime',
                  'last_modified',
                  ]
