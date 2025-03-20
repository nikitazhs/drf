from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError


class WalletError(Exception):
    pass


class Wallet(models.Model):
    label = models.CharField(max_length=255, db_index=True)
    balance = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )

    def update_balance(self):
        total = self.transactions.aggregate(total=Sum("amount"))["total"] or Decimal(
            "0.00"
        )
        if total < Decimal("0.00"):
            raise WalletError("Баланс кошелька не может быть отрицательным.")
        Wallet.objects.filter(pk=self.pk).update(balance=total)

    def __str__(self):
        return f"{self.label} (Баланс: {self.balance})"


class Transaction(models.Model):
    wallet = models.ForeignKey(
        "Wallet", on_delete=models.CASCADE, related_name="transactions", db_index=True
    )
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, db_index=True)

    def clean(self):
        current_total = self.wallet.transactions.aggregate(total=Sum("amount"))[
            "total"
        ] or Decimal("0.00")
        new_balance = current_total + self.amount
        if new_balance < Decimal("0.00"):
            raise ValidationError(
                "Невозможно сохранить транзакцию: баланс кошелька не может стать отрицательным."
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.wallet.update_balance()

    def __str__(self):
        return f"Transaction {self.txid}: {self.amount}"
