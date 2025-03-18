from django.core.exceptions import ValidationError
from decimal import Decimal
from wallet.models import Wallet, Transaction
from django.test import TestCase


class WalletModelTests(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet")

    def test_initial_balance(self):
        self.assertEqual(self.wallet.balance, Decimal('0.00'))

    def test_update_balance_with_valid_transaction(self):
        Transaction.objects.create(wallet=self.wallet, txid="tx1", amount=Decimal('100.00'))
        self.wallet.update_balance()
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal('100.00'))

    def test_transaction_that_leads_to_negative_balance(self):
        Transaction.objects.create(wallet=self.wallet, txid="tx1", amount=Decimal('50.00'))
        tx = Transaction(wallet=self.wallet, txid="tx2", amount=Decimal('-100.00'))
        with self.assertRaisesMessage(ValidationError,
                                      "Невозможно сохранить транзакцию: баланс кошелька не может стать отрицательным."):
            tx.full_clean()