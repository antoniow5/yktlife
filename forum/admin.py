from django.contrib import admin
from forum.models import Category, Tag, Topic, Comment, TopicLike, CommentLike

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(TopicLike)
admin.site.register(CommentLike)
# Register your models here.
