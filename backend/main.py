from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(name, static_folder="../frontend")

@app.route("/")
def root():
return send_from_directory(app.static_folder, "index.html")

@app.route("/api/greet", methods=["POST"])
def greet():
data = request.get_json(silent=True) or {}
name = data.get("name", "").strip()
if not name:
return jsonify({"error": "Falta el nombre"}), 400
return jsonify({"greeting": f"Hola {name}"})

if name == "main":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
