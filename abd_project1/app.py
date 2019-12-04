from datetime import date, datetime

from flask import Flask, render_template, redirect, url_for, request, session

from db_access import DbAccess
from db_connection import DbConnection

app = Flask(__name__)
app.secret_key = 'super secret key'

DbConnection = DbConnection()
dbAccess = DbAccess()


@app.route("/")
def main():
    return redirect(url_for('logowanie'))


@app.route("/logowanie", methods=['GET', 'POST'])
def logowanie():
    error = None

    if request.method == 'POST':
        kronikarz = dbAccess.get_user_by_email(request.form['email'])
        if kronikarz is not None:
            if request.form['password'] != kronikarz.haslo:
                error = 'Spróbuj ponownie'
            else:
                session['id'] = kronikarz.nr_indeksu
                return redirect(url_for('profil'))
        else:
            error = 'Spróbuj ponownie'
    return render_template('logowanie.html', error=error)


@app.route("/profil")
def profil():
    if session['id'] is not None:
        kronikarz = dbAccess.get_user_data()
        return render_template("profil.html", kronikarz=kronikarz)
    return redirect(url_for('logowanie'))


@app.route("/zmien-dane", methods=['GET', 'POST'])
def zmien_dane():
    if session['id'] is not None:
        return render_template("zmien_dane.html")
    return redirect(url_for('logowanie'))


@app.route("/wnioski")
def wnioski():
    if session['id'] is not None:
        redaktor_naczelny = dbAccess.is_user_redaktor_naczelny(session['id'])
        if redaktor_naczelny:
            wniosek_kronikarz_list = dbAccess.get_all_actual_wnioski()
        else:
            wniosek_kronikarz_list = dbAccess.get_wnioski_by_user(session['id'])
        return render_template("wnioski.html",
                               redaktor_naczelny=redaktor_naczelny,
                               len=len(wniosek_kronikarz_list),
                               wniosek_kronikarz=wniosek_kronikarz_list)
    return redirect(url_for('logowanie'))


@app.route("/wniosek-szczegoly", methods=['GET', 'POST'])
def wniosek_szczegoly():
    if session['id'] is not None:
        tresc = request.args.get('tresc')
        rodzaj = request.args.get('rodzaj')
        return render_template("wniosek_szczegoly.html", rodzaj=rodzaj, tresc=tresc)
    return redirect(url_for('logowanie'))


@app.route("/wniosek-rozpatrz", methods=['GET', 'POST'])
def wniosek_rozpatrz():
    if session['id'] is not None:
        if request.method == 'GET':
            tresc = request.args.get('tresc')
            rodzaj = request.args.get('rodzaj')
            imie = request.args.get('imie')
            nazwisko = request.args.get('nazwisko')
            id = request.args.get('id_wniosku')
            return render_template("wniosek_rozpatrz.html", tresc=tresc, rodzaj=rodzaj,
                                   imie=imie, nazwisko=nazwisko, id=id)
        else:
            id = request.form['id']
            if 'akceptuj' in request.form:
                print("akceptuj")
                dbAccess.accept_wniosek(id)
            else:
                print("odrzuc")
                dbAccess.reject_wniosek(id)
            return redirect(url_for('wnioski'))
    return redirect(url_for('logowanie'))


@app.route("/zloz-wniosek", methods=['GET', 'POST'])
def zloz_wniosek():
    if session['id'] is not None:
        if request.method == 'GET':
            return render_template("zloz_wniosek.html")
        dbAccess.add_wniosek(request.form['rodzaj'], request.form['tresc'], session['id'])
        return redirect(url_for('wnioski'))
    return redirect(url_for('logowanie'))


@app.route("/wydarzenia")
def wydarzenia():
    if session['id'] is not None:
        wydarzenia_list = dbAccess.get_wydarzenia_by_user(session['id'])
        return render_template("wydarzenia.html", len=len(wydarzenia_list), wydarzenia=wydarzenia_list)
    return redirect(url_for('logowanie'))


@app.route("/utworz-wydarzenie", methods=['GET', 'POST'])
def utworz_wydarzenie():
    if session['id'] is not None:
        if request.method == 'GET':
            if dbAccess.is_user_redaktor_organizacyjny(session['id']):
                return render_template("utworz_wydarzenie.html")
        else:
            rodzaj = request.form['rodzaj']
            data = request.form['data']
            godz_rozp = datetime.strptime(request.form['godz_rozp'], '%H:%M')
            godz_zako = datetime.strptime(request.form['godz_zako'], '%H:%M')
            opis = request.form['opis']
            dbAccess.add_wydarzenie(rodzaj, data, godz_rozp, godz_zako, opis)
    return redirect(url_for('logowanie'))


@app.route("/zadania-do-rozdzielenia")
def zadania_do_rozdzielenia():
    if session['id'] is not None:
        if dbAccess.is_user_redaktor_naczelny(session['id']):
            task_list = dbAccess.get_zadania_to_assign()
            kronikarz_zad_amount = dbAccess.get_aktualne_zadania_amount_by_user()
            return render_template("zadania_do_rozdzielenia.html",
                                   kronikarze_count=len(kronikarz_zad_amount),
                                   kronikarz_zad_amount=kronikarz_zad_amount,
                                   len=len(task_list),
                                   zadania=task_list)
    return redirect(url_for('logowanie'))


@app.route("/zadania-do-rozdzielenia-szczegoly", methods=['GET', 'POST'])
def zadania_do_rozdzielenia_szczegoly():
    if session['id'] is not None:
        if request.method == 'GET':
            data = request.args.get('data')
            rodzaj = request.args.get('rodzaj')
            opis = request.args.get('opis')
            id = request.args.get('id')
            return render_template("zadania_do_rozdzielenia_szczegoly.html", rodzaj=rodzaj, data=data, opis=opis, id=id)
        else:
            id_zadania = int(request.form['id'])
            data = datetime.strptime(request.form['data'], '%Y-%m-%d')
            user1 = request.form['user1']
            user2 = request.form['user2']
            user3 = request.form['user3']

            print(data)
            print(id_zadania)
            dbAccess.match_kronikarze_zadanie(id_zadania, data, (user1, user2, user3))

            return redirect(url_for('zadania_do_rozdzielenia'))
    return redirect(url_for('logowanie'))


@app.route("/zadania-przydzielone")
def zadania_przydzielone():
    if session['id'] is not None:
        task_list = dbAccess.get_zadania_by_user(session['id'])
        return render_template("zadania_przydzielone.html",
                               len=len(task_list),
                               zadania=task_list)
    return redirect(url_for('logowanie'))


@app.route("/zadania-przydzielone-szczegoly", methods=['GET', 'POST'])
def zadania_przydzielone_szczegoly():
    if session['id'] is not None:
        data = request.args.get('data')
        rodzaj = request.args.get('rodzaj')
        opis = request.args.get('opis')
        return render_template("zadania_przydzielone_szczegoly.html", rodzaj=rodzaj, data=data, opis=opis)
    return redirect(url_for('logowanie'))


if __name__ == "__main__":
    DbConnection.engine.connect()
    DbConnection.Model.metadata.create_all(bind=DbConnection.engine)

    app.run(debug=True)
