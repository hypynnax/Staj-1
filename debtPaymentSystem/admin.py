from django.contrib import admin
from .models import *


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'identification_number', 'first_name', 'last_name', 'date_of_birth')
    list_filter = ('identification_number', 'date_of_birth')
    search_fields = ('person_id', 'identification_number', 'first_name', 'last_name', 'date_of_birth')


admin.site.register(Person, PersonAdmin)


class DebtCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_rate', 'penalty_rate', 'invalid_date', 'valid_date')
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(DebtCategory, DebtCategoryAdmin)


class DebtAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'debt_category_id', 'amount', 'remaining_installment', 'installment', 'create_date',
                    'due_date', 'status')
    list_filter = ('status', 'debt_category_id', 'due_date', 'create_date')
    search_fields = ('person_id',)


admin.site.register(Debt, DebtAdmin)


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('ip', 'rd_installment', 'pay_amount', 'pay_date', 'debt_id')
    list_filter = ('pay_date',)
    search_fields = ('ip', 'debt_id')


admin.site.register(PaymentHistory, PaymentHistoryAdmin)
