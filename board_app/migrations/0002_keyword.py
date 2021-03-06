# Generated by Django 3.2.7 on 2021-09-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=255)),
                ('writeData', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('reply', models.CharField(max_length=255)),
                ('replyList', models.TextField(null=True)),
                ('like', models.CharField(max_length=255)),
                ('user_name', models.CharField(max_length=255)),
                ('user_pk', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
            ],
        ),
    ]
