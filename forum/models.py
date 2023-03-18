from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class Category(models.Model):
    name = models.CharField(max_length= 20)    #Проверить по дизайну максимальную длину названия
    slug = models.SlugField(max_length=10, null = False, blank = False, unique = True)
    description = models.CharField(max_length = 1000)
    position_column = models.PositiveSmallIntegerField()
    position_order = models.PositiveSmallIntegerField()
    users_can_post = models.BooleanField(default = True)
    users_can_comment = models.BooleanField(default = True)
    max_comment = models.PositiveSmallIntegerField(default = 250)
    # can_like = models.BooleanField(default=True)
    
    # Логотип
    # Логотип на мобиле
    # Возможно позиция на мобиле
    class Meta:
        ordering = ['position_column', 'position_order']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name + ' /' + self.slug + ' [' + str(self.position_column) + ',' + str(self.position_order) + ']'  
    

    def save(self, *args, **kwargs):
        update_down_categories = Category.objects.filter(position_column = self.position_column)
        for update_down_category in update_down_categories:
            if update_down_category.position_order >= self.position_order:
                update_down_category.position_order += 1
                update_down_category.save()
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length= 20)    #Проверить по дизайну максимальную длину названия
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.category.name + ' /' + self.name + ' [' + str(self.id) + ']'  
    
    def save(self, *args, **kwargs):
        update_tags = Tag.objects.filter(category = self.category)
        for update_tag in update_tags:
            if update_tag.order >= self.order:
                update_tag.order += 1
                update_tag.save()
        super(Tag, self).save(*args, **kwargs)



class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = False, db_index = True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null = True, default= None, )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=30) #Проверить по дизайну максимальную длину топика
    text = models.CharField(max_length = 10000)
    is_anonymous = models.BooleanField(default=False)
    modified_at = models.DateTimeField(null=True, default = None)
    is_closed = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default = False)
    is_best = models.BooleanField(default = False)
    class Meta:
        indexes = [
                models.Index(fields=['category']),
                models.Index(fields=['category', 'tag', 'user']),
                models.Index(fields=['-created_at']),

            ]
    def save(self, *args, **kwargs):
        if not self.tag == None:
            if not self.tag.category == self.category:
                raise ValueError
            
        super(Topic, self).save(*args, **kwargs)
        
   

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length = 10000)
    is_anonymous = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null = True, blank = True, on_delete=models.CASCADE, related_name='children')
    is_removed = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if not self.parent == None:
            if not self.parent.parent == None:
                raise ValueError
            if not self.parent.topic == self.topic:
                raise ValueError
        if (self.topic.comments.all().count() >= self.topic.category.max_comment) and (not self.topic.is_closed):
            self.topic.is_closed = True
            self.topic.save()
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        indexes = [
                models.Index(fields=['created_at']),
                models.Index(fields=['topic']),
                models.Index(fields=['user'])

            ]

class TopicLike(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topiclikes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topiclikes')

    class Meta:
        unique_together = ('user', 'topic')
        indexes = [

                models.Index(fields=['topic']),
                models.Index(fields=['user'])

            ]


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentlikes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commentlikes')

    class Meta:
        unique_together = ('user', 'comment')


    # https://stackoverflow.com/questions/62131125/vote-only-once-in-django-to-posts-and-comments
