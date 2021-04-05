# Generated by Django 3.1 on 2021-01-31 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_auto_20210126_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='First_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='Last_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='emailRegistration',
        ),
        migrations.RemoveField(
            model_name='client',
            name='pswRegistration1',
        ),
        migrations.RemoveField(
            model_name='client',
            name='pswRegistration2',
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]