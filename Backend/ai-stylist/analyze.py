import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Allows cross-origin requests
from werkzeug.utils import secure_filename
from model import analyze_with_fine_tuning  # Import your analysis function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/analyze", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Call the analyze_with_fine_tuning function after saving the file
        results = analyze_with_fine_tuning(file_path)

        # Return the results as a JSON response
        return (
            jsonify(
                {
                    "message": "File uploaded and analyzed successfully",
                    "filename": filename,
                    "results": results,
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    app.run(debug=True)
