import json
import os
import time

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "SESSION_NEED_THIS_12138"
app.config["UPLOAD_FOLDER"] = "./paper"


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
    return render_template("chat02.html", conversation_id=conversation_id)


@app.route("/")
def index():
    return render_template("show-pdf-dir02.html")


@app.route("/send_message/<conversation_id>", methods=["POST"])
def send_message(conversation_id):
    data = request.get_json()
    user_message = data.get("user")
    # print("User:", user_message)

    with open(os.path.join(os.path.abspath("."), "settings", "API_KEYS.json")) as f:
        api_key = json.load(f)["ChatPDF_API"]
    sourceId = conversation_id

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    message = {
        "role": "user",
        "content": user_message,
    }

    data = {
        "sourceId": sourceId,
        "messages": [message],
    }
    # print(data)

    response = requests.post(
        "https://api.chatpdf.com/v1/chats/message", headers=headers, json=data
    )

    output_dir = "./history"
    if response.status_code == 200:
        print("Result:", response.json()["content"])

        # store the history of chatting
        listdir = os.listdir(output_dir)
        if str(sourceId) + ".json" in listdir:
            with open(os.path.join(output_dir, str(sourceId) + ".json"), "r") as f:
                model = json.load(f)

            temp_msg = {}
            temp_msg["user"] = message["content"]
            temp_msg["assistant"] = response.json()["content"]

            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            model[current_time] = temp_msg
            updated_data = json.dumps(model)

            with open(
                os.path.join(output_dir, str(sourceId) + ".json"), "w"
            ) as fw:  # w: override
                fw.write(updated_data)
    else:
        print("Status:", response.status_code)
        print("Error:", response.text)

    # 重新读一遍咯
    with open(os.path.join(output_dir, str(sourceId) + ".json"), "r") as f:
        new_data = json.load(f)

    return jsonify(new_data)


def record_pdf_source(source_id):
    """Record the pdf source id in the json file."""
    output_dir = "./settings"
    listdir = os.listdir(output_dir)

    if "pdf_source.json" in listdir:
        fr = open(os.path.join(output_dir, "pdf_source.json"))  # a represents append
        model = json.load(fr)
        fr.close()

        for i in source_id:
            model[i] = source_id[i]
        jsObj = json.dumps(model)

        with open(
            os.path.join(output_dir, "pdf_source.json"), "w"
        ) as fw:
            fw.write(jsObj)


@app.route("/upload_file", methods=["POST"])
def upload_file():
    # try:
    uploaded_file = request.files["file"]

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
    uploaded_file.save(file_path)

    # print("File saved to: ", os.path.abspath(file_path))

    # 数据准备
    with open(
        os.path.join(os.path.abspath("."), "settings", "API_KEYS.json")
    ) as f:
        api_key = json.load(f)["ChatPDF_API"]

    headers = {"x-api-key": api_key}
    files = [("file", ("file", open(file_path, "rb"), "application/octet-stream"))]

    response = requests.post(
        "https://api.chatpdf.com/v1/sources/add-file", headers=headers, files=files
    )

    if response.status_code == 200:
        print("Source ID:", response.json()["sourceId"])
        # store the source id in the json file
        source_id = {response.json()["sourceId"]: file_path}
        record_pdf_source(source_id)

        # create a history file to store the chatting history
        output_dir = "./history"
        listdir = os.listdir(output_dir)
        if str(response.json()["sourceId"]) + ".json" not in listdir:
            with open(
                os.path.join(output_dir, str(response.json()["sourceId"]) + ".json"),
                "w",
            ) as f:
                f.write("{}")
    else:
        print("Status:", response.status_code)
        print("Error:", response.text)

    with open("./settings/pdf_source.json", "r") as file:
        conversation_data = json.load(file)
    return jsonify(conversation_data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)  # 端口号默认是5000
