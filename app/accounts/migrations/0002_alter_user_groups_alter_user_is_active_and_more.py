# Generated by Django 4.0.6 on 2022-08-28 14:33

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True,
                                         related_name='user_set',
                                         related_query_name='user',
                                         to='auth.group',
                                         verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True,
                                      verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False,
                                      verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False,
                                      verbose_name='superuser status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True,
                                         related_name='user_set', related_query_name='user',
                                         to='auth.permission',
                                         verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                   max_length=150, unique=True,
                                   validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                                   verbose_name='username'),
        ),
    ]
