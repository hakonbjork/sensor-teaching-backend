from django import forms

class UserInputForm(forms.Form):
    user_id_1 = forms.CharField(label='ID of the leftmost person', max_length=100)
    user_id_2 = forms.CharField(label='ID of the rightmost person', max_length=100)
    user_id_3 = forms.CharField(label='ID of person 3 - probably leave this empty', required=False, max_length=100)
    have_empatica = forms.BooleanField(label='Is empatica in use?', required=False)