from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

RXTERMS_API_URL = "https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search"

@app.route('/')
def index():
    return render_template('prescription.html')

@app.route('/autocomplete')
def autocomplete():
    search_term = request.args.get('term', '')
    if not search_term:
        return jsonify([])

    params = {'terms': search_term}

    try:
        response = requests.get(RXTERMS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        suggestions = data[1] if data and len(data) > 1 else []
        return jsonify(suggestions)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return jsonify({"error": "Could not fetch suggestions"}), 500

@app.route('/api/submit_prescription', methods=['POST'])
def submit_prescription_api():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    print("Prescription data received:", data)
    return jsonify({
        "status": "success",
        "message": "Prescription successfully received."
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
