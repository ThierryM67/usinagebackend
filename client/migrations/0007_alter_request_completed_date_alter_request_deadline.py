# Generated by Django 5.1.2 on 2024-10-31 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_client_address_client_city_client_password1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='completed_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='deadline',
            field=models.IntegerField(),
        ),
    ]