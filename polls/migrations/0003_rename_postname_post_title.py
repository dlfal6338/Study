# Generated by Django 5.1.2 on 2024-11-14 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_post_delete_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='postname',
            new_name='title',
        ),
    ]