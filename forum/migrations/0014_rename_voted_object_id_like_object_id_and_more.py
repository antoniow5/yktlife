# Generated by Django 4.1.7 on 2023-03-12 05:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0013_like_remove_topicvote_topic_remove_topicvote_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='voted_object_id',
            new_name='object_id',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'object_id', 'content_type')},
        ),
    ]
