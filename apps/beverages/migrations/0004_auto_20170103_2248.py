# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration', '0002_user_alias'),
        ('beverages', '0003_try'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavorPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favor_point', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favor_beverage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favor_beverage', to='beverages.Beverage')),
                ('favor_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_and_registration.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='try',
            name='try_beverage',
        ),
        migrations.RemoveField(
            model_name='try',
            name='try_user',
        ),
        migrations.DeleteModel(
            name='Try',
        ),
    ]
