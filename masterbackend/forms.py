from django import forms

class UserInputForm(forms.Form):
    user_id_left = forms.CharField(label='Skriv inn ID til person til venstre', max_length=100)
    user_id_right = forms.CharField(label='Skriv inn ID til person til høyre', max_length=100)
    have_empatica = forms.BooleanField(label='Brukes Empatica?', required=False)