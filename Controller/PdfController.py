from flask import request, Blueprint, jsonify, render_template
from Service.PdfService import PdfService


pdfController = Blueprint("pdfController", __name__)
pdfService = PdfService()


@pdfController.route("/get_answer")
def get_answer():
    """Get the question from user, and get the answer from the API"""
    data = request.get_json()
    # TODO: 不想写了，现在可以在笔记本里问，json里看结果了
