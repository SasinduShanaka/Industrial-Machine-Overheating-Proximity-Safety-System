from flask import Flask, request, jsonify

app = Flask(__name__)

latest_data = {"temperature": 0, "distance": 0}

@app.route("/data", methods=["POST"])
def receive_data():
    global latest_data
    latest_data = request.json
    print("Received:", latest_data)
    return "OK"

@app.route("/")
def dashboard():
    return f"""
    <h2>Industrial Safety Dashboard</h2>
    <p>Temperature: {latest_data['temperature']} °C</p>
    <p>Distance: {latest_data['distance']} cm</p>
    """

app.run(host="0.0.0.0", port=5000)
