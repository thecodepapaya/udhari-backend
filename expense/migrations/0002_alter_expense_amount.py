# Generated by Django 3.2.6 on 2021-08-09 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
