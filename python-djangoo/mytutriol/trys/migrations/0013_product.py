# Generated by Django 5.1.1 on 2024-10-07 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trys', '0012_carr_ceo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
