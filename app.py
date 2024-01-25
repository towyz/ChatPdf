import json
from flask import Flask, jsonify, redirect, render_template, url_for
from Controller.PdfController import pdfController

app = Flask(__name__)
app.config["SECRET_KEY"] = "SESSION_NEED_THIS_12138"
app.register_blueprint(pdfController)


@app.route("/get_conversation_dir")
def get_conversation_dir():
    """Get the dir of pdfs."""
    with open("./settings/pdf_source.json", "r") as file:
        conversation_data = json.load(file)
    return jsonify(conversation_data)


@app.route("/get_conversation_data/<conversation_id>")
def get_conversation_data(conversation_id):
    with open("./history/" + conversation_id + ".json", "r") as file:
        conversation_data = json.load(file)
    return jsonify(conversation_data)


@app.route("/chat/<conversation_id>")
def chat(conversation_id):
    return render_template("history-check04.html", conversation_id=conversation_id)


@app.route("/")
def index():
    return render_template("show-pdf-dir.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)  # 端口号默认是5000
