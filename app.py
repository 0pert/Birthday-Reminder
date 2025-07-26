from flask import Flask, render_template, redirect, url_for, request
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix
from src.bday.bday_list import BdayList

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)

app.config["APPLICATION_ROOT"] = "/bday"

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


@app.route("/")
def root():
    bday_list = BdayList.from_json()
    print(url_for("static", filename="styles/style.css"))
    bday_list.sort_dates()
    return render_template("index.html", bday_list=bday_list)


@app.route("/add_form")
def add_form():
    return render_template("add_form.html")


@app.route("/add_birthday", methods=["POST"])
def add_birthday():
    """Add birtday"""
    bday_list = BdayList.from_json()
    bday_list.add(request.form["name"], request.form["date"])
    bday_list.save_to_file()

    return redirect(url_for("root"))


@app.route("/edit/<person>", methods=["POST", "GET"])
def edit_form(person):
    """Edit form birthday"""
    bday_list = BdayList.from_json()
    for per in bday_list.people:
        if per.name == person:
            person_obj = per

    return render_template(
        "edit_form.html", name=person_obj.name, birth=str(person_obj.date_of_birth)[:10]
    )


@app.route("/remove/<person>", methods=["POST", "GET"])
def remove(person):
    """Remove"""
    bday_list = BdayList.from_json()
    for per in bday_list.people:
        if per.name == person:
            person_obj = per

    bday_list.remove(person_obj.name)
    bday_list.save_to_file()

    return redirect(url_for("root"))


if __name__ == "__main__":
    # app.run(debug=False, port=8080)
    serve(app, host="127.0.0.1", port=8080)
