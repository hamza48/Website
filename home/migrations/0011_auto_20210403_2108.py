# Generated by Django 3.1 on 2021-04-03 21:08

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20210403_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='status',
            field=models.CharField(choices=[(home.models.StateOfOrder['ToBeConfirmed'], 0), (home.models.StateOfOrder['Confirmed'], 1), (home.models.StateOfOrder['ToBeDelivred'], 2), (home.models.StateOfOrder['Delivred'], 3), (home.models.StateOfOrder['Canceled'], 4)], default=home.models.StateOfOrder['ToBeConfirmed'], max_length=30),
        ),
    ]
