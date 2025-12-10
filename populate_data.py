# populate_data.py
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def populate_hospitals():
    """Add real hospital data for Cambodia"""
    hospitals = [
        {
            'name': 'Calmette Hospital',
            'address': 'Monivong Blvd, Phnom Penh',
            'city': 'Phnom Penh',
            'phone': '+855-23-426-948',
            'specialties': ['Dermatology', 'Infectious Disease', 'Oncology'],
            'rating': 4.3,
            'is_verified': True,
            'emergency_services': True,
            'languages': ['Khmer', 'English', 'French']
        },
        {
            'name': 'Royal Phnom Penh Hospital', 
            'address': '888 Russian Confederation Blvd, Phnom Penh',
            'city': 'Phnom Penh',
            'phone': '+855-23-991-000',
            'specialties': ['Dermatology', 'Cosmetology', 'General Medicine'],
            'rating': 4.6,
            'is_verified': True,
            'emergency_services': True,
            'languages': ['Khmer', 'English', 'Thai']
        },
        {
            'name': 'Sihanouk Hospital Center of HOPE',
            'address': 'St. 134, Sangkat Vealvong, Phnom Penh',
            'city': 'Phnom Penh',
            'phone': '+855-23-882-248',
            'specialties': ['Dermatology', 'Infectious Disease', 'Community Health'],
            'rating': 4.4,
            'is_verified': True,
            'emergency_services': True,
            'languages': ['Khmer', 'English']
        },
        {
            'name': 'Sen Sok International University Hospital',
            'address': 'Street 1986, Phnom Penh',
            'city': 'Phnom Penh', 
            'phone': '+855-97-379-7777',
            'specialties': ['Dermatology', 'General Medicine', 'Pediatrics'],
            'rating': 4.2,
            'is_verified': True,
            'emergency_services': True,
            'languages': ['Khmer', 'English', 'Chinese']
        },
        {
            'name': 'Preah Kossamak Hospital',
            'address': 'Preah Monivong Blvd, Phnom Penh',
            'city': 'Phnom Penh',
            'phone': '+855-23-430-077',
            'specialties': ['Dermatology', 'General Medicine', 'Public Health'],
            'rating': 4.1,
            'is_verified': True,
            'emergency_services': True,
            'languages': ['Khmer', 'English']
        }
    ]
    
    for hospital in hospitals:
        db.collection('hospitals').add(hospital)
        print(f"Added: {hospital['name']}")

def populate_disease_mappings():
    """Add disease to specialty mappings for Cambodian context"""
    mappings = [
        {
            'disease_class': '1. Enfeksiyonel',
            'primary_specialty': 'Infectious Disease',
            'urgency_level': 'medium',
            'description_en': 'Infectious skin diseases common in tropical climate',
            'description_kh': 'ជំងឺស្បែកឆ្លងក្នុងអាកាសធាតុត្រូពិក'
        },
        {
            'disease_class': '2. Ekzama',
            'primary_specialty': 'Dermatology', 
            'urgency_level': 'low',
            'description_en': 'Eczema and allergic skin reactions',
            'description_kh': 'ជំងឺស្បែកអេកសែម និងប្រតិកម្មអាលែកហ្ស៊ី'
        },
        {
            'disease_class': '3. Akne',
            'primary_specialty': 'Dermatology',
            'urgency_level': 'low',
            'description_en': 'Acne and skin inflammation',
            'description_kh': 'ជំងឺមុន និងការរលាកស្បែក'
        },
        {
            'disease_class': '4. Pigment',
            'primary_specialty': 'Dermatology',
            'urgency_level': 'low',
            'description_en': 'Skin pigmentation and discoloration',
            'description_kh': 'បញ្ហាពណ៌ស្បែក និងការផ្លាស់ប្តូរពណ៌'
        },
        {
            'disease_class': '5. Benign',
            'primary_specialty': 'Dermatology',
            'urgency_level': 'low',
            'description_en': 'Non-cancerous skin growths and moles',
            'description_kh': 'ការលូតលាស់ស្បែកមិនមែនជាមហារីក'
        },
        {
            'disease_class': '6. Malign',
            'primary_specialty': 'Oncology',
            'urgency_level': 'high',
            'description_en': 'Skin cancer - requires immediate medical attention',
            'description_kh': 'ជំងឺមហារីកស្បែក - ត្រូវការការព្យាបាលភ្លាមៗ',
            'emergency_note': 'URGENT - Seek immediate medical care'
        }
    ]
    
    for mapping in mappings:
        db.collection('disease_mappings').add(mapping)
        print(f"Added mapping for: {mapping['disease_class']}")

def populate_cambodia_cities():
    """Add major Cambodian cities"""
    cities_data = [
        {
            'name': 'Phnom Penh',
            'hospitals_count': 5,
            'region': 'Central'
        },
        {
            'name': 'Siem Reap',
            'hospitals_count': 3,
            'region': 'Northwest'
        },
        {
            'name': 'Sihanoukville',
            'hospitals_count': 2,
            'region': 'Southwest'
        },
        {
            'name': 'Battambang',
            'hospitals_count': 2,
            'region': 'Northwest'
        },
        {
            'name': 'Kampong Cham',
            'hospitals_count': 1,
            'region': 'Central'
        }
    ]
    
    for city in cities_data:
        db.collection('cities').add(city)
        print(f"Added city: {city['name']}")

if __name__ == "__main__":
    print("Populating database with Cambodian healthcare data...")
    populate_hospitals()
    populate_disease_mappings()
    populate_cambodia_cities()
    print("Database population complete!")