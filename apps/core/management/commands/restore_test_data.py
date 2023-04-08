import subprocess

from django.core.management import BaseCommand
from django.db import transaction

from apps.account.models import User
from apps.room.models import Room


class Command(BaseCommand):
    """Command for restoring test data for the system"""

    help = "Creates e2e data"

    def handle(self, *args, **options):
        subprocess.call(["python", "manage.py", "flush", "--noinput"])

        self.restore_test_data()

    @staticmethod
    def _create_users():
        # Hashed password "Admin123$"
        default_password = "pbkdf2_sha256$390000$2YQxNcXJRO0Y0R4oYp8COI$M059FCLHU+olmskmSxvBfOPJjPkbJ7NJQcfowC9lA10="

        superuser, created = User.objects.create(
            name="yamsa-admin",
            username="yamsa-admin",
            password=default_password,
            email="admin@yamsa.local",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        print(
            f'User ID: {superuser.id}, Name: "{superuser.name}" '
            f'{"created" if created else "found"}'
        )

        # --------------- NON GUEST USERS ---------------

        non_guest_user_1, created = User.objects.create(
            name="non_guest_user_1",
            username="non_guest_user_1",
            password=default_password,
            email="non_guest_user_1@yamsa.local",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            is_guest=False,
        )

        print(
            f'User ID: {non_guest_user_1.id}, Name: "{non_guest_user_1.name}" '
            f'{"created" if created else "found"}'
        )

        non_guest_user_2, created = User.objects.create(
            name="non_guest_user_2",
            username="non_guest_user_2",
            password=default_password,
            email="non_guest_user_2@yamsa.local",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            is_guest=False,
        )

        print(
            f'User ID: {non_guest_user_2.id}, Name: "{non_guest_user_2.name}" '
            f'{"created" if created else "found"}'
        )

        # --------------- GUEST USERS ---------------

        guest_user_1, created = User.objects.create(
            name="guest_user_1",
            username="guest_user_1",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            is_guest=True,
        )

        print(
            f'User ID: {guest_user_1.id}, Name: "{guest_user_1.name}" '
            f'{"created" if created else "found"}'
        )

        guest_user_2, created = User.objects.create(
            name="guest_user_2",
            username="guest_user_2",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            is_guest=True,
        )

        print(
            f'User ID: {guest_user_2.id}, Name: "{guest_user_2.name}" '
            f'{"created" if created else "found"}'
        )

    @staticmethod
    def _create_rooms():
        room_1, created = Room.objects.create(
            name="Room_1", description="Description for Room_1"
        )

        room_1.users.add(*[u.id for u in User.objects.all()])

        print(
            f'User ID: {room_1.id}, Name: "{room_1.name}" '
            f'{"created" if created else "found"}'
        )

    @staticmethod
    def restore_test_data():
        """
        Creates / "Finds" test data.

        Will create a superuser, a few guest_users, rooms and transactions
        """

        # Fake self for this method
        self = Command

        with transaction.atomic():
            self._create_users()

            self._create_rooms()