from rest_framework import serializers
from forum.models import Category, Tag, Topic, Comment
from rest_framework.exceptions import PermissionDenied
from django.db.models import Prefetch
from rest_framework_recursive.fields import RecursiveField


    

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
    title_1 = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["id", 
                  "category_slug", 
                  "category_name",
                  "tag_name",
                  "created_at", 
                  "is_modified", 
                  "author_nickname", 
                  "title_1", 
                  "is_anonymous",
                  "comments_count",
                  "is_closed",
                  "is_removed"
                  ]
        # Добавить каунт коммент и дату последнего коммента
    
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('category')
        queryset = queryset.select_related('user')
        queryset = queryset.select_related('tag')
        queryset = queryset.prefetch_related('comments')
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
        return obj.comments.count()
    
    def get_title_1(self, obj):
        if obj.is_removed == True:
            return "Данный топик был удален администрацией YktLife."
        else:
            return obj.title

class TopicCreateSerializer(serializers.ModelSerializer):
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
        # Здесь экспешн
        if not self.validated_data['tag'] == None:
            tag = Tag.objects.get(id = self.validated_data['tag'])
        else:
            tag = None
        topic = Topic.objects.create(user= self.context['request'].user, title=title, text=text, category=category, is_anonymous = is_anonymous, tag = tag)
        return topic


class CommentListChildHelperSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    text_1 = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at',
            'is_anonymous',
            'author_nickname',
            'is_removed',
            'text_1'
        ]
    
    def get_text_1(self, obj):
        if obj.is_removed == True:
            return "Данный комментарий был удален администрацией YktLife."
        else:
            return obj.text
        
    def get_author_nickname(self, obj):
        if obj.is_anonymous:
            return "Аноним"
        else:
            return obj.user.username


class CommentListHelperSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    text_1 = serializers.SerializerMethodField()
    children = CommentListChildHelperSerializer(many = True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at',
            'is_anonymous',
            'author_nickname',
            'is_removed',
            'text_1',
            'children'
        ]
    
    def get_text_1(self, obj):
        if obj.is_removed == True:
            return "Данный комментарий был удален администрацией YktLife."
        else:
            return obj.text
        
    def get_author_nickname(self, obj):
        if obj.is_anonymous:
            return "Аноним"
        else:
            return obj.user.username
    
    # def get_children(self, obj):
    #     replies = obj.children.all().select_related('user').order_by('created_at')
    #     return CommentListChildHelperSerializer(replies, many = True).data

class TopicDetailSerializer(serializers.ModelSerializer):
    is_modified = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    tag_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    title_1 = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["id", 
                  "category_slug", 
                  "category_name",
                  "tag_name",
                  "created_at", 
                  "is_modified", 
                  "author_nickname", 
                  "title_1",
                  "text", 
                  "is_anonymous",
                  "comments_count",
                  "is_closed",
                  "is_removed",
                  "comments"
                  ]
        # Добавить каунт коммент и дату последнего коммента
    
    def setup_eager_loading(queryset):
        # queryset = queryset.select_related('category')
        # queryset = queryset.select_related('user')
        # queryset = queryset.select_related('tag')
        queryset = queryset.prefetch_related('comments')
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
        return obj.comments.count()
    
    def get_title_1(self, obj):
        if obj.is_removed == True:
            return "Данный топик был удален администрацией YktLife."
        else:
            return obj.title

    def get_comments(self, obj):
        comments = obj.comments.all()
        comments = comments.select_related('user').prefetch_related('children').prefetch_related('children__user').filter(parent = None).order_by('created_at')
        return CommentListHelperSerializer(comments, many = True).data
        