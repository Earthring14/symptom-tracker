from flask import Flask, redirect, url_for, render_template, request
from main import transcribe, extract_fields, format_record
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    record = None

    if request.method == "POST":
        session_number = request.form["session_number"]
        audiofile = request.files["audiofile"]
        patient_name  = request.form["patient_name"]

        os.makedirs("Uploads", exist_ok=True)

        filename = audiofile.filename
        audiofile_path = os.path.join("Uploads", filename)

        audiofile.save(audiofile_path)

        transcript = transcribe(audiofile_path)
        extracted_fields = extract_fields(transcript)
        record = format_record(extracted_fields, patient_name, session_number)

    return render_template("index.html", record=record)

if __name__ == "__main__":
    app.run(debug=True)
