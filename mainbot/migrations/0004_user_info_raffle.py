# Generated by Django 4.2.6 on 2023-10-11 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbot', '0003_user_info_itsa2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='raffle',
            field=models.IntegerField(default=0),
        ),
    ]
