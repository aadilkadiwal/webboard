# Generated by Django 4.0.1 on 2022-02-24 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_topic_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='last_updated',
            new_name='created',
        ),
    ]