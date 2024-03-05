# Generated by Django 5.0 on 2024-01-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_userprofile_otp_userprofile_wallet_balance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='user_profile',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='variant',
            old_name='brand',
            new_name='fittings',
        ),
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(default='00000', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='variant',
            name='discount_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='variant',
            name='image2',
            field=models.ImageField(null=True, upload_to='variant_images'),
        ),
        migrations.AddField(
            model_name='variant',
            name='image3',
            field=models.ImageField(null=True, upload_to='variant_images'),
        ),
        migrations.AddField(
            model_name='variant',
            name='price',
            field=models.DecimalField(decimal_places=2, default=500, max_digits=10),
        ),
        migrations.AlterField(
            model_name='variant',
            name='image',
            field=models.ImageField(null=True, upload_to='variant_images'),
        ),
    ]