from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load agent database
with open("backend/database.json", "r") as file:
    data = json.load(file)
    agents = {agent["id"]: agent for agent in data["agents"]}

@app.route("/")
def home():
    return "Securify Backend Running"

@app.route("/verify", methods=["POST"])
def verify_agent():
    data = request.json
    agent_id = data.get("agent_id")

    if agent_id in agents:
        agent = agents[agent_id]

        risk = "Low" if agent["trust_score"] >= 0.6 else "Medium"

        return jsonify({
            "verified": True,
            "agent": agent,
            "risk_level": risk
        })
    else:
        return jsonify({
            "verified": False,
            "risk_level": "High"
        })

if __name__ == "__main__":
    app.run(debug=True)
