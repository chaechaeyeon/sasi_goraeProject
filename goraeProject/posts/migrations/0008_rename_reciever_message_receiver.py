# Generated by Django 4.2.3 on 2023-07-29 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_rename_point_userinfo_points_message_points_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='reciever',
            new_name='receiver',
        ),
    ]
