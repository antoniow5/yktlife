from rest_framework import serializers
from forum.models import Category, Tag, Topic, Comment, CommentLike
from django.db.models import Prefetch, Exists, OuterRef
import datetime

class TopicListCategoryAllSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    title = serializers.CharField()
    is_anonymous = serializers.BooleanField()
    is_closed = serializers.BooleanField()
    # is_removed = serializers.BooleanField()
    is_modified = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    author_nickname = serializers.SerializerMethodField()
    last_comment_or_created = serializers.DateTimeField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

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
        
    def get_likes_count(self, obj):
        return obj.topiclikes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
class TopicListCategorySpecifiedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    title = serializers.CharField()
    is_anonymous = serializers.BooleanField()
    is_closed = serializers.BooleanField()
    # is_removed = serializers.BooleanField()
    is_modified = serializers.SerializerMethodField()
    tag_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    last_comment_or_created = serializers.DateTimeField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_pinned = serializers.BooleanField()

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
        
    def get_likes_count(self, obj):
        return obj.topiclikes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()

    
class TopicCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugField(read_only = False, required = True)
    tag = serializers.IntegerField(allow_null = True, read_only = False, required = True)

    class Meta:
        model = Topic
        fields = ["category", "title", "text", "is_anonymous", "tag", "is_pinned"]

    def validate(self, data): 
        if not data['tag'] == None:
            if not Tag.objects.get(id = data['tag']).category == Category.objects.get(slug = data['category']):
                raise serializers.ValidationError("Тег не относится к данной категории")
        return data

    def create(self, validated_data):
        title = validated_data['title']
        text = validated_data['text']
        is_anonymous = validated_data['is_anonymous']
        category = Category.objects.get(slug = validated_data['category']) 
        is_pinned = validated_data['is_pinned']
        if not validated_data['tag'] == None:
            tag = Tag.objects.get(id = validated_data['tag'])
        else:
            tag = None
        topic = Topic.objects.create(user= self.context['request'].user, title=title, text=text, category=category, is_anonymous = is_anonymous, tag = tag, is_pinned = is_pinned)
        return topic


class CommentListChildHelperSerializer(serializers.ModelSerializer):
    is_removed = serializers.BooleanField()
    is_anonymous = serializers.BooleanField()
    author_nickname = serializers.SerializerMethodField()
    text_1 = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.BooleanField()
    
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
        return obj.commentlikes.all().count()

    
class CommentListHelperSerializer(serializers.ModelSerializer):
    is_removed = serializers.BooleanField()
    is_anonymous = serializers.BooleanField()
    author_nickname = serializers.SerializerMethodField()
    text_1 = serializers.SerializerMethodField()
    children = CommentListChildHelperSerializer(many = True)
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.BooleanField()

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
        return obj.commentlikes.all().count()


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
                  "modified_at",
                  "likes_count",
                  "did_like",
                  "comments"
                  ]    
   
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
        return obj.topiclikes.all().count()

    def get_did_like(self, obj):
        return obj.topiclikes.filter(user = self.context['request'].user).exists()
    
    def get_comments(self, obj):
        comments_annotated = obj.comments.all()
        comments_annotated = comments_annotated.select_related('user')
        comments_annotated = comments_annotated.prefetch_related('commentlikes')
        comments_annotated = comments_annotated.prefetch_related(Prefetch('children', Comment.objects.filter(topic = obj).annotate(did_like = Exists(CommentLike.objects.filter(user=self.context['request'].user, comment_id=OuterRef('pk'))))))
        comments_annotated = comments_annotated.prefetch_related('children__user')
        comments_annotated = comments_annotated.prefetch_related('children__commentlikes')
        comments_annotated = comments_annotated.annotate(did_like = Exists(CommentLike.objects.filter(user=self.context['request'].user, comment_id=OuterRef('pk'))))
        comments_annotated = comments_annotated.filter(parent = None).order_by('created_at')
        return CommentListHelperSerializer(comments_annotated, many = True).data
        

class TopicDetailSerializer(serializers.ModelSerializer):
    is_modified = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source = 'category.slug')
    category_name = serializers.CharField(source = 'category.name')
    tag_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
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
                #   "is_removed",
                  "last_comment_timestamp",
                  "modified_at",
                  "likes_count",
                  "did_like"
                  ]
        
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
        return obj.topiclikes.all().count()

    def get_did_like(self, obj):
        return obj.topiclikes.filter(user = self.context['request'].user).exists()


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
