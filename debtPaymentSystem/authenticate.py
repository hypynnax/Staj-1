from .models import Person


def verify(request, tc_number=None, birth_date=None):
    persons = Person.objects.all()

    for person in persons:
        if person.identification_number == tc_number and person.date_of_birth == birth_date:
            return person
    else:
        return None
