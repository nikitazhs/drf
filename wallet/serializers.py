from rest_framework_json_api import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Wallet, Transaction, WalletError


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        source="calculated_balance", max_digits=18, decimal_places=2, read_only=True
    )

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance"]
        resource_name = "Wallet"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get("balance") is None:
            representation["balance"] = str(instance.balance)
        representation["type"] = "Wallet"
        return representation


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.ResourceRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = ["id", "txid", "amount", "wallet"]
        resource_name = "transactions"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["type"] = "transactions"
        return representation

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except (DjangoValidationError, WalletError) as e:
            raise serializers.ValidationError(self.format_errors(e))

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except (DjangoValidationError, WalletError) as e:
            raise serializers.ValidationError(self.format_errors(e))

    def format_errors(self, e):
        if hasattr(e, "message_dict"):
            return {
                "errors": [
                    {"detail": v, "source": {"pointer": f"/data/attributes/{k}"}}
                    for k, v in e.message_dict.items()
                ]
            }
        return {"errors": [{"detail": str(e)}]}
