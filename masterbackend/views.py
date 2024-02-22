from django.shortcuts import render
from .forms import UserInputForm

def get_user_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Process the input here
            user_input = form.cleaned_data['user_input']
            # Do something with the input, then redirect or show a success message
            return render(request, 'input_success.html', {'user_input': user_input})
    else:
        form = UserInputForm()
    
    return render(request, 'user_input_form.html', {'form': form})
