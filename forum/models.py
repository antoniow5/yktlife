from django.db import models
from django.conf import settings

class Category(models.Model):
    position_column = models.PositiveSmallIntegerField()
    position_order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length= 20)    #Проверить по дизайну максимальную длину названия
    slug = models.SlugField(max_length=10, null = False, blank = False, unique = True)
    description = models.CharField(max_length = 1000)
    
   

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30) #Проверить по дизайну максимальную длину топика
    text = models.CharField(max_length = 10000)

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length = 10000)

class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class TopicVote(models.Model):
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
