from django.shortcuts import render
from .forms import UserInputForm
import os
import csv

def get_user_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Process the input here
            user_id_left = form.cleaned_data['user_id_left']
            user_id_right = form.cleaned_data['user_id_right']
            empatica_used = form.cleaned_data['have_empatica']
            _write_settings_to_csv(user_id_left, user_id_right, empatica_used)
            return render(request, 'input_success.html', {'id_user_left': user_id_left, 'id_user_right': user_id_right, 'empatica_used': 'Ja' if empatica_used else 
                                                          'Nei'})
    else:
        form = UserInputForm()
    
    return render(request, 'user_input_form.html', {'form': form})

def _write_settings_to_csv(id_left, id_right, empatica_used):
        filepath = 'data/user_settings.csv'
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0

        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header only if the file did not exist or was empty
            if not file_exists:
                header = ["id_left", "id_right", "empatica-used"]
                writer.writerow(header)

            # Write the user settings as a new row
            writer.writerow([id_left, id_right, empatica_used])
