# Generated by Django 3.1.2 on 2020-10-23 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_auto_20201023_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gam_name', models.CharField(max_length=255)),
            ],
        ),
    ]
