# Generated by Django 3.2.18 on 2023-03-16 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blabhear', '0003_message'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notification',
            new_name='UserNotification',
        ),
    ]