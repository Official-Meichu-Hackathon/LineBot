# Generated by Django 4.2.6 on 2023-10-12 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbot', '0006_rename_ruffle_raffle'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='prize',
            field=models.CharField(default='None', max_length=255),
        ),
    ]