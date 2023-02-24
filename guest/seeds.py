from guest.models import Establishment, Address, Menu, Plate
from faker import Faker
import random
import re

fake = Faker()

def create_establishments_with_address():
    for i in range(0, 50):
        street = fake.street_name()
        district = fake.street_name()
        number = random.randint(50, 5000)

        address = Address.objects.create(
            street=street,
            district=district,
            number=number
        )

        address.save()

        name = fake.company()
        cnpj_pattern = re.compile(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}')
        cnpj = fake.numerify(text="##############")
        rate = fake.random_element(elements=range(1, 5)) 
        categories = fake.random_element(elements=['mexican', 'healthy', 'brazilian', 'japanese', 'italian'])
        delivery = fake.random_element(elements=[True, False])
        opens_at = fake.date_time()
        closes_at = fake.date_time()
        image = fake.random_element(elements=['http://127.0.0.1:8000/static/client/images/logo-habibs.png', 'http://127.0.0.1:8000/static/client/images/logo-habibs.png'])
        address_id = address

        establishment = Establishment.objects.create(name=name, cnpj=cnpj, rate=rate, categories=categories, delivery=delivery, opens_at=opens_at, closes_at=closes_at, image=image, address_id=address_id)
        establishment.save()

def create_menu_with_plates():
    establishments = Establishment.objects.all()

    for establishment in establishments:
        establishment_id = establishment

        menu = Menu.objects.create(establishment_id=establishment_id)

        price = fake.pydecimal(left_digits=2, right_digits=2, positive=True) 

        for i in range(0, 30):
            name = fake.name()
            price = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
            description = fake.paragraph()
            image = fake.random_element(elements=[
                'http://127.0.0.1:8000/static/guest/images/esfirra.png', 
                'http://127.0.0.1:8000/static/guest/images/esfirra.png'
            ])
            category = fake.random_element(elements=[
                'plate', 'drink'
            ])
            menu_id = menu

            plate = Plate.objects.create(
                name=name,
                price=price,
                description=description,
                image=image,
                category=category,
                menu_id=menu_id
            )

            plate.save()