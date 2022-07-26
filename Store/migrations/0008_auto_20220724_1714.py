# Generated by Django 3.2.2 on 2022-07-24 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_auto_20220724_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='apartment',
            field=models.CharField(help_text='block or room number', max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingdetail',
            name='apartment',
            field=models.CharField(blank=True, help_text='block or room number', max_length=200, null=True),
        ),
    ]