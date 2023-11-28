from django.http import HttpResponse
from rest_framework import generics
from .models import Stocks, Transactions,Balance
from .serializer.serializer import StocksSerializer,BalanceSerializer,TransactionsSerializer,OrderSerializer,WalletSerializer
from .models import Transactions,Balance,Stocks,Orders,Wallet
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
import requests
from django.conf import settings
import webbrowser
import jwt
from django.contrib.auth import authenticate, login
from django.shortcuts import render

@csrf_exempt 
def process_order(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        username = data['username']
        password = data['password']
        # user2 = User.objects.get(email=user)

        
        user = authenticate(username=username, password=password)
        # print(user)
        # user = authenticate(username="admin", password="P@ssw0rd")
        if user is not None:

            user2 = User.objects.get(username=username)

            # print(user2.id,'ohoy')
            order=Orders.objects.filter(user_id_id=user2.id)
            # user22 = Orders.objects.get(user_id_id=user2.id)
            # print(order,'status')

            for i, val in enumerate(order):
                # print(val.action)
            
                if val.action == 'buy':
            
            
                    order_status = val.status
                    if order_status != 'Complete':
                        
                    
                        quantity = val.quantity
                        stock_id = val.stocks_id_id
                        data  = Stocks.objects.get(id=stock_id)
                        total_price = data.price*quantity
                        data  = Wallet.objects.get(user_id=user2.id)
                        data_conv = float(data.wallet_bal)
                        print(data.id,'update id')
                        print(data_conv-total_price,'magkano')
                        total_wallet = data_conv-total_price

                        
                        Wallet.objects.filter(id=data.id).update(wallet_bal=total_wallet)
                        Orders.objects.filter(user_id_id=user2.id).update(status='Complete')
                        
                        allbalance = Balance.objects.all()
                        
                        Balance.objects.create(
                            balance=total_price,
                            username=user2.id,
                            stock=stock_id,  
                        )
                        # Balance.save()      

                        Transactions.objects.create(
                            price=total_price,
                            status="Successful",
                            action="Buy Stocks",
                            stocks_id=stock_id,
            
                        )

                elif val.action == 'sell':
                    order_status = val.status
                    if order_status != 'Complete':
                        
                        # print(val.quantity)
                        data  = Stocks.objects.get(id=val.stocks_id_id)
                        total_price = data.price*val.quantity

                        
                        # print(total_price,'sell')
                        balance=Balance.objects.filter(username=user2.id)
                        data2  = Wallet.objects.get(user_id=user2.id)
                        data_conv = float(data2.wallet_bal)
                        # print(data_conv)
                        for i, val_balance in enumerate(balance):
                            # print(val_balance.stock)
                            stock_id_order = str(val.stocks_id_id)
                            existing_stock_id = str(val_balance.stock)
                            # print(val.stocks_id_id)
                            if existing_stock_id == stock_id_order:
                                # print('kalabaw')
                                sell_value = val_balance.balance - total_price 
                                total_wallet_value =  data_conv + total_price 
                                # total_wallet_value =  data_conv 
                                print(sell_value,'after stock')
                                print(total_wallet_value,'after wallet')

                                Wallet.objects.filter(user_id=user2.id).update(wallet_bal=total_wallet_value)
                                Orders.objects.filter(user_id_id=user2.id).update(status='Complete')
                                Balance.objects.filter(stock=existing_stock_id).update(balance=sell_value)
                                Transactions.objects.create(
                                    price=total_price,
                                    status="Successful",
                                    action="Sell Stocks",
                                    stocks_id=existing_stock_id,
                    
                                )

    return HttpResponse('zup', status=200)
@csrf_exempt 
def get_portfolio(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        username = data['username']
        password = data['password']
        # user2 = User.objects.get(email=user)

        
        user = authenticate(username=username, password=password)
        # user = authenticate(username="admin", password="P@ssw0rd")
        if user is not None:
            user2 = User.objects.get(username=username)
            balance=Balance.objects.filter(username=user2.id)
            data2  = Wallet.objects.get(user_id=user2.id)
            data_conv = float(data2.wallet_bal)
            stocks_and_balance = []
            for i, val_balance in enumerate(balance):
                # print(val_balance.username)
                conv_user_id = str(user2.id)
                conv_balance_user_id = str(val_balance.username)
                # print(conv_balance_user_id)
                # print(conv_user_id)
                data  = Stocks.objects.get(id=val_balance.stock)
                if conv_user_id == conv_balance_user_id:
                    # print("pasok ba")
                    raw =   {
                                "stock":data.name,
                                "balance" : val_balance.balance ,
                                # "Wallet Balance":   data_conv  
                            }
                    stocks_and_balance.append(raw)
            # print(stocks_and_balance)
            stocks_and_balance.append({"Wallet Balance":data_conv})
            result = json.dumps(stocks_and_balance)
          
            
        
    
    return HttpResponse(result, status=200)


def account(request):
    # url="http://localhost:8000/auth/sign_in/"
    # webbrowser.open(url)
    data = Balance.objects.all()
    context = {"balance":data}
    print(context,'hy')
    
    return render(request,'user/account.html',context)

def user_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'user/account.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'user/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'user/login.html')




class StockList(generics.ListCreateAPIView):
    serializer_class = StocksSerializer

    def get_queryset(self):
        queryset = Stocks.objects.all()
        
        return queryset
    
class StockDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StocksSerializer
    queryset = Stocks.objects.all()


class BalanceList(generics.ListCreateAPIView):
    serializer_class = BalanceSerializer

    def get_queryset(self):
        queryset = Balance.objects.all()
        
        return queryset
    
class BalanceDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BalanceSerializer
    queryset = Balance.objects.all()

class TrasactionList(generics.ListCreateAPIView):
    serializer_class = TransactionsSerializer

    def get_queryset(self):
        queryset = Transactions.objects.all()
        
        return queryset
    
class TransactionDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionsSerializer
    queryset = Transactions.objects.all()

class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Orders.objects.all()
        
        return queryset
    
class OrdernDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()


class WalletList(generics.ListCreateAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        queryset = Wallet.objects.all()
        
        return queryset
    
class WalletDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()