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

def add_data(user_id, data):

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('sensor-data')

    child_exists = ref.child(f"{user_id}").get()
    
    if (not child_exists):
        ref.child(f"{user_id}").set(data)
    
    else:
        ref.child(f"{user_id}").update(data)


    
