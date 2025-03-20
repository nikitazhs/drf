import json
import uuid
from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from wallet.models import Wallet, Transaction


class WalletAPITests(APITestCase):
    def setUp(self):
        self.wallet1 = Wallet.objects.create(label="Test Wallet 1")
        self.wallet2 = Wallet.objects.create(label="Test Wallet 2")
        self.wallets_url = reverse("wallet-list")

    def test_get_wallet_list(self):
        response = self.client.get(
            self.wallets_url, HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        raw = json.loads(response.content.decode("utf-8"))
        self.assertIn("data", raw)
        self.assertEqual(len(raw["data"]), 2)

    def test_create_wallet(self):
        data = {"data": {"type": "Wallet", "attributes": {"label": "New Wallet"}}}
        response = self.client.post(
            self.wallets_url,
            data,
            format="vnd.api+json",
            HTTP_ACCEPT="application/vnd.api+json",
        )

        raw_content = response.content.decode("utf-8")
        parsed = json.loads(raw_content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("data", parsed)
        self.assertEqual(parsed["data"]["attributes"]["label"], "New Wallet")

    def test_sort_wallets_by_balance(self):
        Transaction.objects.create(
            wallet=self.wallet1, txid="tx1", amount=Decimal("50.00")
        )
        Transaction.objects.create(
            wallet=self.wallet2, txid="tx2", amount=Decimal("100.00")
        )

        response = self.client.get(
            f"{self.wallets_url}?sort=balance", HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        raw = json.loads(response.content.decode("utf-8"))
        wallets = raw["data"]
        self.assertGreater(
            Decimal(wallets[1]["attributes"]["balance"]),
            Decimal(wallets[0]["attributes"]["balance"]),
        )


class TransactionAPITests(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet")
        self.transactions_url = reverse("transaction-list")

    def test_create_valid_transaction(self):
        unique_txid = "tx_valid_" + str(uuid.uuid4())
        data = {
            "data": {
                "type": "transactions",
                "attributes": {"txid": unique_txid, "amount": "100.00"},
                "relationships": {
                    "wallet": {"data": {"type": "Wallet", "id": str(self.wallet.id)}}
                },
            }
        }
        response = self.client.post(
            self.transactions_url,
            data,
            format="vnd.api+json",
            HTTP_ACCEPT="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("100.00"))

    def test_create_transaction_negative_balance(self):
        Transaction.objects.create(
            wallet=self.wallet, txid="tx_initial", amount=Decimal("50.00")
        )
        unique_txid = "tx_negative_" + str(uuid.uuid4())
        data = {
            "data": {
                "type": "transactions",
                "attributes": {"txid": unique_txid, "amount": "-100.00"},
                "relationships": {
                    "wallet": {"data": {"type": "Wallet", "id": str(self.wallet.id)}}
                },
            }
        }
        response = self.client.post(
            self.transactions_url,
            data,
            format="vnd.api+json",
            HTTP_ACCEPT="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Невозможно сохранить транзакцию", str(response.data))

    def test_get_transactions_for_wallet(self):
        Transaction.objects.create(
            wallet=self.wallet, txid="tx1", amount=Decimal("100.00")
        )
        Transaction.objects.create(
            wallet=self.wallet, txid="tx2", amount=Decimal("50.00")
        )
        url = reverse("wallet-transactions", kwargs={"pk": self.wallet.id})

        response = self.client.get(url, HTTP_ACCEPT="application/vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        raw = json.loads(response.content.decode("utf-8"))
        transactions = raw["data"]["data"]

        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["type"], "transactions")

    def test_search_transaction_by_txid(self):
        Transaction.objects.create(
            wallet=self.wallet, txid="unique_txid", amount=Decimal("100.00")
        )
        response = self.client.get(
            f"{self.transactions_url}?filter[txid]=unique_txid",
            HTTP_ACCEPT="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        raw = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(raw["data"]), 1)
        self.assertEqual(raw["data"][0]["attributes"]["txid"], "unique_txid")

    def test_pagination(self):
        for i in range(15):
            Transaction.objects.create(
                wallet=self.wallet, txid=f"tx{i}", amount=Decimal("10.00")
            )

        response = self.client.get(
            f"{self.transactions_url}?page[size]=10",
            HTTP_ACCEPT="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        raw = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            len(raw["data"]), 10
        )  # Должно быть 10 записей на первой странице
