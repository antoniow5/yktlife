from django.contrib import admin
from forum.models import Category, Tag, Topic, Comment, Like

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Like)
# Register your models here.
