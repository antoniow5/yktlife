from django.db import models
from django.conf import settings

class Category(models.Model):
    position_column = models.PositiveSmallIntegerField()
    position_order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length= 20)    #Проверить по дизайну максимальную длину названия
    slug = models.SlugField(max_length=10, null = False, blank = False, unique = True)
    description = models.CharField(max_length = 1000)
    can_post = models.BooleanField(default = True)
    can_comment = models.BooleanField(default = True)
    can_like = models.BooleanField(default = True)
    # Логотип
    # Логотип на мобиле
    # Возможно позиция на мобиле
    class Meta:
        ordering = ['position_column', 'position_order']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name + ' /' + self.slug + ' [' + str(self.position_column) + ',' + str(self.position_order) + ']'  
    
class Tag(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length= 20)    #Проверить по дизайну максимальную длину названия
    slug = models.CharField(max_length = 10)

    def __str__(self):
        return self.category.name + ' /' + self.name + ' [' + self.slug + ']'  

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null = True, default= None)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30) #Проверить по дизайну максимальную длину топика
    text = models.CharField(max_length = 10000)
    is_anonymous = models.BooleanField(default=False)
    modified_at = models.DateTimeField(null=True, default = None)

        
   

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length = 10000)
    is_anonymous = models.BooleanField(default=False)


class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class TopicVote(models.Model):
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://stackoverflow.com/questions/62131125/vote-only-once-in-django-to-posts-and-comments
