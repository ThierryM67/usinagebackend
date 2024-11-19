# Generated by Django 5.1.2 on 2024-10-28 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0002_news_alter_request_file1_alter_request_file2_and_more'),
        ('manufacturer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('reciepient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='manufacturer.manufacturer')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='client.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='client.client')),
            ],
        ),
        migrations.CreateModel(
            name='ManufacturerMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('reciepient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='client.client')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='manufacturer.manufacturer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='manufacturer.manufacturer')),
            ],
        ),
    ]