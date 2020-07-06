from rest_framework import serializers
from django.contrib.auth.models import User
from .models import City_Codes

class City_CodesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City_Codes
        fields = ('id', 'sid', 'pid', 'full_name', 'level')
