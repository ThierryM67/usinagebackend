# Generated by Django 5.1.2 on 2024-10-31 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturer', '0004_manufacturer_profile_name_manufacturer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='profile_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
