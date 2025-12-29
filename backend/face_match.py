import face_recognition

def verify_face(agent_id, uploaded_image_path):
    try:
        known_image_path = f"backend/known_faces/{agent_id}.jpg"

        known_image = face_recognition.load_image_file(known_image_path)
        uploaded_image = face_recognition.load_image_file(uploaded_image_path)

        known_encoding = face_recognition.face_encodings(known_image)
        uploaded_encoding = face_recognition.face_encodings(uploaded_image)

        if not known_encoding or not uploaded_encoding:
            return False

        result = face_recognition.compare_faces(
            [known_encoding[0]],
            uploaded_encoding[0]
        )

        return result[0]

    except Exception as e:
        return False
