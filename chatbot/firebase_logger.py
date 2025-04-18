import firebase_admin
from firebase_admin import credentials, firestore
import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def log_to_firebase(user_msg, bot_msg):
    data = {
        'user_input': user_msg,
        'bot_response': bot_msg,
        'timestamp': datetime.datetime.now().isoformat()
    }
    db.collection('chat_logs').add(data)
