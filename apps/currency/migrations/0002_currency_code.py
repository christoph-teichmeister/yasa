# Generated by Django 4.1.9 on 2023-10-03 11:40

from django.db import migrations, models


def set_currency_codes(apps, schema_editor):
    Currency = apps.get_model("currency", "Currency")
    db_alias = schema_editor.connection.alias

    for currency in Currency.objects.using(db_alias).all():
        if currency.name == "Pound Sterling":
            currency.code = "GBP"

        if currency.name == "Euro":
            currency.code = "EUR"

        currency.save()


class Migration(migrations.Migration):
    dependencies = [
        ("currency", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="currency",
            name="code",
            field=models.CharField(default="eur", max_length=5),
            preserve_default=False,
        ),
        migrations.RunPython(set_currency_codes, migrations.RunPython.noop),
    ]
