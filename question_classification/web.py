from flask import Flask, request, jsonify
from question_classification.classifier import QCClassifier


def main(args=[]):
    app = Flask(__name__)
    classifier = QCClassifier()

    @app.route("/api/classify", methods=["POST"])
    def post_class():
        sentence = request.json()["sentence"]
        out = classifier.classify(sentence)
        return jsonify({"sentence": sentence, "class": out})

    app.run(host="", port=8080, debug=True)