from rest_framework import serializers
from forum.models import Category, Topic

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","slug", "description", "position_column", "position_order"]

class TopicSerializer(serializers.ModelSerializer):
    is_updated = serializers.BooleanField(read_only = True, source = 'get_is_updated')
    category = serializers.SlugRelatedField(slug_field='slug', many = False, queryset = Category.objects.all())
    class Meta:
        model = Topic
        fields = ["id","category","created_at", "updated_at", "is_updated", "user", "title", "text", "is_anonymous"]

class TopicCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugField(read_only = False)


    class Meta:
        model = Topic
        fields = ["category", "title", "text"]
        
    def create(self, validated_data):
        title = self.validated_data['title']
        text = self.validated_data['text']
        category = Category.objects.get(slug = self.validated_data['category'])
        topic = Topic.objects.create(user= self.context['request'].user, title=title, text=text, category=category, is_anonymous = False)
        return topic






