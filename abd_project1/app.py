from flask import Flask, render_template, redirect, url_for, request, session

from db_access import DbAccess
from db_connection import DbConnection

app = Flask(__name__)
app.secret_key = 'super secret key'

DbConnection = DbConnection()
dbAccess = DbAccess()


@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        kronikarz = dbAccess.get_user_by_email(request.form['email'])
        if kronikarz is not None:
            if request.form['password'] != kronikarz.haslo:
                error = 'Spróbuj ponownie'
            else:
                session['id'] = kronikarz.nr_indeksu
                return redirect(url_for('profil'))
    return render_template('logowanie.html', error=error)


@app.route("/profil")
def profil():
    if session['id'] is not None:
        kronikarz = dbAccess.get_user_data()
        return render_template("profil.html", kronikarz=kronikarz)
    return render_template('logowanie.html')


@app.route("/zmien-dane")
def zmien_dane():
    if session['id'] is not None:
        return render_template("zmien_dane.html")
    return render_template('logowanie.html')


@app.route("/wnioski")
def wnioski():
    if session['id'] is not None:
        return render_template("wnioski.html")
    return render_template('logowanie.html')


@app.route("/zloz-wniosek")
def zloz_wniosek():
    if session['id'] is not None:
        return render_template("zloz_wniosek.html")
    return render_template('logowanie.html')


@app.route("/wydarzenia")
def wydarzenia():
    if session['id'] is not None:
        return render_template("wydarzenia.html")
    return render_template('logowanie.html')


@app.route("/utworz-wydarzenie")
def utworz_wydarzenie():
    if session['id'] is not None:
        return render_template("utworz_wydarzenie.html")
    return render_template('logowanie.html')


@app.route("/zadania-do-rozdzielenia")
def zadania_do_rozdzielenia():
    if session['id'] is not None:
        if dbAccess.is_user_redaktor_naczelny():
            task_list = dbAccess.get_task_to_assign()

            return render_template("zadania_do_rozdzielenia.html", len=len(task_list), zadania=task_list)
    return render_template('logowanie.html')


@app.route("/zadania-przydzielone")
def zadania_przydzielone():
    if session['id'] is not None:
        task_list = ["zadanie1", "zadanie2", "zadanie3"]
        return render_template("zadania_przydzielone.html", len=len(task_list), zadania=task_list)
    return render_template('logowanie.html')


if __name__ == "__main__":
    DbConnection.engine.connect()
    DbConnection.Model.metadata.create_all(bind=DbConnection.engine)

    app.run(debug=True)
