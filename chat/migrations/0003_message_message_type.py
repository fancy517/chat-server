# Generated by Django 2.2.13 on 2020-10-06 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20201005_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.TextField(default='text'),
        ),
    ]
