from ..models import Category, Topic, Comment, TopicLike, CommentLike
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from model_bakery import baker


@api_view(['GET'])
def test1(request):
    category = Category.objects.get(slug = 'auto')
    user = request.user
    # topics = baker.make('forum.Topic', category = category, _quantity=100000)
    # assert len(topics) == 100000
    # return Response(status = status.HTTP_201_CREATED)
    x = 0
    while x < 10000:
        topics = baker.make("forum.Topic", user = user, category = category, _bulk_create = True)
        comments1 = baker.make("forum.Comment", user = user, topic = topics, parent = None, _quantity=20, _bulk_create = True)
        x +=1
    return Response(status = status.HTTP_201_CREATED)