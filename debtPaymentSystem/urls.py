from . import views
from django.urls import path
import debtPaymentSystem.managment.fillDatabase
import debtPaymentSystem.report

app_name = 'debtPaymentSystem'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('debts/', views.debts, name='debts'),
    path('payment/<int:debt_id>', views.payment, name='payment'),
    path('result/<int:debt_id>', views.result, name='result'),
    path('history/', views.history, name='history'),
    path('bill/<int:bill_id>', views.bill, name='bill'),
    path('filldatabase/', debtPaymentSystem.managment.fillDatabase.fill_database, name='filldatabase'),
]
