# Generated by Django 3.1.6 on 2021-03-21 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udhari', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='udhari',
            name='notes',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
