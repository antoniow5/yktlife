from django.contrib import admin
from forum.models import Category, Tag, Topic, Comment

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(Comment)
# Register your models here.
