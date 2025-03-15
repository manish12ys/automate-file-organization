from flask import Flask, request, jsonify, render_template
import os
import shutil

app = Flask(__name__)

FILE_TYPE_MAPPING = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".flv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
    "Others": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize_files():
    data = request.json
    folder_path = data.get('folder')

    if not folder_path or not os.path.exists(folder_path):
        return jsonify({"status": "error", "message": "Invalid folder path"}), 400

    # Create folders if they don't exist
    for folder in FILE_TYPE_MAPPING.keys():
        folder_dir = os.path.join(folder_path, folder)
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)

    # Get all files from the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files:
        file_path = os.path.join(folder_path, file)
        file_extension = os.path.splitext(file)[1].lower()

        destination_folder = "Others"
        for folder, extensions in FILE_TYPE_MAPPING.items():
            if file_extension in extensions:
                destination_folder = folder
                break

        destination_path = os.path.join(folder_path, destination_folder, file)
        shutil.move(file_path, destination_path)

    return jsonify({"status": "success", "message": "Files organized successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
