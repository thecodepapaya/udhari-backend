# Generated by Django 3.2.6 on 2021-08-09 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udhari', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='udhari',
            old_name='isDone',
            new_name='is_done',
        ),
        migrations.RenameField(
            model_name='udhari',
            old_name='isMerged',
            new_name='is_merged',
        ),
    ]