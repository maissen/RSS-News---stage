# Generated by Django 4.2.6 on 2024-01-26 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_feed', '0026_alter_newssource_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newssource',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]