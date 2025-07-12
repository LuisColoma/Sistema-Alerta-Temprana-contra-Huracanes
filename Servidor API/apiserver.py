import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "alerts.json"

# Al iniciar, intenta cargar el JSON desde disco
try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        alerts = data.get("alertas", [])  # Cargamos desde clave "alertas"
except FileNotFoundError:
    alerts = []

def save_alerts_to_disk():
    with open(DATA_FILE, "w") as f:
        json.dump({"alertas": alerts}, f, indent=2)  # Guardamos envuelto

@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify({"alertas": alerts}), 200

@app.route("/alerts", methods=["POST"])
def post_alert():
    fecha_utc = datetime.utcnow().isoformat() + "Z"
    fecha_formateada = fecha_utc[:10]
    id = str(len(alerts)+1)
    data = request.get_json()
    data["received_at"] = fecha_formateada
    data["id"] = "ALERTA-"+fecha_formateada + "-" + id
    data["image_url"] = f"/static/images/img_{data['received_at']}.jpg"
    alerts.append(data)
    save_alerts_to_disk()   # ← Persistir a JSON
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
