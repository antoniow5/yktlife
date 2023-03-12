from ..models import Topic, Comment, TopicLike, CommentLike
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def like_topic(request, id):
    try:
        topic = Topic.objects.get(id = id)
    except Topic.DoesNotExist:
        raise Http404
    if request.user.is_authenticated:
        user = request.user
    else:
        return Response(status= status.HTTP_401_UNAUTHORIZED)


    if request.method == 'POST':
        if topic.topiclikes.filter(user = user).exists():
            topic.topiclikes.get(user = user).delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            TopicLike.objects.create(user = user, topic = topic)
            return Response(status = status.HTTP_201_CREATED)
    