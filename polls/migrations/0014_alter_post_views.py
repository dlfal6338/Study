# Generated by Django 5.1.2 on 2024-11-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_alter_post_del_post_alter_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
