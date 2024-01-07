from debtPaymentSystem.models import Person, Debt, DebtCategory, PaymentHistory
from datetime import datetime, timedelta
from django.shortcuts import render
from faker import Faker
import random

fake = Faker('tr_TR')


def fake_identification_number():
    identity_number = str(random.randint(1, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    even_sum = sum([int(digit) for index, digit in enumerate(identity_number) if index % 2 == 0])
    odd_sum = sum([int(digit) for index, digit in enumerate(identity_number) if index % 2 != 0])
    tenth_digit = (even_sum * 7 - odd_sum) % 10
    eleventh_digi = (sum([int(digit) for digit in identity_number]) + tenth_digit) % 10
    identity_number += str(tenth_digit) + str(eleventh_digi)
    return identity_number


def add_user(times):
    for i in range(times):
        person = Person(
            identification_number=fake_identification_number(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=100),
            phone_number="05" + ''.join([str(random.randint(0, 9)) for _ in range(9)]),
            e_mail=fake.email(),
            address=fake.address(),
            account_number=''.join([str(random.randint(0, 9)) for _ in range(16)])
        )
        person.save()


def add_debt_category(times):
    debt_category_list = ['Ev', 'Araba', 'Arsa', 'Vergi']
    for i in range(times):
        debt_category = DebtCategory(
            name=random.choice(debt_category_list),
            discount_rate=str(10),
            penalty_rate=str(10),
            valid_date=fake.random_int(min=1, max=3),
            invalid_date=fake.random_int(min=1, max=3)
        )
        debt_category_list.remove(debt_category.name)
        debt_category.save()


def add_debt(times):
    for i in range(times):
        create_date = fake.date_between(start_date='-10y', end_date='now')
        installment = fake.random_int(min=3, max=48)
        amount = fake.random_int(min=100, max=10000)
        remaining_installment = fake.random_int(min=3, max=installment)
        debt = Debt(
            person_id=fake.random_int(min=1, max=100),
            debt_category_id=fake.random_int(min=1, max=4),
            amount=amount,
            installment=installment,
            installment_amount=amount / installment,
            remaining_installment=remaining_installment,
            create_date=create_date,
            due_date=fake.date_between(start_date=create_date + timedelta(weeks=2),
                                       end_date=create_date + timedelta(weeks=2)),
            status=True if remaining_installment == installment else False
        )
        debt.save()


def add_payment_history(times):
    for i in range(times):
        id = fake.random_int(min=1, max=800)
        debts = Debt.objects.filter(pk=str(id)).all()
        for debt in debts:
            for i in range(int(debt.remaining_installment)):
                payment_history = PaymentHistory(
                    debt_id=debt.pk,
                    rd_installment=i + 1,
                    pay_amount=debt.installment_amount,
                    pay_date=fake.date_between(start_date=debt.create_date,
                                               end_date=debt.create_date + timedelta(weeks=52)),
                    ip=fake.ipv4(),
                )
                payment_history.save()


# run one by one in sequence
def fill_database(request):
    # add_user(100)
    # add_debt_category(4)
    # add_debt(800)
    # add_payment_history(450)
    return render(request, 'debtPaymentSystem/faker_data.html')
