import face_recognition
import os

def verify_face(agent_id, uploaded_image_path):
    """
    Compares uploaded face with all known faces.
    Returns:
    {
        "matched": bool,
        "confidence": float
    }
    """

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        KNOWN_FACES_DIR = os.path.join(BASE_DIR, "known_faces")

        known_face_files = [
            f for f in os.listdir(KNOWN_FACES_DIR)
            if f.lower().endswith(".jpg")
        ]

        if not known_face_files:
            return {"matched": False, "confidence": 0.0}

        uploaded_image = face_recognition.load_image_file(uploaded_image_path)
        uploaded_encodings = face_recognition.face_encodings(uploaded_image)

        if not uploaded_encodings:
            return {"matched": False, "confidence": 0.0}

        uploaded_encoding = uploaded_encodings[0]
        best_distance = None

        for face_file in known_face_files:
            known_image_path = os.path.join(KNOWN_FACES_DIR, face_file)
            known_image = face_recognition.load_image_file(known_image_path)
            known_encodings = face_recognition.face_encodings(known_image)

            if not known_encodings:
                continue

            distance = face_recognition.face_distance(
                [known_encodings[0]],
                uploaded_encoding
            )[0]

            if best_distance is None or distance < best_distance:
                best_distance = distance

        if best_distance is None:
            return {"matched": False, "confidence": 0.0}

        MATCH_THRESHOLD = 0.6
        matched = best_distance < MATCH_THRESHOLD
        confidence = max(0.0, min(1.0, 1 - best_distance)) * 100

        return {
            "matched": matched,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        print("Face match error:", e)
        return {"matched": False, "confidence": 0.0}
