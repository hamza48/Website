# Generated by Django 3.1 on 2021-04-03 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20210403_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='command_id',
        ),
    ]
