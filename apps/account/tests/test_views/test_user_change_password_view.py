import http

from django.contrib.auth import authenticate
from django.urls import reverse
from model_bakery import baker

from apps.account.tests.baker_recipes import default_password
from apps.account.views import UserChangePasswordView, UserDetailView
from apps.core.tests.setup import BaseTestSetUp


class UserChangePasswordViewBaseTest(BaseTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make_recipe("apps.account.tests.user")

    def test_get_regular(self):
        self.client = self.reauthenticate_user(self.user)

        response = self.client.get(reverse("account:change-password", args=(self.user.id,)))

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTrue(response.template_name[0], UserChangePasswordView.template_name)

        self.assertIn("Change your password", str(response.content))

    def test_post_regular(self):
        new_password = "my_new_password"

        self.client = self.reauthenticate_user(self.user)

        # Change password
        response = self.client.post(
            reverse("account:change-password", args=(self.user.id,)),
            data={
                "old_password": default_password,
                "new_password": new_password,
                "new_password_confirmation": new_password,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        # Assert, that we've been redirected to the detail view
        self.assertTrue(response.template_name[0], UserDetailView.template_name)
        self.assertIn("Your data:", str(response.content))

        # Assert, that the password-change worked
        self.assertEqual(self.user, authenticate(username=self.user.username, password=new_password))