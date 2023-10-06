# Generated by Django 4.1.9 on 2023-10-03 14:38
from decimal import Decimal

from django.conf import settings
from django.db import migrations
from django.db.models import Q

from apps.core.utils import add_or_update_dict


def translate_old_debts_to_new_debts(apps, schema_editor):
    OldDebt = apps.get_model("debt", "Debt")
    NewDebt = apps.get_model("debt", "NewDebt")

    Room = apps.get_model("room", "Room")
    Currency = apps.get_model("currency", "Currency")

    db_alias = schema_editor.connection.alias

    # Handle settled debts
    for debt in OldDebt.objects.using(db_alias).filter(settled=True):
        if debt.user != debt.transaction.paid_by:
            new_debt_qs = NewDebt.objects.using(db_alias).filter(
                debitor=debt.user,
                creditor=debt.transaction.paid_by,
                room=debt.transaction.room,
                currency=debt.transaction.currency,
                settled=True,
            )

            if new_debt_qs.exists():
                new_debt = new_debt_qs.first()
                new_debt.value += debt.transaction.value
                new_debt.save()
            else:
                NewDebt.objects.using(db_alias).create(
                    debitor=debt.user,
                    creditor=debt.transaction.paid_by,
                    room=debt.transaction.room,
                    currency=debt.transaction.currency,
                    value=debt.transaction.value,
                    settled=True,
                    settled_at=debt.settled_at,
                )

    # Handle open debts
    for debt in OldDebt.objects.using(db_alias).filter(settled=False):
        if debt.user != debt.transaction.paid_by:
            new_debt_qs = NewDebt.objects.using(db_alias).filter(
                debitor=debt.user,
                creditor=debt.transaction.paid_by,
                room=debt.transaction.room,
                currency=debt.transaction.currency,
                settled=False,
            )

            if new_debt_qs.exists():
                new_debt = new_debt_qs.first()
                new_debt.value += debt.transaction.value
                new_debt.save()
            else:
                NewDebt.objects.using(db_alias).create(
                    debitor=debt.user,
                    creditor=debt.transaction.paid_by,
                    room=debt.transaction.room,
                    currency=debt.transaction.currency,
                    value=debt.transaction.value,
                    settled=False,
                    settled_at=debt.settled_at,
                )

    # Optimise open debts
    for room in Room.objects.using(db_alias).all():
        all_debts_of_room_tuple = tuple(
            OldDebt.objects.filter(transaction__room_id=room.id, settled=False)
            .order_by("transaction__value", "transaction__currency__sign")
            .values_list("transaction__currency__sign", "user", "transaction__paid_by", "transaction__value")
        )

        currency_debts = {}
        for currency_sign, debtor, creditor, amount in all_debts_of_room_tuple:
            debt_tuple = (debtor, creditor, amount)
            if currency_debts.get(currency_sign) is None:
                currency_debts[currency_sign] = [debt_tuple]
            else:
                currency_debts[currency_sign].append(debt_tuple)

        currency_transactions = {}
        for currency_sign, debt_list in currency_debts.items():
            # Create a dictionary to track how much each person owes or is owed
            balances = {}

            # Populate the balances dictionary based on the provided debts
            for debtor, creditor, amount in debt_list:
                balances[debtor] = balances.get(debtor, 0) - amount
                balances[creditor] = balances.get(creditor, 0) + amount

            # Initialize two lists for debtors and creditors
            debtors = []
            creditors = []

            # Separate debtors and creditors, ignoring those with a balance of 0
            for person, balance in balances.items():
                if balance < 0:
                    debtors.append((person, balance))
                elif balance > 0:
                    creditors.append((person, balance))

            # Sort debtors and creditors based on the owed amounts
            debtors.sort(key=lambda x: x[1])
            creditors.sort(key=lambda x: x[1], reverse=True)

            # Initialize a list to track the transactions
            transactions = []

            # Perform debt consolidation
            while debtors and creditors:
                debtor, debt = debtors[0]
                creditor, credit = creditors[0]

                # Calculate the amount to transfer
                transfer_amount = min(-debt, credit)

                # Update balances and create a transaction
                balances[debtor] += transfer_amount
                balances[creditor] -= transfer_amount

                # Add the transaction to the list
                transactions.append((debtor, creditor, transfer_amount))

                # Remove debtors and creditors with zero balance
                if balances[debtor] == 0:
                    debtors.pop(0)
                if balances[creditor] == 0:
                    creditors.pop(0)

            currency_transactions[currency_sign] = transactions

        created_debt_ids_tuple = ()
        touched_debt_ids_tuple = ()
        for currency_sign, transaction_list in currency_transactions.items():
            for debtor, creditor, transfer_amount in transaction_list:
                debt_qs = NewDebt.objects.filter(
                    room=room,
                    debitor=debtor,
                    creditor=creditor,
                    currency__sign=currency_sign,
                    settled=False,
                )

                if not debt_qs.exists():
                    if transfer_amount != Decimal(0):
                        created_debt_ids_tuple += (
                            NewDebt.objects.create(
                                debitor_id=debtor,
                                creditor_id=creditor,
                                room=room,
                                value=transfer_amount,
                                currency=Currency.objects.get(sign=currency_sign),
                            ).id,
                        )
                        continue

                if debt_qs.count() == 1:
                    debt = debt_qs.first()
                    if transfer_amount != Decimal(0):
                        debt.value = transfer_amount
                        debt.save()
                        touched_debt_ids_tuple += (debt.id,)
                    else:
                        debt.delete()

            # Delete any untouched, unsettled debt objects
            NewDebt.objects.exclude(
                Q(id__in=(created_debt_ids_tuple + touched_debt_ids_tuple)) | Q(settled=True)
            ).delete()


def reverse_delete_all_new_debts(apps, schema_editor):
    NewDebt = apps.get_model("debt", "NewDebt")

    NewDebt.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("debt", "0003_newdebt"),
        ("transaction", "0006_populate_new_m2m_connection"),
    ]

    operations = [
        migrations.RunPython(translate_old_debts_to_new_debts, reverse_delete_all_new_debts),
    ]
