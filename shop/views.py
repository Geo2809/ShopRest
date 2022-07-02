from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet

@api_view()
def product_list(request):
    pass

@api_view()
def product_detail(request, id):
    pass