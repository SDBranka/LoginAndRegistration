# Generated by Django 2.2 on 2021-06-07 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_user_birthday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='birthday',
            new_name='birthdate',
        ),
    ]
