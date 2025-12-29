from flask import Flask, request, jsonify
import json
import os
from face_match import verify_face

app = Flask(__name__)

UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load agent database
with open("backend/database.json", "r") as file:
    data = json.load(file)
    agents = {agent["id"]: agent for agent in data["agents"]}

@app.route("/")
def home():
    return "Securify Backend Running"

@app.route("/verify", methods=["POST"])
def verify_agent():
    agent_id = request.form.get("agent_id")
    image = request.files.get("image")

    if agent_id not in agents:
        return jsonify({"verified": False, "reason": "Agent not found"})

    if not image:
        return jsonify({"verified": False, "reason": "Image not provided"})

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    face_verified = verify_face(agent_id, image_path)

    os.remove(image_path)  # privacy-first: delete uploaded image

    if face_verified:
        return jsonify({
            "verified": True,
            "risk_level": "Low",
            "message": "Face verified successfully"
        })
    else:
        return jsonify({
            "verified": False,
            "risk_level": "High",
            "message": "Face mismatch"
        })

if __name__ == "__main__":
    app.run(debug=True)
