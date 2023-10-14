from ambient_toolbox.view_layer import htmx_mixins
from django.utils.functional import cached_property
from django.views import generic
from django_context_decorator import context

from apps.transaction.models import ParentTransaction


class TransactionDetailHTMXView(htmx_mixins.HtmxResponseMixin, generic.DetailView):
    model = ParentTransaction
    context_object_name = "parent_transaction"
    template_name = "transaction/_detail.html"

    @context
    @cached_property
    def child_transactions(self):
        return self.object.child_transactions.all()

    @context
    @cached_property
    def room(self):
        return self.object.room

    def get_object(self, queryset=None):
        return super().get_object(queryset)