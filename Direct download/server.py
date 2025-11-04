from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 FileUploaderBot is Running Successfully!"

@app.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
