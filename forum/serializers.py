from rest_framework import serializers
from forum.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","slug", "description", "position_column", "position_order"]
