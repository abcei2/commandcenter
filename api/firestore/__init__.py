import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
"""
    Expected collections:
    - PHRecords
    - PPMRecords
"""
class Firestore:
    
    def __init__(self,pathToCreds):
        cred = credentials.Certificate(pathToCreds)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        
    def savePh(self, ph, temperature = None):
        doc_ref = self.db.collection(u'PHRecords').document()
        doc_ref.set({
            u'ph': ph,
            u'created': datetime.datetime.now(tz=datetime.timezone.utc),
            u'temperature': temperature
        })

    def savePPM(self, ppm, temperature = None):
        doc_ref = self.db.collection(u'PPMRecords').document()
        doc_ref.set({
            u'ppm': ppm,
            u'created': datetime.datetime.now(tz=datetime.timezone.utc),
            u'temperature': temperature
        })