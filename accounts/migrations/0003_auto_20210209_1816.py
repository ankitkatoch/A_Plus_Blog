# Generated by Django 3.1.6 on 2021-02-09 12:46

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='.../blog/static/img/demo.jpg', upload_to=accounts.models.upload_location),
        ),
    ]
