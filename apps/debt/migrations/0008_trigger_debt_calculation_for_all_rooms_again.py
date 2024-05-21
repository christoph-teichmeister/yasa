# Generated by Django 4.1.9 on 2023-10-08 13:36

from django.conf import settings
from django.db import migrations

from apps.debt.handlers.events.optimise_debts import calculate_optimised_debts
from apps.transaction.messages.events.transaction import ParentTransactionUpdated


def triggers_debt_calculation_for_all_rooms(apps, schema_editor):
    Room = apps.get_model("room", "Room")

    db_alias = schema_editor.connection.alias

    for room in Room.objects.using(db_alias).all():
        transaction = room.parent_transactions.first()

        calculate_optimised_debts(context=ParentTransactionUpdated.Context(parent_transaction=transaction, room=room))


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("debt", "0007_rename_newdebt_debt_alter_debt_options"),
    ]

    operations = [
        migrations.RunPython(triggers_debt_calculation_for_all_rooms, migrations.RunPython.noop),
    ]
