from guest.models import Establishment, Address, Menu, Plate
from django.core.files import File
from faker import Faker
import random
import re
import os

fake = Faker()

def create_establishments_with_address():
    for i in range(0, 9):
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
        address_id = address
        
        file_path = f'guest/static/guest/images/establishment_{i+1}.jpg'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file = File(f)
                image = file

                establishment = Establishment.objects.create(
                    name=name, cnpj=cnpj, rate=rate, categories=categories,
                    delivery=delivery, opens_at=opens_at, closes_at=closes_at, image=image, 
                    address_id=address_id
                )

                establishment.image.name = f'establishment_{i+1}.jpg' 
                establishment.save()
                file.close()

def create_menu_with_plates():
    establishments = Establishment.objects.all()

    for establishment in establishments:
        establishment_id = establishment

        menu = Menu.objects.create(establishment_id=establishment_id)

        price = fake.pydecimal(left_digits=2, right_digits=2, positive=True) 

        for i in range(0, 9):
            name = fake.name()
            price = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
            description = fake.paragraph()
            category = 'plate'
            menu_id = menu

            file_path = f'guest/static/guest/images/plate_{i+1}.jpg'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file = File(f)
                    image = file

                    plate = Plate.objects.create(
                        name=name,
                        price=price,
                        description=description,
                        image=image,
                        category=category,
                        menu_id=menu_id
                    )

                    plate.image.name = f'plate_{i+1}.jpg' 

                    plate.save()
                    file.close()
        
        for i in range(0, 5):
            name = fake.name()
            price = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
            description = fake.paragraph()
            category = 'drink'
            menu_id = menu

            file_path = f'guest/static/guest/images/drink_{i+1}.jpg'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file = File(f)
                    image = file

                    plate = Plate.objects.create(
                        name=name,
                        price=price,
                        description=description,
                        image=image,
                        category=category,
                        menu_id=menu_id
                    )

                    plate.image.name = f'drink_{i+1}.jpg' 
                    plate.save()
                    file.close()