from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from forum.serializers import TopicListSerializer, TopicCreateUpdateSerializer, TopicDetailSerializer, TopicCommentsDetailSerializer, TopicEditSerializer
from ..models import Category, Tag, Topic, Comment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from django.core.paginator import Paginator
# from .exceptiondicts import responce_dicts
from django.db.models import Max, Count
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models.functions import Coalesce

@api_view(['GET','POST'])
def topics_list(request):
    if request.method == 'GET':

        params = dict(request.query_params)
        if 'cat' in params:
            if params['cat'][0] == 'all':
                topics = Topic.objects.all()
                category_slug = 'all'
            else:
                try:
                    category = Category.objects.get(slug = params['cat'][0])
                except Exception:
                    raise Http404
                
                if 'tag' in params:
                    if params['tag'][0] == 'null':
                        tag = None
                    else:
                        try:
                            tag = Tag.objects.get(id = int(params['tag'][0]))
                        except Exception as e:
                            return Response( status = status.HTTP_400_BAD_REQUEST)
                    topics = topics.filter(tag = tag)
                
                topics = Topic.objects.filter(category = category)
                category_slug = category.slug
            if not topics.exists():
                content = {"message": "Опубликованных тем еще нет. Стантьте первым!"}
                return Response(content, status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        

        if 'order' in params:
            if params['order'][0] == 'created':
                comment_order = False
                topics = topics.order_by('-created_at')
            if params['order'][0] == 'comment':
                topics = topics.annotate(last_comment_or_created=Coalesce(Max('comments__created_at'), "created_at")).order_by('-last_comment_or_created')
                comment_order = True
        else:
            topics = topics.order_by('-created_at')
            comment_order = False

        page = 1
        offset = 20
        try:
            if 'page' in params and int(params['page'][0]) > 0: #вот тут поправить чтобы не было исключений сервера. Пейдж может быть не интом
                page = int(params['page'][0])
        except Exception as e:
            return Response( status = status.HTTP_400_BAD_REQUEST)
        try:
            if 'offset' in params and int(params['offset'][0]) > 0:
                offset = int(params['offset'][0])
        except Exception as e:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        topics = topics.values_list('id', flat = True)
        paginator = Paginator(topics, offset)


        try:
            paginated_topics = paginator.page(page)
        except Exception as e:
            raise Http404      
        
        paginated_topics_query = Topic.objects.filter(id__in = paginated_topics)
        paginated_topics_query = paginated_topics_query.annotate(last_comment_or_created=Coalesce(Max('comments__created_at'), "created_at"))
        paginated_topics_query = paginated_topics_query.select_related('category')
        paginated_topics_query = paginated_topics_query.select_related('user')
        paginated_topics_query = paginated_topics_query.select_related('tag')
        paginated_topics_query = paginated_topics_query.prefetch_related('comments').annotate(comments_count = Count('comments'))
        paginated_topics_query = paginated_topics_query.prefetch_related('topiclikes')
        paginated_topics_query = paginated_topics_query.defer("category__description", 
                                "text",
                                "tag__category_id",
                                "user__password",
                                "user__last_login",
                                "user__email",
                                "user__is_active",
                                "user__date_joined",
                                "category__position_column",
                                "category__position_order", 
                            )
        if comment_order:
            paginated_topics_query = paginated_topics_query.order_by('-last_comment_or_created')
        if not comment_order:
            paginated_topics_query = paginated_topics_query.order_by('-created_at')
        # paginated_topics_query = TopicListSerializer.setup_eager_loading(paginated_topics.object_list)
        serializer = TopicListSerializer(paginated_topics_query,many=True)
        if paginated_topics.has_next():
            next_url = f"/api/v1/forum/topics?cat={category_slug}&page={page+1}&offset={offset}"
        else:
            next_url = None
        if paginated_topics.has_previous():
            previous_url = f"/api/v1/forum/topics?cat={category_slug}&page={page-1}&offset={offset}"
        else:
            previous_url = None
        return_dict = { 
                'pages_num' : paginator.num_pages,
                'topics_num': paginator.count,
                'has_next': paginated_topics.has_next(),
                'has_previous': paginated_topics.has_previous(),
                'next_url': next_url,
                'previous_url': previous_url,
                'results': serializer.data
            }

        return Response(return_dict)

    elif(request.method == 'POST'):
        if request.user.is_authenticated:
            if request.user.is_superuser:

                serializer = TopicCreateUpdateSerializer(data = request.data, context = {'request':request})
            else:
                if not Category.objects.get(slug=request.data['category']).can_post:
                    raise PermissionDenied
            if serializer.is_valid():
                serializer.save()
                return Response(status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied({"message":"You don't have permission"})


@api_view(['GET','PATCH', 'DELETE'])
def topics_detail(request, id):
    try:
        topic = Topic.objects.get(id = id)
    except Topic.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        params = dict(request.query_params)
        if 'show' in params:
            if params['show'][0] == 'simple':
                serializer = TopicDetailSerializer(topic, context = {'request':request})
        else:
            serializer = TopicCommentsDetailSerializer(topic, context = {'request':request})
        return Response(serializer.data)

    elif(request.method == 'PATCH'):
        if request.user.is_superuser:
            serializer = TopicEditSerializer(topic, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status= status.HTTP_201_CREATED)
            return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        elif request.user == topic.user:
            if timezone.now() - topic.created_at < timedelta(hours = 1):
                serializer = TopicEditSerializer(topic, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status= status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
            else: 
                return Response(f'Вы не можете редактировать топик, так как прошло более {timezone.now() - topic.created_at} минут', status= status.HTTP_400_BAD_REQUEST)
        else: 
            raise PermissionDenied({"message":"You don't have permission"})
        
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            topic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied({"message":"You don't have permission"})
        # Поправить таймзоны
        # Поправить таймзоны
        # Поправить таймзоны
        # Поправить таймзоны
        # Поправить таймзоны
        # Поправить таймзоны
        # Поправить таймзоны
# # 204 NotFound