from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Transactions,Balance,Stocks,Orders,Wallet


admin.site.register(Stocks)
admin.site.register(Balance)
admin.site.register(Transactions)
admin.site.register(Orders)
admin.site.register(Wallet)
