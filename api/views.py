from django.shortcuts import render

# Create your views here.

from .serializers import City_CodesSerializer
from rest_framework import viewsets
from .models import City_Codes

class City_CodesViewSet(viewsets.ModelViewSet):
    queryset = City_Codes.objects.all()
    serializer_class = City_CodesSerializer

