# Generated by Django 5.1.1 on 2024-10-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trys', '0017_movieapp'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieapp',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
