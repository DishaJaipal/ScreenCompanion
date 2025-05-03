import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Firebase Configuration
def initialize_firebase():
    # Create the service account file if it doesn't exist
    service_account_info = {
        "type": "service_account",
        "project_id": "chatbot-94efc",
        "private_key_id": "ab103f4c3193b187058a7039fc8acb21d44c92d0",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDEWoLnRlL5e9iL\nMN9Duo11GvDfeWLaURxqpLmtXt52OeK0VojQY8kQUWE632OH6Pn/I5lMApKIHFgq\ngNQKlqRgeCN6uwrpdFSP5+diyQ+4bgq6YxBgvo0kaFFlD3PEyg0k7DwMpH6Illek\nLrn0n8BgqS48wwjbFdwj343Rs5/Ge06mMLe4eZLTHqRMRB8iVTtzb/o45YvJ/DxL\nDUrcQgeaSJqpAgjOGdJRWjV9QqJGzcs7q2T7oGApEhZE6OcOOk/DAiz1HEuL7Z3D\nVcrddjCyn5jpJWu3mO3BozBFXeYEIvcU1nCrnpeokdG2QjoXTAVUb+0eePUQAMmW\nbc83P4/zAgMBAAECggEACk1Pae/8IX/YdDEbvbN3gYno0mjNgXPZAFVlMo30MRLH\nbLvPkNNzdKo4ZjzbPYHBQBwvilfmNUL7cztwJKATvsX+4o0WvPnwB97ceoffDcek\nQ3Q4I0NMJ3lbr+g4JD6PovzMB8PHqcXtkj0rX4TUNJ4bwW9gMxJ6Ct3LVJHOk7zD\n3CfxBk2uGLZOwm5nL+w5+7yId/2CSaqhygBSS/k8+rjgU9+dN8ijMfe26TG6zKRP\nxOcY1hMVMTLRnEdFE2ifITrAjS1oh9Vg7LQSC5BMHbTbJp2seElOF1xFIzW5DUc0\nZn4m0lffv9Dsz9t9+T5dPIBWyZ+tJOab2O2e6xl6XQKBgQD1NM5FfWK6J8T/YYu8\nl88QrA8O5/BTvuzHB/Eb9j4+cO4Mo5e/ZHqqLzcUiQvm5l2cz/gpLObxkCmpeoGF\nYPJ+q0wvpFH0c1LDoW08rJPvanGYUAKm6XRGjGdNRxsP1BST6ta4hJMnmmwSQXWN\ncG7Zf8RrGFxZVG1lkcN60QVEdwKBgQDM/zD/TB+QiMZYSffiA6mTWR2GlQuIlhEG\nW3wN0fwe7p9hjiYeuPXIO4ghcdbp9JZrKCVP5YMsr+mX2nT6zzcskRy2CLABm7hQ\nw53TRYS7KHcyx8FX2V1k3BbPagCORJXpiJXKDvH385e5EdTW4p99cGp9mMh1bAGF\nx26FCWUbZQKBgHDExEh5DbqHJ7Y7akRlnLkSKCq2yHP7TnGKWXx+lsmorhHp+pPu\n5er2o+Ix1ONv9oVzr7FgESXvIvnqeT6aA2v146fVbkt57gpCZzaMN8zXqz5dLZsN\nqof3clq75No2svAEBJP/hJ2mCyWqLSHLH2+vrumB3pbGmTko/DmzfzSpAoGAH+bq\n4iAfnWebrmu8duDpB/RLYwFY7SWlep7MHH58RPgPt6feiNNx9HpHQiUsM/aLXhu+\nSsPF+TNbH/WwVMPgqz/d/vo1IdrxASigLBvafyHaAv4RObGrFiImLpspgPptdg16\nehp/T34KM5Px0ossFOJkwC0BrTxktEQIEA4ZPP0CgYAte/TxGWXwpx0oe4j6Flno\n4xVsiriBQEJegRzrrTxi1ESN67LpPpAtkSHW33OO3QWPeWY46Nm+rustvzQp13X/\ng2PJYKu+2XYpBVpG/rcZNK1ZqlyRn7pj5UuV902dalNvhB+EpdN8e5ZKHsce2Fgt\nlmzbYx+wYy6/O4qYtHc1QA==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-fbsvc@chatbot-94efc.iam.gserviceaccount.com",
        "client_id": "104725058646993852598",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40chatbot-94efc.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    # Create the service account file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cred_path = os.path.join(current_dir, "serviceAccountKey.json")
    
    if not os.path.exists(cred_path):
        with open(cred_path, 'w') as f:
            json.dump(service_account_info, f, indent=2)

    # Initialize Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://chatbot-94efc-default-rtdb.firebaseio.com/'  # Replace with your actual DB URL
        })

# Firebase Logger Function
def log_to_firebase(data, path='/logs'):
    """Log data to Firebase Realtime Database"""
    try:
        initialize_firebase()
        ref = db.reference(path)
        ref.push(data)
        return True
    except Exception as e:
        print(f"Firebase logging error: {str(e)}")
        return False

# Example Usage
if __name__ == "__main__":
    test_data = {
        "timestamp": datetime.now().isoformat(),
        "event": "test_log",
        "message": "Firebase integration test"
    }
    
    if log_to_firebase(test_data):
        print("Successfully logged to Firebase")
    else:
        print("Failed to log to Firebase")