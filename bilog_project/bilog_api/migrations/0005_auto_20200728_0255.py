# Generated by Django 3.0.8 on 2020-07-27 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bilog_api', '0004_chat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='reciever',
            new_name='receiver',
        ),
    ]
