from rest_framework import serializers
from forum.models import Category, Topic

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id",
                  "name",
                  "slug", 
                  "description", 
                  "position_column", 
                  "position_order"]

class TopicSerializer(serializers.ModelSerializer):
    is_updated = serializers.BooleanField(read_only = True, source = 'get_is_updated')
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    author_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["id", 
                  "category_slug", 
                  "category_name", 
                  "created_at", 
                  "updated_at", 
                  "is_updated", 
                  "author_nickname", 
                  "title", 
                  "text", 
                  "is_anonymous"]
    
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('category')
        queryset = queryset.select_related('user')
        return queryset
    
    def get_author_nickname(self, obj):
        if obj.is_anonymous:
            return "Аноним"
        else:
            return obj.user.username

class TopicCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugField(read_only = False)


    class Meta:
        model = Topic
        fields = ["category", "title", "text", "is_anonymous"]
        
    def create(self, validated_data):
        title = self.validated_data['title']
        text = self.validated_data['text']
        is_anonymous = self.validated_data['is_anonymous']
        category = Category.objects.get(slug = self.validated_data['category'])
        topic = Topic.objects.create(user= self.context['request'].user, title=title, text=text, category=category, is_anonymous = is_anonymous)
        return topic






