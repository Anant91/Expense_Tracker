from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # allow all origins (development). For production, pass resources/origins.

# Example endpoints that match the frontend expectations
expenses = [
    {"id":1, "date":"2025-11-25", "amount":100, "category":"food", "note":"pizza"},
    {"id":2, "date":"2025-11-24", "amount":50,  "category":"travel","note":"bus"}
]

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    return jsonify(success=True, expenses=expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json() or {}
    new_id = (expenses[-1]['id'] if expenses else 0) + 1
    item = {
      "id": new_id,
      "date": data.get("date"),
      "amount": data.get("amount"),
      "category": data.get("category"),
      "note": data.get("note")
    }
    expenses.append(item)
    return jsonify(success=True, id=new_id)

# Simple export simulation (immediate finish)
@app.route('/api/export/start', methods=['POST'])
def start_export():
    # in a real app start background task; here just respond success
    return jsonify(success=True)

@app.route('/api/export/status', methods=['GET'])
def export_status():
    return jsonify(status={"running": False, "finished_at": "now", "path": "/tmp/export.xlsx"})

@app.route('/api/export/download', methods=['GET'])
def export_download():
    # for demo, return a small CSV file generated on the fly
    from io import BytesIO
    f = BytesIO()
    f.write(b"id,date,amount,category,note\n1,2025-11-25,100,food,pizza\n")
    f.seek(0)
    return send_file(f, as_attachment=True, download_name="export.csv", mimetype="text/csv")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
