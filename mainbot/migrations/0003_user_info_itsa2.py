# Generated by Django 4.2.6 on 2023-10-11 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbot', '0002_token_delete_asml_delete_cathay_delete_ctbc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='itsa2',
            field=models.BooleanField(default=False),
        ),
    ]
