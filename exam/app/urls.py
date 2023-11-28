
from .views import TrasactionList,TransactionDetails,BalanceList,BalanceDetails,StockList,StockDetails,OrderList,OrdernDetails,WalletDetails,WalletList
from django.urls import path,include
from django.conf import settings
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tokenverify/', TokenVerifyView.as_view(), name='token_refresh'),

    path('get_portfolio', views.get_portfolio, name='get_portfolio'),
    path('process_order', views.process_order, name='process_order'),
    path('login', views.user_login, name='user_login'),

    path('transactions/', TrasactionList.as_view()),
    path('transactions/<str:pk>', TransactionDetails.as_view()),

    path('balance/', BalanceList.as_view()),
    path('balance/<str:pk>', BalanceDetails.as_view()),

    path('stock/', StockList.as_view()),
    path('stock/<str:pk>', StockDetails.as_view()),

    path('order/', OrderList.as_view()),
    path('order/<str:pk>', OrdernDetails.as_view()),

    path('wallet/', WalletList.as_view()),
    path('wallet/<str:pk>', WalletDetails.as_view()),
]
