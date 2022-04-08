from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.models import User


class AppUsersSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'add_datetime',
                  'last_modified',
                  ]


class AppUsersExtendedSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'add_datetime',
                  'last_modified',
                  'is_staff',
                  'is_superuser',
                  ]
