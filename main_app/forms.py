from django.forms import ModelForm
from django.forms import TextInput
from main_app.models import Apparel

class ApparelForm(ModelForm):
    class Meta:
        model = Apparel
        fields = ['name', 'brand', 'color', 'size', 'img', 'style', 'type']
        widgets = {
            'name': TextInput(attrs={
            'placeholder': 'Name this item',
            'class': "form-control",
            'style': 'max-width: 450px; border-radius: 20px;',
            }),
            'brand': TextInput(attrs={
            'placeholder': 'What brand made this item?',
            'class': "form-control",
            'style': 'max-width: 450px; border-radius: 20px;',
            }),
            'color': TextInput(attrs={
            'placeholder': 'What color is this item?',
            'class': "form-control",
            'style': 'max-width: 450px; border-radius: 20px;',
            }),
            'size': TextInput(attrs={
            'placeholder': 'What size is this item?',
            'class': "form-control",
            'style': 'max-width: 450px; border-radius: 20px;',
            }),
            'style': TextInput(attrs={
            'placeholder': 'Does this item have any special attributes? (Ex: Sleeve-length: Short, Heel-height: 3in)',
            'class': "form-control",
            'style': 'max-width: 450px; border-radius: 20px;',
            })
        }
        
        