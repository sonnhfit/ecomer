# Generated by Django 2.1.5 on 2019-01-31 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
