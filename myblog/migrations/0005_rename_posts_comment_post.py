# Generated by Django 5.0.6 on 2024-12-07 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0004_rename_comments_comment_post_alter_comment_posts_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='posts',
            new_name='post',
        ),
    ]
