# Generated by Django 2.2.10 on 2020-04-14 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_retailer',
            field=models.BooleanField(default=True),
        ),
    ]
