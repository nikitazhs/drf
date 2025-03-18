from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from wallet.models import Wallet, Transaction

class WalletTransactionsEndpointTests(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet")
        Transaction.objects.create(wallet=self.wallet, txid="tx1", amount=Decimal('100.00'))
        Transaction.objects.create(wallet=self.wallet, txid="tx2", amount=Decimal('50.00'))
        self.wallet_detail_url = reverse('wallet-detail', kwargs={'pk': self.wallet.id})

    def test_get_transactions_for_wallet(self):
        url = f"{self.wallet_detail_url}transactions/"
        response = self.client.get(url, HTTP_ACCEPT="application/vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transactions = response.data["data"]
        self.assertIsInstance(transactions, list)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["type"], "transactions")
        self.assertEqual(transactions[1]["type"], "transactions")

