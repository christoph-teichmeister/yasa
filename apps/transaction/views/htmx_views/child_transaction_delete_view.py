from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from apps.core import htmx
from apps.transaction.models import ChildTransaction


class ChildTransactionDeleteHTMXView(htmx.FormHtmxResponseMixin, generic.DeleteView):
    model = ChildTransaction
    template_name = "transaction/_edit.html"

    toast_success_message = "Transaction successfully deleted!"
    toast_error_message = "There was an error deleting the transaction"

    def get_hx_trigger(self):
        if self.parent_transactions_has_no_child_transactions_anymore:
            return None
        return "reloadTransactionEditView"

    def form_valid(self, form):
        form_valid_return = super().form_valid(form)

        if self.parent_transactions_has_no_child_transactions_anymore:
            self.object.parent_transaction.delete()
            form_valid_return["HX-Redirect"] = reverse(
                viewname="room-detail", kwargs={"room_slug": self.object.parent_transaction.room.slug}
            )

        return form_valid_return

    @cached_property
    def parent_transactions_has_no_child_transactions_anymore(self):
        return self.object.parent_transaction.child_transactions.count() == 0
