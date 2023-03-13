# Generated by Django 4.1.7 on 2023-03-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_alter_commentlike_unique_together_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='topic',
            index=models.Index(fields=['category'], name='forum_topic_categor_e92d61_idx'),
        ),
        migrations.AddIndex(
            model_name='topic',
            index=models.Index(fields=['category', 'tag'], name='forum_topic_categor_1b5df2_idx'),
        ),
    ]