# Generated by Django 5.1.2 on 2024-11-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_remove_request2_deadline_request2_expire'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='deadline',
        ),
        migrations.AddField(
            model_name='request',
            name='expire',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]