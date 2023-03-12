from ..models import Topic, Comment
from rest_framework.decorators import api_view
from django.http import Http404


@api_view(['POST'])
def like_topic(request, topic_id):
    try:
        topic = Topic.objects.get(id = topic_id)
    except Topic.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        if topic.likes.filter(user = request.user).exists():
            topic.get(user = request.user).delete()
        offset = 20
        params = dict(request.query_params)
        print(params)
        if 'cat' in params:
            if params['cat'][0] == 'all':
                topics = Topic.objects.all()
                category_slug = 'all'
            else:
                try:
                    category = Category.objects.get(slug = params['cat'][0])
                except Exception:
                    raise Http404
