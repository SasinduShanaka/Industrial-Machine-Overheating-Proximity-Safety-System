from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

latest_data = {
    "temperature": 0,
    "distance": 0,
    "status": "Waiting for data..."
}

@app.route("/data", methods=["POST"])
def receive_data():
    global latest_data
    data = request.json

    temperature = data.get("temperature", 0)
    distance = data.get("distance", 0)

    # Simple status logic (UI only)
    if temperature > 29 and distance <= 5:
        status = "CRITICAL"
    elif temperature > 29:
        status = "OVERHEATING RISK"
    elif distance <= 5:
        status = "UNSAFE PROXIMITY"
    else:
        status = "NORMAL"

    latest_data = {
        "temperature": temperature,
        "distance": distance,
        "status": status
    }

    print("Received:", latest_data)
    return "OK"

@app.route("/status")
def status_api():
    return jsonify(latest_data)

@app.route("/")
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Industrial Safety Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            text-align: center;
        }
        .card {
            background: #1e293b;
            padding: 30px;
            margin: 80px auto;
            width: 350px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }
        h1 {
            margin-bottom: 20px;
        }
        .value {
            font-size: 22px;
            margin: 10px 0;
        }
        .status {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
        .NORMAL { color: #22c55e; }
        .OVERHEATING\\ RISK { color: #facc15; }
        .UNSAFE\\ PROXIMITY { color: #fb923c; }
        .CRITICAL { color: #ef4444; }
    </style>
</head>
<body>

<div class="card">
    <h1>Machine Safety Monitor</h1>

    <div class="value">🌡 Temperature: <span id="temp">--</span> °C</div>
    <div class="value">📡 Distance: <span id="dist">--</span> cm</div>

    <div class="status" id="status">Waiting...</div>
</div>

<script>
function updateData() {
    fetch("/status")
        .then(res => res.json())
        .then(data => {
            document.getElementById("temp").innerText = data.temperature;
            document.getElementById("dist").innerText = data.distance;

            let statusEl = document.getElementById("status");
            statusEl.innerText = data.status;
            statusEl.className = "status " + data.status;
        });
}

setInterval(updateData, 100);
updateData();
</script>

</body>
</html>
""")

app.run(host="0.0.0.0", port=5000)
