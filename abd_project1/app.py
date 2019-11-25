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
    return redirect(url_for(''))



@app.route("/zmien-dane", methods=['GET', 'POST'])
def zmien_dane():
    if session['id'] is not None:
        return render_template("zmien_dane.html")
    return render_template('logowanie.html')


@app.route("/wnioski")
def wnioski():
    if session['id'] is not None:
        redaktor_naczelny = dbAccess.is_user_redaktor_naczelny()
        if redaktor_naczelny:
            wniosek_kronikarz_list = dbAccess.get_all_actual_wnioski()
        else:
            wniosek_kronikarz_list = dbAccess.get_wnioski_by_user(session['id'])
        return render_template("wnioski.html", redaktor_naczelny=redaktor_naczelny, len=len(wniosek_kronikarz_list), wniosek_kronikarz=wniosek_kronikarz_list)
    return redirect(url_for(''))


@app.route("/zloz-wniosek", methods=['GET', 'POST'])
def zloz_wniosek():
    if session['id'] is not None:
        if request.method == 'GET':
            return render_template("zloz_wniosek.html")
        dbAccess.add_wniosek(request.form['rodzaj'], request.form['tresc'], session['id'])
        return redirect(url_for('wnioski'))
    return redirect(url_for(''))


@app.route("/wydarzenia")
def wydarzenia():
    if session['id'] is not None:
        wydarzenia_list = dbAccess.get_wydarzenia_by_user()
        return render_template("wydarzenia.html", len=len(wydarzenia_list), wydarzenia=wydarzenia_list)
    return redirect(url_for(''))


@app.route("/utworz-wydarzenie", methods=['GET', 'POST'])
def utworz_wydarzenie():
    if session['id'] is not None:
        return render_template("utworz_wydarzenie.html")
    return redirect(url_for('logowanie'))


@app.route("/zadania-do-rozdzielenia")
def zadania_do_rozdzielenia():
    if session['id'] is not None:
        if dbAccess.is_user_redaktor_naczelny():
            task_list = dbAccess.get_zadania_to_assign()

            return render_template("zadania_do_rozdzielenia.html", len=len(task_list), zadania=task_list)
    return redirect(url_for(''))


@app.route("/zadania-przydzielone")
def zadania_przydzielone():
    if session['id'] is not None:
        task_list = dbAccess.get_zadania_by_user(session['id'])
        aktualne_zadania_count = dbAccess.get_aktualne_zadania_amount_by_user(session['id'])
        return render_template("zadania_przydzielone.html",
                               aktualne_zadania_count=aktualne_zadania_count,
                               len=len(task_list),
                               zadania=task_list)
    return redirect(url_for(''))


if __name__ == "__main__":
    DbConnection.engine.connect()
    DbConnection.Model.metadata.create_all(bind=DbConnection.engine)

    app.run(debug=True)
