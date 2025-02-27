import firebase_admin
from firebase_admin import credentials, db

class FirebaseDB:
    def __init__(self, credential_path, database_url):
        #Se inicializa firebase con las credenciales de la cuenta de servicio
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })

    def write_record(self, path, data):
        # Write data to the specified path in the Realtime Database
        ref = db.reference(path)
        ref.push(data)

    def read_record(self, path):
        # Read data from the specified path in the Realtime Database
        ref = db.reference(path)
        data = ref.get()
        if data is None:
            raise ValueError(f"No data found at path: {path}")
        return data

    def update_record(self, path, data):
        # Update data at the specified path in the Realtime Database
        ref = db.reference(path)
        ref.update(data)

    def delete_record(self, path):
        # Delete data at the specified path in the Realtime Database
        ref = db.reference(path)
        ref.delete()