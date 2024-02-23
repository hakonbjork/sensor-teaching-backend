from django import forms

class UserInputForm(forms.Form):
    user_id = forms.CharField(label='Skriv inn ID', max_length=100)
    have_empatica = forms.BooleanField(label='Brukes Empatica?', required=False)