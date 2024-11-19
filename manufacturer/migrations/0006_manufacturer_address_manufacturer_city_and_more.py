# Generated by Django 5.1.2 on 2024-10-31 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturer', '0005_alter_manufacturer_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='company',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='idNumber',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='password1',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='password2',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='postalCode',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
