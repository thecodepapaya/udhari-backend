# Generated by Django 3.1.6 on 2021-05-23 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udhari_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='udhariuser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='udhariuser',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='udhariuser',
            name='password',
        ),
    ]
