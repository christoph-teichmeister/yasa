from django import forms
from django.utils import timezone

from apps.debt.models import Debt


class DebtSettleForm(forms.ModelForm):
    # TODO CT: Completely rework this to a Charfield with the debt ids in a comma separated list
    debt_ids = forms.MultipleChoiceField(
        choices=tuple((i,i) for i in range(0, 10000))
    )

    class Meta:
        model = Debt
        fields = (
            "debt_ids",
            "settled",
        )

    def mark_debt_as_settled(self):
        debt_to_be_updated_tuple = ()

        debts_qs = self._meta.model.objects.filter(
            id__in=self.cleaned_data.get("debt_ids")
        ).only("settled", "settled_at")

        for debt in debts_qs:
            if debt.settled:
                continue

            debt.settled = True
            debt.settled_at = timezone.now().date()
            debt_to_be_updated_tuple += (debt,)

        self._meta.model.objects.bulk_update(
            objs=debt_to_be_updated_tuple, fields=("settled", "settled_at")
        )
