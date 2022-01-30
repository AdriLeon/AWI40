import pyrebase
import firebase_config as token

firebase = pyrebase.initialize_app(token.firebaseConfig)
auth = firebase.auth()

email = "correo_2@outlook.com"
password = "0987654321"

user = auth.sign_in_with_email_and_password(email, password)
print(user['localId'])
