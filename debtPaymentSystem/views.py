from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from .report import create_bill_pdf
from django.http import HttpResponse, FileResponse
import debtPaymentSystem.authenticate
import debtPaymentSystem.templates
import iyzipay
import json

user_name = ""
id = ""


def home(request):
    global user_name
    user_name = Person.objects.get(pk=id).first_name + " " + Person.objects.get(pk=id).last_name
    return render(request, 'debtPaymentSystem/home.html', {'user_name': user_name})


def debts(request):
    global user_name, id
    debt = Debt.objects.filter(person_id=id).all()
    return render(request, 'debtPaymentSystem/debts.html', {'debts': debt, 'user_name': user_name})


iyzipay.api_key = 'sandbox-9Gb75tjDcYn47SWVqnwVE8SsPNnpHnZq'
iyzipay.secret_key = 'CDsKViazBrNRz3guQ5aYtVPAafAOwfL2'

options = {
    'api_key': iyzipay.api_key,
    'secret_key': iyzipay.secret_key,
    'base_url': iyzipay.base_url
}

tokens = list()


def payment(request, debt_id):
    person = Debt.objects.get(pk=debt_id).person
    debt_category = Debt.objects.get(pk=debt_id).debt_category
    debt = Debt.objects.get(pk=debt_id)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    buyer = {
        'id': 'BY789',
        'name': person.first_name,
        'surname': person.last_name,
        'gsmNumber': person.phone_number,
        'email': person.e_mail,
        'identityNumber': person.identification_number,
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': person.address,
        'ip': ip,
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address = {
        'contactName': person.first_name,
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': person.address,
        'zipCode': '34732'
    }

    basket_items = [
        {
            'id': 'BI101',
            'name': debt_category.name,
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': str(debt.installment_amount)
        }
    ]

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'price': str(debt.installment_amount),
        'paidPrice': str(debt.installment_amount),
        'currency': 'TRY',
        'basketId': 'BI101',
        'paymentGroup': debt_category.name,
        "callbackUrl": f"http://localhost:8000/account/result/{debt_id}",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    tokens.append(json_content['token'])
    return HttpResponse(json_content["checkoutFormContent"])


@require_http_methods(['POST'])
@csrf_exempt
def result(request, debt_id):
    claim = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': tokens[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(claim, options)
    result = checkout_form_result.read().decode('utf-8')
    response = json.loads(result, object_pairs_hook=list)
    print(response[0][1])
    if response[0][1] == 'success':
        debt = Debt.objects.get(pk=debt_id)
        debt.remaining_installment = str(int(debt.remaining_installment) + 1)
        debt.save()
        if debt.remaining_installment == debt.installment:
            debt.status = True
            debt.save()
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            payment_history = PaymentHistory(rd_installment=debt.remaining_installment,
                                             pay_amount=debt.installment_amount,
                                             pay_date=datetime.now().date().strftime('%Y-%m-%d'), ip=ip,
                                             debt_id=debt_id)
            payment_history.save()
        return render(request, 'debtPaymentSystem/result.html',
                      {'title': 'BAŞARILI İŞLEM', 'body': 'İşlem Başarılı Ödeme Alındı'})
    elif response[0][1] == 'failure':
        return render(request, 'debtPaymentSystem/result.html',
                      {'title': 'BAŞARISIZ İŞLEM', 'body': 'İşlem Başarısız Ödeme Alınamadı'})


def history(request):
    global user_name, id
    person_debts = Debt.objects.filter(person_id=id).all()
    dataset = []
    for pd in person_debts:
        person_payments_history = PaymentHistory.objects.filter(debt_id=pd.id).all()
        for pph in person_payments_history:
            dataset.append({'debt': pd, 'payment': pph})
    return render(request, 'debtPaymentSystem/payment_history.html',
                  {'dataset': dataset, 'user_name': user_name})


def bill(request, bill_id):
    response = FileResponse(create_bill_pdf(bill_id), filename="FATURA.pdf", content_type='FATURA/pdf')
    response['Content-Disposition'] = 'inline; filename="FATURA.pdf"'
    return response


def login(request):
    global user_name, id
    if request.method == 'POST':
        tc_number = request.POST.get('tc_number')
        birth_date = request.POST.get('birth_date')
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        user = debtPaymentSystem.authenticate.verify(request, tc_number=tc_number, birth_date=birth_date)
        if user is not None:
            id = user.id
            user_name = user.first_name + " " + user.last_name
            return redirect('debtPaymentSystem:debts')
        else:
            messages.error(request, 'Giriş bilgileri geçersiz.')

    return render(request, 'debtPaymentSystem/login.html')
