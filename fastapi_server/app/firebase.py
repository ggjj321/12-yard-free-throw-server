import firebase_admin

from firebase_admin import credentials


cred = credentials.Certificate("./yard-soccer-detection-firebase-adminsdk-kfvya-70e5867256.json")

firebase_admin.initialize_app(cred)

