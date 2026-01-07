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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>

<div class="container">
    <div class="header">
        <h1>⚙️ Industrial Safety Monitor</h1>
        <p>Real-time machine monitoring system</p>
    </div>

    <div class="dashboard">
        <div class="metric-card">
            <div class="metric-icon temp-icon">🌡️</div>
            <div class="metric-label">Temperature</div>
            <div class="metric-value">
                <span id="temp">--</span><span class="metric-unit">°C</span>
            </div>
        </div>

        <div class="metric-card">
            <div class="metric-icon dist-icon">📡</div>
            <div class="metric-label">Proximity Distance</div>
            <div class="metric-value">
                <span id="dist">--</span><span class="metric-unit">cm</span>
            </div>
        </div>
    </div>

    <div class="status-card">
        <div class="status-label">System Status</div>
        <div class="status-value" id="status">Waiting...</div>
    </div>
    
    <div class="footer">
        Last updated: <span id="timestamp">--</span>
    </div>
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
            statusEl.className = "status-value status-" + data.status.replace(/ /g, "\\ ");
            
            const now = new Date();
            document.getElementById("timestamp").innerText = now.toLocaleTimeString();
        });
}

setInterval(updateData, 100);
updateData();
</script>

</body>
</html>
""")

app.run(host="0.0.0.0", port=5000)
