from rest_framework import serializers
from forum.models import Category, Tag, Topic, Comment, Like
from rest_framework.exceptions import PermissionDenied
from django.db.models import Prefetch, Max
import datetime
from django.db.models import Q

class TopicListSerializer(serializers.ModelSerializer):
    is_modified = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    tag_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    last_comment_timestamp = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

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
                  "is_anonymous",
                  "comments_count",
                  "is_closed",
                  "is_removed",
                  "last_comment_timestamp",
                  "likes_count"
                  ]
        # Добавить каунт коммент и дату последнего коммента
    
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('category')
        queryset = queryset.select_related('user')
        queryset = queryset.select_related('tag')
        queryset = queryset.prefetch_related('comments')
        queryset = queryset.prefetch_related('likes')
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
    
    # def get_title_1(self, obj):
    #     if obj.is_removed == True:
    #         return "Данный топик был удален администрацией YktLife."
    #     else:
    #         return obj.title
    
    def get_last_comment_timestamp(self, obj):
        if obj.comments.exists():
            return obj.last_comment
        else:
            return obj.created_at
        
    def get_likes_count(self, obj):
        return obj.likes.all().count()
    
class TopicCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugField(read_only = False)
    tag = serializers.IntegerField(allow_null = True, read_only = False)


    class Meta:
        model = Topic
        fields = ["category", "title", "text", "is_anonymous", "tag"]

    def validate(self, data): 
        if not data['tag'] == None:
            if not Tag.objects.get(id = data['tag']).category == Category.objects.get(slug = data['category']):
                raise serializers.ValidationError("Тег не относится к данной категории")
        return data


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
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at',
            'is_anonymous',
            'author_nickname',
            'is_removed',
            'text_1',
            "likes_count",
            "did_like"
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

    def get_likes_count(self, obj):
        return obj.likes.all().count()

    def get_did_like(self, obj):
        return obj.likes.filter(user = self.context['request'].user).exists()

    
class CommentListHelperSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    text_1 = serializers.SerializerMethodField()
    children = CommentListChildHelperSerializer(many = True)
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at',
            'is_anonymous',
            'author_nickname',
            'is_removed',
            'text_1',
            "likes_count",
            "did_like",
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
    
    def get_likes_count(self, obj):
        return obj.likes.all().count()

    def get_did_like(self, obj):
        # return obj.likes.filter(user = self.context['request'].user).exists()
        criterion1 = Q(content_type=10)
        criterion2 = Q(object_id=obj.id)
        return self.context['user_likes'].filter(criterion1 & criterion2)

    
class TopicCommentsDetailSerializer(serializers.ModelSerializer):
    is_modified = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    tag_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    text_1 = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()

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
                  "text_1", 
                  "is_anonymous",
                  "comments_count",
                  "is_closed",
                  "is_removed",
                  "modified_at",
                  "likes_count",
                  "did_like",
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
    
    def get_text_1(self, obj):
        if obj.is_removed == True:
            return "Данный топик был удален администрацией YktLife."
        else:
            return obj.text
        
    def get_likes_count(self, obj):
        return obj.likes.all().count()

    def get_did_like(self, obj):
        return obj.likes.filter(user = self.context['request'].user).exists()
    
    def get_comments(self, obj):
        comments = obj.comments.all()
        comments = comments.select_related('user').prefetch_related('children').prefetch_related('children__user').prefetch_related('likes').prefetch_related('children__likes').filter(parent = None).order_by('created_at')
        self.context['user_likes'] = self.context['request'].user.liked_by.select_related('user')
        return CommentListHelperSerializer(comments, many = True, context = self.context).data
        
class TopicDetailSerializer(serializers.ModelSerializer):
    is_modified = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    tag_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    title_1 = serializers.SerializerMethodField()
    last_comment_timestamp = serializers.SerializerMethodField()
    text_1 = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()

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
                  "text_1",
                  "is_anonymous",
                  "comments_count",
                  "is_closed",
                  "is_removed",
                  "last_comment_timestamp",
                  "modified_at",
                  "likes_count",
                  "did_like"
                  ]
    
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
    
    
    def get_last_comment_timestamp(self, obj):
        if obj.comments.exists():
            return obj.comments.order_by('created_at').last().created_at
        else:
            return obj.created_at
    
    def get_text_1(self, obj):
        if obj.is_removed == True:
            return "Данный топик был удален администрацией YktLife."
        else:
            return obj.text
        
    def get_likes_count(self, obj):
        return obj.likes.all().count()

    def get_did_like(self, obj):
        return obj.likes.filter(user = self.context['request'].user).exists()

class TopicEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [                   
                  "title", 
                  "text"
                  ]
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.is_modified = True
        instance.modified_at = datetime.datetime.now()  
        instance.save()
        return instance
