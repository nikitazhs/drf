from rest_framework_json_api.views import ModelViewSet
from rest_framework_json_api.renderers import JSONRenderer
from rest_framework_json_api.parsers import JSONParser
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from django.db.models import Sum
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.annotate(
        calculated_balance=Sum('transactions__amount')
    ).order_by('id')
    serializer_class = WalletSerializer
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    pagination_class = JsonApiPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['label']
    ordering_fields = ['balance', 'label']
    search_fields = ['label']

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        wallet = self.get_object()
        qs = wallet.transactions.all().order_by('id')
        self.pagination_class = None
        serializer = TransactionSerializer(qs, many=True, context={'request': request})
        return Response({"data": serializer.data})


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = JsonApiPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['wallet', 'wallet__label', 'txid']
    ordering_fields = ['amount', 'txid']
    search_fields = ['txid']
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
