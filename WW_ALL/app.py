from flask import Flask, render_template, request, redirect
from database import init_db, add_person, get_people, get_schools, get_classes, get_basket, sql_examples

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    people = get_people()
    schools = get_schools()
    classes = get_classes()
    basket = get_basket()
    results = sql_examples() 
    return render_template("index.html",
                           people=people,
                           schools=schools,
                           classes=classes,
                           basket=basket,
                           results=results)

@app.route("/add_person", methods=["POST"])
def add_person_route():
    add_person(
        request.form["first_name"],
        request.form["last_name"],
        request.form["school_number"],
        request.form["class_number"],
        request.form.get("address", "")
    )
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
