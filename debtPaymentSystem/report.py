from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import *
import datetime
import os


def create_bill_pdf(bill_id):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    payment_history = PaymentHistory.objects.get(pk=bill_id)
    debt = Debt.objects.get(pk=payment_history.debt_id)
    person = Person.objects.get(pk=debt.person_id)
    debt_category = DebtCategory.objects.get(pk=debt.debt_category_id)
    account_number = person.account_number
    identity_number = person.identification_number
    name = person.first_name + " " + person.last_name
    phone = person.phone_number
    email = person.e_mail
    address = person.address
    debt_category = debt_category.name
    pay_date = payment_history.pay_date.strftime("%d/%m/%Y")
    pay_amount = str(payment_history.pay_amount)
    total_amount = str(debt.amount)

    c.setFont("Helvetica", 15)
    text = "INVOICE"
    c.drawString(font_width(text, "Helvetica", 15), 750, text)

    c.setFont("Helvetica-Bold", 8)
    c.drawString(35, 715, "IDENTITY NUMBER")
    c.drawString(35, 685, "ACCOUNT NUMBER")
    c.drawString(35, 655, "PHONE")
    c.drawString(35, 625, "E-MAIL")
    c.drawString(130, 715, ":")
    c.drawString(130, 685, ":")
    c.drawString(130, 655, ":")
    c.drawString(130, 625, ":")
    c.setFont("Helvetica", 8)
    c.drawString(140, 715, identity_number)
    c.drawString(140, 685, account_number)
    c.drawString(140, 655, phone)
    c.drawString(140, 625, email)

    c.setFont("Helvetica-Bold", 8)
    c.drawString(321, 715, "DEAR")
    c.drawString(321, 685, "NAME")
    c.drawString(321, 655, "ADDRESS")
    c.drawString(365, 685, ":")
    c.drawString(365, 655, ":")
    c.setFont("Helvetica", 8)
    c.drawString(370, 685, name)
    c.drawString(370, 655, address)

    c.setFont("Helvetica-Bold", 8)
    c.drawString(40, 580, "EXPLANATION")
    c.drawString(40, 568, "DEBT CATEGORY")
    c.drawString(40, 556, "PAY DATE")
    c.drawString(40, 544, "PAY AMOUNT")
    c.drawString(40, 532, "TOTAL AMOUNT")
    c.drawString(130, 568, ":")
    c.drawString(130, 556, ":")
    c.drawString(130, 544, ":")
    c.drawString(130, 532, ":")
    c.setFont("Helvetica", 8)
    c.drawString(140, 568, debt_category)
    c.drawString(140, 556, pay_date)
    c.drawString(140, 544, pay_amount + " TL")
    c.drawString(140, 532, total_amount + " TL")

    c.drawString(40, 490, pay_amount + " TL has been withdrawn from your account")
    c.drawString(40, 480, datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))

    path = os.path.dirname(os.path.abspath(__file__)) + "\\static\\debtPaymentSystem\\images\\"
    c.drawImage(path + "sancaktepeBelediyesiLogo.png", 20, 745, 90, 45)
    c.drawImage(path + "IyzicoLogo.png", 30, 30, 72, 30)
    c.drawImage(path + "mastercardLogo.png", 510, 60, 31, 24)
    c.drawImage(path + "maestroLogo.png", 550, 60, 31, 24)
    c.drawImage(path + "troyLogo.png", 470, 30, 31, 24)
    c.drawImage(path + "visaLogo.png", 510, 30, 31, 24)
    c.drawImage(path + "visaElectronLogo.png", 550, 30, 31, 24)

    # Frame color and width
    border_color = (0, 0, 0)
    border_width = 1

    # Paint frame
    c.setStrokeColor(border_color)
    c.setLineWidth(border_width)
    c.rect(frame_width(572), 462, 572, 280)
    c.rect(frame_width(572) + 5, 609, 276, 128)
    c.rect(frame_width(572) + 291, 609, 276, 128)

    c.save()

    buffer.seek(0)
    pdf = buffer.getvalue()

    return BytesIO(pdf)


def font_width(text, font_name, font_size):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    return ((letter[0] - c.stringWidth(text, font_name, font_size)) / 2)


def frame_width(frm_wdth):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    return ((letter[0] - frm_wdth) / 2)
