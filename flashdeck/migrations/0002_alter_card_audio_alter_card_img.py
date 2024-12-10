# Generated by Django 5.1.1 on 2024-12-06 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeck', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='audio',
            field=models.FileField(blank=True, default=None, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='card',
            name='img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/'),
        ),
    ]