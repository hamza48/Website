# Generated by Django 3.1 on 2021-01-26 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailRegistration', models.CharField(max_length=200)),
                ('pswRegistration1', models.CharField(max_length=200)),
                ('pswRegistration2', models.CharField(max_length=200)),
                ('generator_token', models.CharField(max_length=8)),
                ('First_name', models.CharField(max_length=200)),
                ('Last_name', models.CharField(max_length=200)),
                ('logged_in', models.BooleanField(default=False)),
                ('mail_verified', models.BooleanField(default=False)),
                ('sexe', models.CharField(default='NULL', max_length=30)),
                ('adresse', models.CharField(default='', max_length=400)),
                ('Telephone', models.CharField(default='', max_length=10)),
                ('Date_of_registration', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
