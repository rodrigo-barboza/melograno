from django import forms

<<<<<<< HEAD
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
         model = Product
         fields = ['image', 'name', 'description', 'price', 'category']
=======
CATEGORIES = (
    ('mexican', 'Mexicana'),
    ('healthy', 'Saudável'),
    ('brazilian', 'Brasileira'),
    ('japanese', 'Japonesa'),
    ('italian', 'Italiana'),
)

class RegisterEstablishmentForm(forms.Form):
    file = forms.FileField(required=True)
    name = forms.CharField(required=True, max_length=100)
    opens_at =  forms.TimeField(required=True)
    closes_at = forms.TimeField(required=True)
    category = forms.ChoiceField(required=True, choices=CATEGORIES)

    def clean(self):
        cleaned_data = super(RegisterEstablishmentForm, self).clean()

        return cleaned_data

>>>>>>> 2f0926d06953a36e3354b386ebec0dc8da0c46d4
