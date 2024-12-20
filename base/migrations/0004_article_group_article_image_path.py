# Generated by Django 5.1.3 on 2024-11-11 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_article_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="group",
            field=models.CharField(
                blank=True,
                help_text="Category or group of the article, e.g., 'Statistics'",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="image_path",
            field=models.CharField(
                blank=True,
                help_text="URL or path to the article's image",
                max_length=255,
            ),
        ),
    ]
