# Generated by Django 5.1.2 on 2024-11-28 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_alter_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_comment',
            name='del_comment',
            field=models.BooleanField(default=False),
        ),
    ]
