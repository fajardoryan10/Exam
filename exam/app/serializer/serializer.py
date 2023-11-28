from rest_framework import serializers
# from ..models import Company,Groups,Departments,Divisions,,Sections
from ..models import Transactions,Balance,Stocks,Orders,Wallet


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('__all__')

class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ('__all__')

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('__all__')

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('__all__')