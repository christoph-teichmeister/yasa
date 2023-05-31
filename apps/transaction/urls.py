from django.urls import path

# from django.views.decorators.cache import cache_page

from apps.transaction import views

urlpatterns = [
    path("add/", views.TransactionCreateView.as_view(), name="transaction-add"),
    path(
        "htmx/<str:slug>/list",
        # Cached for 10 minutes
        # cache_page(60 * 10)(views.TransactionListHTMXView.as_view()),
        views.TransactionListHTMXView.as_view(),
        name="htmx-transaction-list",
    ),
    path(
        "htmx/<str:slug>/add-payment-modal",
        # Cached for 10 minutes
        # cache_page(60 * 10)(views.TransactionAddModalHTMXView.as_view()),
        views.TransactionAddModalHTMXView.as_view(),
        name="htmx-transaction-add-modal",
    ),
]
