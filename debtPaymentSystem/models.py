from django.db import models


class Person(models.Model):
    identification_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    account_number = models.CharField(max_length=150)


class DebtCategory(models.Model):
    name = models.CharField(max_length=50)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2)
    invalid_date = models.CharField(max_length=20)
    valid_date = models.CharField(max_length=20)


class Debt(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    debt_category = models.ForeignKey(DebtCategory, on_delete=models.CASCADE)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_installment = models.CharField(max_length=20)
    installment = models.CharField(max_length=20)
    create_date = models.DateField()
    due_date = models.DateField()
    status = models.BooleanField()


class PaymentHistory(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    rd_installment = models.CharField(max_length=20)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField()
    ip = models.GenericIPAddressField()
