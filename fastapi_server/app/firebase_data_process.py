import json
import datetime

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("/code/./app/yard-soccer-detection-firebase-adminsdk-kfvya-70e5867256.json")

firebase_admin.initialize_app(cred, {'databaseURL': 'https://12-yard-soccer-detection.firebaseio.com'})

def save_data_to_firebase_db(grid_shoot_data, percentage, pivot_foot_bias, hit_pos, target):
    shoot_data = {
        "grid_shoot_data" : json.dumps(grid_shoot_data),
        "percentage" : percentage,
        "pivot_foot_bias" : pivot_foot_bias,
        "hit_pos" : hit_pos,
        "target" : target,
        "created_at": datetime.datetime.now
    } 

    db = firestore.client()

    new_shoot_data_ref = db.collection("soccer-shoot-datas").document()

    new_shoot_data_ref.set(shoot_data)