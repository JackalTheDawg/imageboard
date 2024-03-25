# Generated by Django 5.0.2 on 2024-02-28 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='commentary', to='core.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked', to='core.profile'),
        ),
    ]
