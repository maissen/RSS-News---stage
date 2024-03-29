# Generated by Django 4.2.6 on 2024-01-11 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news_feed', '0006_delete_newsarticle_delete_searchhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='news_sources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(unique=True)),
                ('adding_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-adding_date'],
            },
        ),
    ]
