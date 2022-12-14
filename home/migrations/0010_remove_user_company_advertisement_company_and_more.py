# Generated by Django 4.0.1 on 2022-11-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_company_advertisements'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='company',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), related_name='company_advertisement', to='home.company'),
        ),
        migrations.AddField(
            model_name='user',
            name='companies',
            field=models.ManyToManyField(blank=True, null=True, to='home.Company'),
        ),
        migrations.AlterField(
            model_name='company',
            name='advertisements',
            field=models.ManyToManyField(blank=True, null=True, related_name='advertisementCompany', to='home.Advertisement'),
        ),
    ]
