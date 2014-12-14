from flask import Flask, request, jsonify
from question_classification.bayesian_classifier import find_eat_indicating_phrase
from question_classification.classifier import QCClassifier


def main(args=[]):
    app = Flask(__name__)
    classifier = QCClassifier()

    @app.route("/api/classify", methods=["POST"])
    def post_class():
        sentence = request.json["sentence"]
        out = classifier.classify(sentence)
        return jsonify({"sentence": sentence, "class": out})

    @app.route("/api/indicate_eat", methods=["POST"])
    def post_eat():
        sentence = request.json["sentence"]
        clazz = request.json["class"]
        out = find_eat_indicating_phrase(sentence, clazz)
        return jsonify({"sentence": sentence, "class": clazz, "indicator": out})

    app.run(host="", port=11112, debug=True)