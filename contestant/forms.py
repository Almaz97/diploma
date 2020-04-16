from django import forms

from contestant.models import Contestant


class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['full_name', 'email', 'address', 'phone_number', 'documents']
        labels = {
            'full_name': 'ФИО',
            'address': 'Адрес',
            'phone_number': 'Номер телефона',
            'documents': 'Докуметы',
        }