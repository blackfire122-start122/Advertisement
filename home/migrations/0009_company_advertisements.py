# Generated by Django 4.0.1 on 2022-10-22 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_advertisement_email_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='advertisements',
            field=models.ManyToManyField(blank=True, null=True, to='home.Advertisement'),
        ),
    ]