# Generated by Django 4.0.1 on 2022-11-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_advertisement_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='date',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
