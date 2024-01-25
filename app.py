from flask import Flask, render_template
from Controller.PdfController import pdfController

app = Flask(__name__)
app.register_blueprint(pdfController)


@app.route("/")
def index():
    return render_template("./pages/history-check04.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)  # 端口号默认是5000
