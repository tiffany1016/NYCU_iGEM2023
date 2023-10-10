from flask import Flask, render_template, request, jsonify
from joblib import load
from Bio import SeqIO
import numpy as np
import re
import io

app = Flask(__name__, template_folder='templates', static_folder='static')

data = np.load("./model/uniprotSeq.npz")
svm_model = load('./model/svm.joblib')
scaler = load('./model/scaler.joblib')

def extractEntryId(entry_name):
    match = re.match(r".*\|([A-Z0-9]+)\|.*", entry_name)
    if match:
        return match.group(1)
    else:
        return "N/A"

def embedEntry(entry):
    return data[entry]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/classify', methods=['POST'])
def process_fasta_data():
    if request.method == 'POST':

        data = request.get_json()

        entryIds = data.get('entryIds', [])
        response_data = {'message': 'Data received and processed successfully'}
        return jsonify(response_data), 200
    
def classify():
    try:
        fasta_file = request.files['fastaFile']
        if fasta_file:
            fasta_contents = fasta_file.read().decode("utf-8")
            entries = [str(record.id) for record in SeqIO.parse(io.StringIO(fasta_contents), 'fasta')]

            results = []

            for entry in entries:
                embedded_entry = embedEntry(entry)
                X_reshaped = embedded_entry.reshape(1, -1)
                X_scaled = scaler.transform(X_reshaped)
                svm_pred = svm_model.predict_proba(X_scaled)

                if 0 <= svm_pred[0][1] < 0.3:
                    pred = "Impossible"
                elif 0.3 <= svm_pred[0][1] < 0.5:
                    pred = "Not quite"
                elif 0.5 <= svm_pred[0][1] < 0.7:
                    pred = "Can be"
                elif 0.7 <= svm_pred[0][1] <= 1:
                    pred = "Highly possible"

                results.append(f"Prediction for {entry}: {svm_pred[0][1]:.2%} {pred}")

            return "\n".join(results)
        else:
            return "No file provided."

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(port=8080)
