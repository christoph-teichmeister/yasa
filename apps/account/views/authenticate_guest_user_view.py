from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from apps.account.models import User


class AuthenticateGuestUserView(generic.View):
    http_method_names = [
        "post",
        "options",
    ]

    def post(self, request, *args, **kwargs):
        room_slug = self.request.POST.get("room_slug")

        redirect_response = HttpResponseRedirect(
            redirect_to=reverse(viewname="room-detail", kwargs={"slug": room_slug})
        )

        if request.user.is_authenticated:
            return redirect_response

        user_id = self.request.POST.get("user_id")
        guest_user = User.objects.get(id=user_id)
        login(request=request, user=guest_user)

        return redirect_response