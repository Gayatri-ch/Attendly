import os
from deepface import DeepFace
from config import Config

class FaceRecognitionService:
    @staticmethod
    def find_match(frame, dataset_path):
        try:
            results = DeepFace.find(
                img_path=frame,
                db_path=dataset_path,
                model_name=Config.FACE_RECOGNITION_MODEL,
                detector_backend=Config.DETECTOR_BACKEND,
                enforce_detection=False,
                silent=True
            )
            
            if len(results) > 0 and not results[0].empty:
                match = results[0].iloc[0]
                # Filter by threshold (cosine distance)
                if match["distance"] < Config.SIMILARITY_THRESHOLD:
                    return match
            return None
        except Exception as e:
            print(f"[FACE SERVICE ERROR] {e}")
            return None
