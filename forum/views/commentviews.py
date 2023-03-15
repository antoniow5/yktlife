from rest_framework.decorators import api_view
from ..models import Category, Tag, Topic, Comment


@api_view(['GET','POST'])
def comments_list(request):
    if request.method == 'GET':
        params = dict(request.query_params)
        
        if "cat" in params:
            comments = Comment.objects.filter(topic__category = Category.objects.get(slug=params['cat'][0]))
            

