from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, TransactionViewSet, WalletTransactionsAPIView

router = DefaultRouter()
router.register(r"wallets", WalletViewSet, basename="wallet")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "wallets/<int:pk>/transactions/",
        WalletTransactionsAPIView.as_view(),
        name="wallet-transactions",
    ),
]
