from flask import Flask, request, jsonify, render_template
from question_classification.bayesian_classifier import find_eat_indicating_phrase
from question_classification.classifier import QCClassifier
from question_classification.config import classes


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

    @app.route("/index.html", methods=["GET"])
    def get_index():
        return render_template("index.html", classes=classes)

    @app.route("/classify.html", methods=["POST"])
    def post_classify():
        sentence = request.form["sentence"]
        clazz = classifier.classify(sentence)
        indicator = find_eat_indicating_phrase(sentence, clazz)
        return render_template("results.html", sentence=sentence, clazz=clazz, indicator=indicator)

    @app.route("/indicate.html", methods=["POST"])
    def post_indicate():
        sentence = request.form["sentence"]
        clazz = request.form["clazz"]
        indicator = find_eat_indicating_phrase(sentence, clazz)
        return render_template("results.html", sentence=sentence, clazz=clazz, indicator=indicator)

    app.run(host="", port=8080, debug=True)