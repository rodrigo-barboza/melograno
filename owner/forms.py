from django import forms

CATEGORIES = (
    ('mexican', 'Mexicana'),
    ('healthy', 'Saudável'),
    ('brazilian', 'Brasileira'),
    ('japanese', 'Japonesa'),
    ('italian', 'Italiana'),
)

FOOD_TYPES = (
    ('plate', 'Prato'),
    ('drink', 'Bebida'),
)
class PlateForm(forms.Form):
    name = forms.CharField(required=True, max_length=100)
    price =  forms.FloatField(required=True)
    description = forms.CharField(required=True)
    file = forms.FileField()
    category = forms.ChoiceField(required=True, choices=FOOD_TYPES)

    def clean(self):
        cleaned_data = super(PlateForm, self).clean()

        return cleaned_data

class RegisterEstablishmentForm(forms.Form):
    file = forms.FileField(required=True)
    name = forms.CharField(required=True, max_length=100)
    opens_at =  forms.TimeField(required=True)
    closes_at = forms.TimeField(required=True)
    category = forms.ChoiceField(required=True, choices=CATEGORIES)

    def clean(self):
        cleaned_data = super(RegisterEstablishmentForm, self).clean()

        return cleaned_data

