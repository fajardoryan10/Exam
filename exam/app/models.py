from django.db import models
from django.conf import settings
from django.contrib.auth.models import User # new


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    wallet_bal = models.FloatField(default=0,null=False,blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True,blank=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False) 

    def __str__(self):
        return str(self.wallet_bal)
    class Meta:
        db_table = "wallet"
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallet'
class Stocks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "stocks"
        verbose_name = 'Stocks'
        verbose_name_plural = 'Stocks'


class Balance(models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    stock = models.CharField(max_length=255)
    # user_id = models.ForeignKey(User,related_name="auth_user", on_delete=models.CASCADE,null=False) 
    # stocks_id = models.ForeignKey(Stocks,related_name="stocks", on_delete=models.CASCADE,null=False)
    class Meta:
        db_table = "balance"
        verbose_name = 'balance'
        verbose_name_plural = 'balance'


class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.FloatField(max_length=50)
    status = models.CharField(max_length=50)
    action = models.CharField(max_length=50)

    stocks_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    # stocks_id = models.ForeignKey(Stocks,related_name="stocks", on_delete=models.CASCADE,null=False)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False) 

    def __str__(self):
        return  self.status
    class Meta:
        db_table = "transactions"
        verbose_name = 'Transactions'
        verbose_name_plural = 'Transactions'


   

        
class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    action = models.CharField(max_length=255,null=False,blank=False)
    status = models.CharField(max_length=255,null=True,blank=True,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    user_id = models.ForeignKey(User,related_name="auth_user", on_delete=models.CASCADE,null=False) 
    stocks_id = models.ForeignKey(Stocks,related_name="stocks", on_delete=models.CASCADE,null=False)
    # wallet_id = models.ForeignKey(Wallet,related_name="wallet", on_delete=models.CASCADE,null=False)
        

    def __str__(self):
        return str(self.quantity) + ' ' + str(self.user_id) + '  '+ str(self.stocks_id)
    class Meta:
        db_table = "orders"
        verbose_name = 'orders'
        verbose_name_plural = 'orders'