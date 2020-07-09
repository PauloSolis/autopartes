# Generated by Django 2.2.10 on 2020-07-09 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='productos.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_code', models.CharField(max_length=100, unique=True)),
                ('product_code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('car_brand', models.CharField(max_length=100, null=True)),
                ('car_model', models.CharField(max_length=100, null=True)),
                ('car_year', models.IntegerField(null=True)),
                ('public_price', models.FloatField()),
                ('card_price', models.FloatField(null=True)),
                ('master_price', models.FloatField(null=True)),
                ('wholesale_price', models.FloatField(null=True)),
                ('dozen_price', models.FloatField(null=True)),
                ('image1', models.ImageField(blank=True, upload_to='images/%Y/%m/%d')),
                ('image2', models.ImageField(blank=True, upload_to='images/%Y/%m/%d')),
                ('in_stock', models.IntegerField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Category')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.SubCategory')),
            ],
        ),
    ]
