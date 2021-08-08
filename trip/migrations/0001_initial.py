# Generated by Django 3.2.6 on 2021-08-08 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('udhari_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New Trip', max_length=30)),
                ('notes', models.CharField(blank=True, default='', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_creator', to='udhari_user.udhariuser')),
            ],
        ),
    ]
