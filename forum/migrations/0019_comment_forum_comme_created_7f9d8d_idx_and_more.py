# Generated by Django 4.1.7 on 2023-03-12 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0018_remove_topic_forum_topic_categor_1b5df2_idx_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created_at'], name='forum_comme_created_7f9d8d_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['topic'], name='forum_comme_topic_i_48ba22_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['user'], name='forum_comme_user_id_f28cc6_idx'),
        ),
        migrations.AddIndex(
            model_name='topiclike',
            index=models.Index(fields=['topic'], name='forum_topic_topic_i_6be3ce_idx'),
        ),
        migrations.AddIndex(
            model_name='topiclike',
            index=models.Index(fields=['user'], name='forum_topic_user_id_aafa76_idx'),
        ),
    ]
