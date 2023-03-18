from rest_framework import serializers
from forum.models import Category, Tag


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
                #   "description", 
                  "position_column", 
                  "position_order"]

class CategoryDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    me_can_post = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["name",
                  "slug", 
                  "description", 
                  "position_column", 
                  "position_order",
                  "tags",
                  "users_can_post",
                  "me_can_post",
                  "me_can_pin"
                  ]
        
    def get_tags(self, obj):
        return TagHelperSerializer(Tag.objects.filter(category = obj).order_by('order'), many = True).data
    
    def get_me_can_post(self, obj):
        if obj.users_can_post:
            return True
        else:
            return self.context['request'].user.is_superuser
        
    def get_me_can_pin(self, obj):
        return self.context['request'].user.is_superuser