# Generated by Django 5.0.6 on 2024-06-15 08:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0005_news_room"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="news",
            options={"ordering": ("-id",), "verbose_name": "News", "verbose_name_plural": "News"},
        ),
        migrations.RemoveField(
            model_name="news",
            name="highlighted",
        ),
        migrations.RemoveField(
            model_name="news",
            name="message",
        ),
        migrations.DeleteModel(
            name="NewsComment",
        ),
    ]
