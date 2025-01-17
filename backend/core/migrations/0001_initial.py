# Generated by Django 5.0.2 on 2024-02-28 08:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('email', models.CharField(max_length=100, unique=True, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(max_length=20)),
                ('profile_picture', models.CharField(default='static/media/assets/default_pp.png', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=10000)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('text', models.CharField(max_length=1000)),
                ('content', models.CharField(max_length=1000)),
                ('mime', models.CharField(max_length=20)),
                ('posted_as', models.CharField(default='profile', max_length=9)),
                ('comments', models.ManyToManyField(related_name='commentary', to='core.profile')),
                ('liked_by', models.ManyToManyField(related_name='liked', to='core.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('private', models.BooleanField(default=False)),
                ('image', models.CharField(default='static/media/assets/default_pp.png', max_length=1000)),
                ('admins', models.ManyToManyField(related_name='community_admins', to='core.profile')),
            ],
        ),
    ]
