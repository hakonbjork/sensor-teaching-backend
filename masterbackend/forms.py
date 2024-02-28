from django import forms

class UserInputForm(forms.Form):
    user_id_1 = forms.CharField(label='Skriv inn ID til person 1', max_length=100)
    user_id_2 = forms.CharField(label='Skriv inn ID til person 2', max_length=100)
    user_id_3 = forms.CharField(label='Skriv inn ID til person 3 (hvis 3 personer)', required=False, max_length=100)
    have_empatica = forms.BooleanField(label='Brukes Empatica?', required=False)