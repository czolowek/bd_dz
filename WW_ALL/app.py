from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_person, get_people, get_schools, get_classes

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET"])
def index():
    people = get_people()
    schools = get_schools()
    classes = get_classes()
    return render_template("index.html", people=people, schools=schools, classes=classes)

@app.route("/add_person", methods=["POST"])
def add_person_route():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    school_number = request.form.get("school_number", "").strip()
    class_number = request.form.get("class_number", "").strip()
    address = request.form.get("address", "").strip()

    if first_name == "" or last_name == "":
        return redirect(url_for("index"))

    add_person(first_name, last_name, school_number or None, class_number or None, address or None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
