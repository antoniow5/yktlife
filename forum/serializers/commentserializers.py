from rest_framework import serializers
from forum.models import Category, Tag, Topic, Comment, CommentLike
from django.db.models import Prefetch, Exists, OuterRef
import datetime
    
class CommentCreateSerializer(serializers.ModelSerializer):
    is_anonymous = serializers.BooleanField()
    parent = serializers.IntegerField(allow_null = True, read_only = False)
    topic = serializers.IntegerField(allow_null = False)
    class Meta:
        model = Topic
        fields = ["is_anonymous", "parent", "topic", "is_anonymous", "tag"]

    def validate(self, data): 
        if not data['tag'] == None:
            if not Tag.objects.get(id = data['tag']).category == Category.objects.get(slug = data['category']):
                raise serializers.ValidationError("Тег не относится к данной категории")
        return data

    def create(self, validated_data):
        title = validated_data.get('title')
        text = validated_data.get('text')
        is_anonymous = validated_data.get('is_anonymous')
        category = Category.objects.get(slug = validated_data.get('category'))
        if not validated_data.get('tag') == None:
            tag = Tag.objects.get(id = validated_data.get('tag'))
        else:
            tag = None
        topic = Topic.objects.create(user= self.context['request'].user, title=title, text=text, category=category, is_anonymous = is_anonymous, tag = tag)
        return topic
