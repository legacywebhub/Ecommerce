# Generated by Django 3.2.2 on 2022-07-18 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='Images/Company')),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('email1', models.EmailField(max_length=254)),
                ('email2', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone1', models.CharField(max_length=25)),
                ('phone2', models.CharField(blank=True, max_length=25, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook_link', models.URLField(blank=True, max_length=2000, null=True)),
                ('twitter_link', models.URLField(blank=True, max_length=2000, null=True)),
                ('instagram_link', models.URLField(blank=True, max_length=2000, null=True)),
                ('youtube_link', models.URLField(blank=True, null=True)),
                ('ad1', models.TextField(blank=True, max_length=3000, null=True)),
                ('ad2', models.TextField(blank=True, max_length=3000, null=True)),
                ('public_key', models.CharField(blank=True, max_length=160, null=True)),
                ('secret_key', models.CharField(blank=True, max_length=160, null=True)),
                ('google_analytics', models.TextField(blank=True, max_length=2000, null=True)),
            ],
        ),
    ]