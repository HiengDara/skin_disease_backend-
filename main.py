# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import uvicorn

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI(
    title="Skin Disease Classification API - Cambodia",
    description="AI-powered skin disease detection with Cambodian hospital recommendations",
    version="1.0.0"
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your skin disease classes
CLASS_NAMES = [
    '1. Enfeksiyonel',
    '2. Ekzama',
    '3. Akne',
    '4. Pigment',
    '5. Benign',
    '6. Malign'
]

class SkinDiseaseModel:
    def __init__(self, model_path: str = "ml_model/best_skin_model.keras"):
        self.model = None
        self.model_path = model_path
        self.input_size = (380, 380)
        self.load_model()
    
    def load_model(self):
        """Load your trained TensorFlow model"""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print("ML Model loaded successfully")
        except Exception as e:
            print(f"Model failed to load: {e}")
            raise RuntimeError("Model could not be loaded.")

    def preprocess_image(self, image: Image.Image):
        """
        MATCHES TRAINING PREPROCESSING EXACTLY:
        - Resize 380x380
        - RGB (same as training)
        - Normalize 0–1 (same as ImageDataGenerator rescale=1/255)
        - Expand dims
        """
        image = image.resize(self.input_size)
        image_array = np.array(image).astype(np.float32) / 255.0
        image_batch = np.expand_dims(image_array, axis=0)
        return image_batch
    
    def predict(self, image: Image.Image):
        """Run model prediction"""
        if self.model is None:
            raise RuntimeError("Model not loaded.")
        
        processed_image = self.preprocess_image(image)
        predictions = self.model.predict(processed_image)
        return predictions


# Initialize model
model_loader = SkinDiseaseModel()



class FirebaseManager:
    def get_hospitals_by_specialty(self, specialty: str, city: str = "Phnom Penh", limit: int = 3):
        try:
            hospitals_ref = db.collection('hospitals')
            query = hospitals_ref.where('specialties', 'array_contains', specialty)
            query = query.where('city', '==', city)
            query = query.where('is_verified', '==', True)
            
            result = []
            for hospital in query.limit(limit).stream():
                d = hospital.to_dict()
                d['id'] = hospital.id
                result.append(d)
            return result
        except Exception as e:
            print(f"Error getting hospitals: {e}")
            return []
    
    def get_disease_mapping(self, disease_class: str):
        try:
            ref = db.collection('disease_mappings')
            docs = ref.where('disease_class', '==', disease_class).stream()
            for d in docs:
                return d.to_dict()
            return None
        except Exception as e:
            print(f"Error getting disease mapping: {e}")
            return None
    
    def get_available_cities(self):
        try:
            ref = db.collection('cities')
            return sorted([c.to_dict()['name'] for c in ref.stream()])
        except:
            return ['Phnom Penh']


firebase_manager = FirebaseManager()



@app.get("/")
async def root():
    return {
        "message": "Skin Disease Classification API - Cambodia",
        "status": "active",
        "cities_available": firebase_manager.get_available_cities()
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": (model_loader.model is not None),
        "firebase_connected": True,
        "cities": firebase_manager.get_available_cities()
    }



@app.post("/predict")
async def predict_skin_disease(
    request: Request,
    file: UploadFile = File(...),
    city: str = "Phnom Penh"
):
    """
    Upload a skin image → classify → map disease → recommend hospitals
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Please upload an image file")

        # Load image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        # Predict disease
        predictions = model_loader.predict(image)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]
        confidence = float(np.max(predictions))

        # Mapping from database
        disease_mapping = firebase_manager.get_disease_mapping(predicted_class)
        if not disease_mapping:
            raise HTTPException(status_code=500, detail="Disease mapping not found in database")

        # Hospital recommendations
        hospitals = firebase_manager.get_hospitals_by_specialty(
            disease_mapping['primary_specialty'],
            city,
            limit=3
        )

        return {
            "prediction": {
                "disease_class": predicted_class,
                "confidence": confidence,
                "specialty": disease_mapping['primary_specialty'],
                "urgency_level": disease_mapping['urgency_level'],
                "description_en": disease_mapping.get("description_en", ""),
                "description_kh": disease_mapping.get("description_kh", ""),
                "emergency_note": disease_mapping.get("emergency_note", "")
            },
            "recommended_hospitals": hospitals,
            "all_probabilities": {
                CLASS_NAMES[i]: float(predictions[0][i]) for i in range(len(CLASS_NAMES))
            },
            "location": {
                "city": city,
                "country": "Cambodia"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")



@app.get("/hospitals/{city}")
async def get_hospitals_by_city(city: str):
    hospitals_ref = db.collection('hospitals')
    query = hospitals_ref.where('city', '==', city).where('is_verified', '==', True)

    results = []
    for h in query.stream():
        d = h.to_dict()
        d['id'] = h.id
        results.append(d)

    return {"city": city, "country": "Cambodia", "hospitals": results}



@app.get("/cities")
async def get_cities():
    return {
        "country": "Cambodia",
        "cities": firebase_manager.get_available_cities()
    }



if __name__ == "__main__":
    print("Starting Skin Disease Classification API - Cambodia")
    print("API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
