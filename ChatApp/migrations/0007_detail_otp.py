# Generated by Django 3.1.7 on 2021-05-13 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0006_cast'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='otp',
            field=models.IntegerField(null=True),
        ),
    ]