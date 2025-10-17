from django.contrib import admin

from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone','profile')
    search_fields = ('user',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'purchase_no', 'amount', 'price', 'type','total_price', 'pay_status', 'create_date']
    search_fields = ('user', 'name', 'purchase_no')


@admin.register(RecoveryPurchase)
class RecoveryPurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'delete_by', 'user', 'name', 'purchase_no', 'amount', 'price', 'type','total_price', 'pay_status', 'create_date', 'delete_date']
    search_fields = ('user', 'name', 'purchase_no')

@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'sale_no', 'amount', 'price', 'type','total_price', 'pay_status', 'create_date']
    search_fields = ('user', 'name', 'sale_no')

@admin.register(RecoverySaleProduct)
class RecoverySaleProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'delete_by', 'user', 'name', 'sale_no', 'amount', 'price', 'type','total_price', 'pay_status', 'create_date', 'delete_date']
    search_fields = ('user', 'name', 'sale_no')

@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'is_leave', 'paystatus']
    search_fields = ('user',)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['worklog', 'amount']
    search_fields = ('worklog',)