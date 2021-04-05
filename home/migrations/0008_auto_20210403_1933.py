# Generated by Django 3.1 on 2021-04-03 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_auto_20210318_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command_id', models.IntegerField()),
                ('type', models.CharField(default='NULL', max_length=40)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=40)),
                ('price', models.IntegerField(default=0)),
                ('delivery_man', models.CharField(max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Note',
        ),
    ]