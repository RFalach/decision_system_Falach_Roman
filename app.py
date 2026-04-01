from flask import Flask, render_template, request, redirect
from data import *
from service import calculate_scores

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():
    alternatives = get_alternatives()
    criteria = get_criteria()
    evaluations = get_evaluations()

    scores = calculate_scores(alternatives, criteria, evaluations)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    result = []
    for alt_id, score in sorted_scores:
        alt = next(a for a in alternatives if a["_id"] == alt_id)
        result.append({
            "name": alt["name"],
            "score": round(score, 3)
        })

    return render_template("results.html", result=result)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        performance = float(request.form["performance"])
        battery = float(request.form["battery"])
        weight = float(request.form["weight"])

        alt_id = add_alternative(name)

        add_evaluation(alt_id, 1, price)
        add_evaluation(alt_id, 2, performance)
        add_evaluation(alt_id, 3, battery)
        add_evaluation(alt_id, 4, weight)

        return redirect("/results")

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
