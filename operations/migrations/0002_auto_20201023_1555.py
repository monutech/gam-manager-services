# Generated by Django 3.1.2 on 2020-10-23 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='advertiser',
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_name',
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='order',
            name='trafficker',
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_pql', models.CharField(max_length=255)),
                ('line_items', models.ManyToManyField(blank=True, null=True, related_name='line_items', to='operations.LineItem')),
                ('orders', models.ManyToManyField(blank=True, null=True, related_name='orders', to='operations.Order')),
            ],
        ),
    ]
