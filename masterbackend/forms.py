from django import forms

class UserInputForm(forms.Form):
    user_input = forms.CharField(label='Enter ID', max_length=100)