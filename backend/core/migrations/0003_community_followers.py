# Generated by Django 5.0.2 on 2024-02-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_post_comments_alter_post_liked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='followers',
            field=models.ManyToManyField(related_name='community_followers', to='core.profile'),
        ),
    ]
