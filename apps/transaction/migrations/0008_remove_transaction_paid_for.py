# Generated by Django 4.1.9 on 2023-10-14 05:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("transaction", "0007_populate_new_m2m_connection_again"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="paid_for",
        ),
    ]
