# Generated by Django 3.2.6 on 2021-08-09 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udhari', '0002_auto_20210810_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='udhari',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
