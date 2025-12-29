from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample agent database (temporary)
agents = {
    "AG001": {
        "name": "Ramesh Kumar",
        "organization": "Bank XYZ",
        "status": "Active",
        "trust_score": 0.6
    }
}

@app.route("/")
def home():
    return "Securify Backend Running"

@app.route("/verify", methods=["POST"])
def verify_agent():
    data = request.json
    agent_id = data.get("agent_id")

    if agent_id in agents:
        return jsonify({
            "verified": True,
            "agent": agents[agent_id],
            "risk_level": "Low"
        })
    else:
        return jsonify({
            "verified": False,
            "risk_level": "High"
        })

if __name__ == "__main__":
    app.run(debug=True)

