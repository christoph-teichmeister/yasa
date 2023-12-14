from django.utils.functional import cached_property
from django_context_decorator import context

from apps.room.models import Room


class RoomSpecificMixin:
    _room = None

    def dispatch(self, request, *args, **kwargs):
        # Set room here, so that only one query is made and room is accessible throughout the other methods
        self._room = Room.objects.get(slug=self.kwargs.get("room_slug"))
        # TODO CT: This is obsolete because of the RoomToRequestMiddleware. Continue working on this
        return super().dispatch(request, *args, **kwargs)

    @context
    @cached_property
    def room(self):
        return self._room

    @context
    @cached_property
    def room_users(self):
        # TODO CT: Look for this and replace
        return self._room.room_users
