from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from face_match import verify_face

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
RESULTS_FILE = os.path.join(BASE_DIR, "results.json")
DATABASE_FILE = os.path.join(BASE_DIR, "database.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ Load Agents ------------------
with open(DATABASE_FILE, "r") as f:
    agents_data = json.load(f)["agents"]
    agents = {agent["id"]: agent for agent in agents_data}

# ------------------ Helpers ------------------
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)["users"]

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users}, f, indent=4)

def load_results():
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)["results"]

def save_results(results):
    with open(RESULTS_FILE, "w") as f:
        json.dump({"results": results}, f, indent=4)

# ------------------ Routes ------------------
@app.route("/")
def home():
    return "Securify Backend Running"

# -------- LOGIN --------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    users = load_users()

    for user in users:
        if user["username"] == data.get("username") and user["password"] == data.get("password"):
            return jsonify({"success": True})

    return jsonify({"success": False})

# -------- REGISTER --------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    users = load_users()

    if any(u["username"] == data.get("username") for u in users):
        return jsonify({"success": False})

    users.append({
        "username": data.get("username"),
        "password": data.get("password")
    })

    save_users(users)
    return jsonify({"success": True})

# -------- VERIFY --------
@app.route("/verify", methods=["POST"])
def verify_agent():
    agent_id = request.form.get("agentId")
    image = request.files.get("image")

    if agent_id not in agents:
        return jsonify({"success": False, "status": "fail", "confidence": 0})

    if not image:
        return jsonify({"success": False, "status": "fail", "confidence": 0})

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    result = verify_face(agent_id, image_path)
    os.remove(image_path)

    agent = agents[agent_id]

    if result["matched"]:
        agent["trust_score"] = min(agent["trust_score"] + 0.05, 1.0)
        status = "success"
    else:
        agent["trust_score"] = max(agent["trust_score"] - 0.1, 0.0)
        status = "fail"

    with open(DATABASE_FILE, "w") as f:
        json.dump({"agents": list(agents.values())}, f, indent=4)

    results = load_results()
    results.append({
        "agentId": agent_id,
        "status": status,
        "confidence": result["confidence"],
        "timestamp": datetime.now().isoformat()
    })
    save_results(results)

    return jsonify({
        "success": True,
        "status": status,
        "confidence": result["confidence"]
    })

# -------- DASHBOARD --------
@app.route("/dashboard", methods=["GET"])
def dashboard():
    results = load_results()
    return jsonify({
        "total": len(results),
        "success": len([r for r in results if r["status"] == "success"]),
        "fail": len([r for r in results if r["status"] == "fail"])
    })

# ------------------ Run ------------------
if __name__ == "__main__":
    app.run(debug=True)

