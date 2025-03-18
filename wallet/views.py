from rest_framework_json_api.views import ModelViewSet
from rest_framework_json_api.renderers import JSONRenderer
from rest_framework_json_api.parsers import JSONParser
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from django.db.models import Sum
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404


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


class WalletTransactionsAPIView(APIView):
    def get(self, request, pk, format=None):
        wallet = get_object_or_404(Wallet, pk=pk)
        transactions = wallet.transactions.all().order_by('id')
        serializer = TransactionSerializer(transactions, many=True, context={'request': request})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


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
