import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def init_firebase():

    # Fetch the service account key JSON file contents
    # for sikkerhetshensyn er ikke denne filen per nå del av repoet
    # kan ta den med og gitignore den
    cred = credentials.Certificate('../sensor-teaching-firebase.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sensor-teaching-default-rtdb.europe-west1.firebasedatabase.app/'
    })

def add_measurement_data(user_id, measurement, value):

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('sensor-data')

    user_exists = ref.child(f"{user_id}").get()
    
    if (not user_exists):
        ref.child(f"{user_id}").set({})

    measurement_exists = ref.child(f"{user_id}/{measurement}").get()

    if (not measurement_exists):
        ref.child(f"{user_id}/{measurement}").set({})
    
    
    new_data_ref = ref.child(f"{user_id}/{measurement}").push()
    new_data_ref.set({
        "time": time.time(),
        "value": value
    })

def update_signalling_data(user_id, measurement, value):

    ref = db.reference('signalling-data')
    user_exists = ref.child(f"{user_id}").get()
    
    if (not user_exists):
        ref.child(f"{user_id}").set({measurement: value})

    else:
        ref.child(f"{user_id}").update({measurement: value})

def get_user_data(user_id):
    ref = db.reference('sensor-data')
    user_data = ref.child(f"{user_id}").get()
    return user_data
