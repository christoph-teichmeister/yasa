# Generated by Django 5.0.6 on 2024-06-15 08:16

from django.db import migrations


def delete_old_news(apps, schema_editor):
    News = apps.get_model("news", "News")
    db_alias = schema_editor.connection.alias

    News.objects.using(db_alias).delete()


def create_generic_news(apps, schema_editor):
    News = apps.get_model("news", "News")
    ParentTransaction = apps.get_model("transaction", "ParentTransaction")
    db_alias = schema_editor.connection.alias

    for transaction in ParentTransaction.objects.all().order_by("created_at"):
        description = (
            transaction.description[:85] + "..." if len(transaction.description) > 90 else transaction.description
        )
        News.objects.using(db_alias).create(
            title=f'"{description}" created',
            room=transaction.room,
            created_by=transaction.created_by,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0006_alter_news_options_remove_news_highlighted"),
    ]

    operations = [
        migrations.RunPython(delete_old_news, migrations.RunPython.noop),
        migrations.RunPython(create_generic_news, migrations.RunPython.noop),
    ]
