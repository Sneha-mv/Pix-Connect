# Generated by Django 4.2.17 on 2024-12-17 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pixconnectapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotomanDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('aadhar_image', models.ImageField(upload_to='aadhar_images/')),
                ('place', models.CharField(max_length=100)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
