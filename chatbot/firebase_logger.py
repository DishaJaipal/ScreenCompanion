import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")  # New (correct path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def log_to_firebase(user_input, response):
    db.collection("chatlogs").add({
        "user_input": user_input,
        "response": response
    })
