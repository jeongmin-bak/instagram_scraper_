# Generated by Django 3.2.7 on 2021-09-30 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HelloWorld',
            fields=[
                ('text', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
    ]