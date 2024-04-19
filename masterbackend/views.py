from django.shortcuts import render
from .forms import UserInputForm
import os
import csv

def get_user_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Process the input here
            user_id_1 = form.cleaned_data['user_id_1']
            user_id_2 = form.cleaned_data['user_id_2']
            user_id_3 = form.cleaned_data['user_id_3']
            empatica_used = form.cleaned_data['have_empatica']
            _write_settings_to_csv(user_id_1, user_id_2, user_id_3, empatica_used)
            return render(request, 'input_success.html', {'id_1': user_id_1, 'id_2': user_id_2, 
                                                          'id_3': user_id_3 if user_id_3 else 'Not in use', 
                                                          'empatica_used': 'Yes' if empatica_used else 
                                                          'No'})
    else:
        form = UserInputForm()
    
    return render(request, 'user_input_form.html', {'form': form})

def _write_settings_to_csv(id1, id2, id3, empatica_used):
        filepath = 'data/user_settings.csv'
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0

        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header only if the file did not exist or was empty
            if not file_exists:
                header = ["user_id_1", "user_id_2", "user_id_3", "empatica-used"]
                writer.writerow(header)

            # Write the user settings as a new row
            writer.writerow([id1, id2, id3, empatica_used])
