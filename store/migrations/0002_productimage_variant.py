# Generated by Django 5.0 on 2024-01-09 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
                ('stock', models.IntegerField()),
                ('price_modifier', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('ram', models.CharField(blank=True, max_length=50, null=True)),
                ('storage', models.CharField(blank=True, max_length=50, null=True)),
                ('battery', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_available', models.BooleanField(default=True, null=True)),
                ('image', models.ImageField(null=True, upload_to='varient_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]