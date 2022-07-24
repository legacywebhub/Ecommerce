# Generated by Django 3.2.2 on 2022-07-23 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_auto_20220718_0500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=160)),
                ('file', models.FileField(blank=True, null=True, upload_to='Images/Newsletter')),
                ('body', models.TextField(blank=True, max_length=5000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
