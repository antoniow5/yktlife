from rest_framework import serializers
from forum.models import Category, Tag, Topic
from rest_framework.exceptions import PermissionDenied


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
        if Tag.objects.filter(category = obj).exists():
            return TagHelperSerializer(Tag.objects.filter(category = obj), many = True).data
        else:
            return None
    
class TagListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ["name"]

class TopicListSerializer(serializers.ModelSerializer):
    is_modified = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    tag_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["id", 
                  "category_slug", 
                  "category_name",
                  "tag_name",
                  "created_at", 
                  "is_modified", 
                  "author_nickname", 
                  "title", 
                  "text", 
                  "is_anonymous",
                  "comments_count",
                  "is_closed"
                  ]
        # Добавить каунт коммент и дату последнего коммента
    
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('category')
        queryset = queryset.select_related('user')
        queryset = queryset.select_related('tag')
        queryset = queryset.prefetch_related('comment_set')
        return queryset
    
    def get_author_nickname(self, obj):
        if obj.is_anonymous:
            return "Аноним"
        else:
            return obj.user.username
        
    def get_is_modified(self, obj):
        if obj.modified_at == None:
            return False
        else:
            return True
    
    def get_tag_name(self, obj):
        if obj.tag == None:
            return None
        else:
            return obj.tag.name
    
    def get_comments_count(self, obj):
        return obj.comment_set.count()

class TopicAdminCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugField(read_only = False)
    tag = serializers.IntegerField(allow_null = True, read_only = False)


    class Meta:
        model = Topic
        fields = ["category", "title", "text", "is_anonymous", "tag"]
        
    def create(self, validated_data):
        title = self.validated_data['title']
        text = self.validated_data['text']
        is_anonymous = self.validated_data['is_anonymous']
        category = Category.objects.get(slug = self.validated_data['category'])
        if not self.validated_data['tag'] == None:
            tag = Tag.objects.get(id = self.validated_data['tag'])
        else:
            tag = None
        topic = Topic.objects.create(user= self.context['request'].user, title=title, text=text, category=category, is_anonymous = is_anonymous, tag = tag)
        return topic
    


class TopicUserCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugField(read_only = False)
    tag = serializers.IntegerField(allow_null = True)

    class Meta:
        model = Topic
        fields = ["category", "title", "text", "is_anonymous", "tag"]
        
    def create(self, validated_data):
        title = self.validated_data['title']
        text = self.validated_data['text']
        is_anonymous = self.validated_data['is_anonymous']
        category = Category.objects.get(slug = self.validated_data['category'])
        if not self.validated_data['tag'] == None:
            tag = Tag.objects.get(id = self.validated_data['tag'])
        else:
            tag = None
        if not category.can_post:
            raise PermissionDenied
        else:
            topic = Topic.objects.create(user= self.context['request'].user, title=title, text=text, category=category, is_anonymous = is_anonymous, tag = tag)
        return topic


class TopicDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ["name",
                  "slug", 
                  "description", 
                  "position_column", 
                  "position_order",
                  "tags",
                  "can_post",
                  "can_comment",
                  "can_like"]

    def setup_eager_loading(queryset):
        queryset = queryset.select_related('category')
        queryset = queryset.select_related('user')
        queryset = queryset.select_related('tag')
        queryset = queryset.prefetch_related('comment_set')
        return queryset

