# Generated by Django 3.2.7 on 2021-10-21 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instaid_app', '0002_instaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='id_board',
            name='query',
            field=models.CharField(default=False, max_length=255),
        ),
    ]
