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
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e5e7eb;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 900px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            animation: fadeInDown 0.6s ease-out;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa 0%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #94a3b8;
            font-size: 1rem;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 20px;
            padding: 28px;
            transition: all 0.3s ease;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            border-color: rgba(148, 163, 184, 0.2);
        }
        
        .metric-icon {
            width: 60px;
            height: 60px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin-bottom: 16px;
        }
        
        .temp-icon {
            background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
            box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
        }
        
        .dist-icon {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
        }
        
        .metric-label {
            font-size: 0.875rem;
            color: #94a3b8;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #f1f5f9;
            line-height: 1;
        }
        
        .metric-unit {
            font-size: 1.25rem;
            color: #64748b;
            margin-left: 6px;
        }
        
        .status-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 20px;
            padding: 32px;
            text-align: center;
            animation: fadeInUp 0.8s ease-out;
            transition: all 0.3s ease;
        }
        
        .status-label {
            font-size: 0.875rem;
            color: #94a3b8;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }
        
        .status-value {
            font-size: 2rem;
            font-weight: 700;
            padding: 16px 32px;
            border-radius: 12px;
            display: inline-block;
            transition: all 0.3s ease;
            animation: pulse 2s ease-in-out infinite;
        }
        
        .status-NORMAL {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
            color: white;
        }
        
        .status-OVERHEATING\\ RISK {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
            color: white;
        }
        
        .status-UNSAFE\\ PROXIMITY {
            background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
            box-shadow: 0 10px 30px rgba(251, 146, 60, 0.3);
            color: white;
        }
        
        .status-CRITICAL {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.4);
            color: white;
            animation: criticalPulse 1s ease-in-out infinite;
        }
        
        .status-Waiting\\.\\.\\. {
            background: linear-gradient(135deg, #64748b 0%, #475569 100%);
            box-shadow: 0 10px 30px rgba(100, 116, 139, 0.3);
            color: white;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.02);
            }
        }
        
        @keyframes criticalPulse {
            0%, 100% {
                transform: scale(1);
                box-shadow: 0 10px 30px rgba(239, 68, 68, 0.4);
            }
            50% {
                transform: scale(1.05);
                box-shadow: 0 15px 40px rgba(239, 68, 68, 0.6);
            }
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #64748b;
            font-size: 0.875rem;
        }
        
        @media (max-width: 640px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .metric-value {
                font-size: 2rem;
            }
            
            .status-value {
                font-size: 1.5rem;
                padding: 12px 24px;
            }
        }
    </style>
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
