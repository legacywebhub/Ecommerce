# Generated by Django 3.2.2 on 2022-07-24 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_auto_20220724_0144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletter',
            old_name='sent',
            new_name='sent_mail',
        ),
    ]
