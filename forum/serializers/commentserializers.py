from rest_framework import serializers
from forum.models import Category, Tag, Topic, Comment, CommentLike
from django.db.models import Prefetch, Exists, OuterRef
import datetime
    
class CommentCreateSerializer(serializers.ModelSerializer):
    topic = serializers.IntegerField(allow_null = False, required = True)
    parent = serializers.IntegerField(allow_null = False, required = True)

    class Meta:
        model = Comment
        fields = ["is_anonymous", "parent", "topic", "text"]

    def validate(self, data): 
        if not Topic.objects.get(id = data['topic']) == Comment.objects.get(slug = data['parent']).topic:
            raise serializers.ValidationError("Parental comment is in another category")
        if not Comment.objects.get(slug = data['parent']).parent == None:
            raise serializers.ValidationError("Parental comment is already nested")
        return data

    def create(self, validated_data):
        text = validated_data.get('text')
        is_anonymous = validated_data.get('is_anonymous')
        topic = Topic.objects.get(id = validated_data.get('topic'))
        if not validated_data.get('parent') == None:
            parent = Comment.objects.get(id = validated_data.get('parent'))
        else:
            parent = None
        comment = Comment.objects.create(user= self.context['request'].user, text=text, is_anonymous = is_anonymous, parent = parent, topic = topic)
        return comment

class CommentSpecifiedTopicSerializer(serializers.ModelSerializer):
    pass

class CommentSpecifiedCategorySerializer(serializers.ModelSerializer):
    pass