from rest_framework import serializers
from forum.models import Category, Tag
from rest_framework.exceptions import PermissionDenied
from django.db.models import Prefetch, Max


class TagHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag 
        fields = ["name",
                  "id"]     
        

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name",
                  "slug", 
                  "description", 
                  "position_column", 
                  "position_order"]

class CategoryDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["name",
                  "slug", 
                  "description", 
                  "position_column", 
                  "position_order",
                  "tags",
                  "can_post",
                  "can_comment",
                  "can_like"]
        
    def get_tags(self, obj):
        return TagHelperSerializer(Tag.objects.filter(category = obj), many = True).data