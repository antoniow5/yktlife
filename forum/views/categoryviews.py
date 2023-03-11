from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from forum.serializers import CategoryListSerializer, CategoryDetailSerializer
from ..models import Category
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from django.core.paginator import Paginator
# from .exceptiondicts import responce_dicts
from django.db.models import Max



@api_view(['GET','POST'])
def categories_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories,many=True)
        return Response(serializer.data)

    elif(request.method == 'POST'):
        if request.user.is_superuser:
            serializer = CategoryDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status= status.HTTP_201_CREATED)
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied({"message":"You don't have permission"})
            # return Response(responce_dicts(403), status = status.HTTP_403_FORBIDDEN)


@api_view(['GET','PUT', 'DELETE'])
def categories_detail(request, slug):
    try:
        category = Category.objects.get(slug = slug)
    except Category.DoesNotExist as e: 
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)

    elif(request.method == 'PUT'):
        if request.user.is_superuser:
            serializer = CategoryDetailSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied({"message":"You don't have permission"})
        
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied({"message":"You don't have permission"})