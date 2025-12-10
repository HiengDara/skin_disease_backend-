import firebase_admin
from firebase_admin import credentials, firestore
import json

def test_firebase():
    print("Testing Firebase Connection...")
    print("=" * 50)
    
    try:
        # Initialize Firebase with your service account
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully!")
        
        # Get Firestore client
        db = firestore.client()
        print("Firestore client created!")
        
        # Test writing data
        test_data = {
            'message': 'Hello from Skin Disease App!',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'project': 'skin-disease-classifier',
            'status': 'connected'
        }
        
        # Write to Firestore
        doc_ref = db.collection('connection_tests').document('python_test')
        doc_ref.set(test_data)
        print("Data written to Firestore!")
        
        # Read back the data
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            print(f"Data read successfully: {data}")
        else:
            print("Could not read data back")
        
        # Test adding a hospital
        hospital_data = {
            'name': 'Test Dermatology Center - Python',
            'city': 'İstanbul',
            'specialties': ['Dermatology', 'Test Specialty'],
            'phone': '+90-212-999-8888',
            'rating': 4.5,
            'is_verified': True
        }
        
        hospital_ref = db.collection('hospitals').add(hospital_data)
        print(f"Hospital added with ID: {hospital_ref[1].id}")
        
        # Query hospitals
        hospitals = db.collection('hospitals').where('city', '==', 'İstanbul').stream()
        hospital_count = 0
        for hospital in hospitals:
            hospital_count += 1
            print(f"🏥 Found: {hospital.to_dict()['name']}")
        
        print(f"Found {hospital_count} hospitals in Istanbul")
        
        print("=" * 50)
        print("FIREBASE CONNECTION SUCCESSFUL!")
        print("Your project: skin-disease-classifier-fe36b")
        print("You can now build your skin disease app!")
        
        return True
        
    except Exception as e:
        print(f"Firebase test failed: {e}")
        return False

if __name__ == "__main__":
    test_firebase()