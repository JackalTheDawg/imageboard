# Generated by Django 5.0.2 on 2024-02-29 09:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_followsprofiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.AlterField(
            model_name='followsprofiles',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='whos_followed', to='core.profile'),
        ),
        migrations.AlterField(
            model_name='followsprofiles',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_follow', to='core.profile'),
        ),
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('content', models.CharField(max_length=1000)),
                ('date', models.DateField(verbose_name=django.utils.timezone.now)),
                ('liked_by', models.ManyToManyField(related_name='likes', to='core.profile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.profile')),
            ],
        ),
    ]
