# Generated by Django 4.2.17 on 2024-12-17 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pixconnectapp', '0002_photomandetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotographyImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='working_images/')),
                ('spot', models.CharField(max_length=100)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('photographer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_images', to='pixconnectapp.photomandetails')),
            ],
        ),
    ]
