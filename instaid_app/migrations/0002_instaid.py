# Generated by Django 3.2.7 on 2021-10-19 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instaid_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instaid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_id', models.CharField(max_length=100)),
                ('crawling_date', models.CharField(max_length=100)),
                ('profile', models.CharField(max_length=100)),
                ('media_type', models.CharField(max_length=255)),
                ('media_url', models.CharField(max_length=255)),
                ('media_views', models.CharField(max_length=255)),
                ('media_title', models.CharField(max_length=255)),
                ('comments_cnt', models.CharField(max_length=255)),
                ('like_cnt', models.CharField(max_length=255)),
            ],
        ),
    ]
