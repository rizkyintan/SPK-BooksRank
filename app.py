import os
import json

from Moora import Moora
from os import path
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'this is secret key'

@app.route('/')
def index():
    session.clear()
    if path.exists('data.json'):
        os.remove("data.json")
    return render_template('home.html')


@app.route('/fill')
def fill():
    unlock = False
    isThere = False
    if path.exists('data.json'):
        with open('data.json') as f:
            obj = json.load(f)
            if len(obj) > 1:
                unlock = True
            if len(obj) > 0:
                isThere = True
        return render_template('guest.html', unlock=unlock, condition=isThere, data=obj)
    else:
        return render_template('guest.html', unlock=unlock, condition=isThere)


@app.route('/admin')
def admin():
    session['admin'] = True
    return redirect('/fill')


@app.route('/save', methods=['POST'])
def save():
    if path.exists('data.json'):
        with open('data.json') as f:
            old_data = json.load(f)
        with open('data.json', 'w') as f:
            old_data.append(request.form)
            json.dump(old_data, f)
    else:
        with open('data.json', 'w') as f:
            data = []
            data.append(request.form)
            json.dump(data, f)

    return redirect('/fill')


@app.route('/process')
def process():
    if path.exists('data.json'):
        with open('data.json') as f:
            old_data = json.load(f)
            seller = []
            criteria = []

            for data in old_data:
                seller.append(data['seller'])
                criteria.append([float(data['prices']), int(data['condition']), int(data['rating'])])

            moora = Moora()
            moora.setData(seller, criteria)

            session['normalization'] = moora.normalizationCriteria()
            moora.setDivider()
            session['normalizationMoora'] = moora.normalizationMoora()

            tableYi = moora.optimationYi()
            session['optimationYi'] = list(zip(seller, tableYi))

            moora.setRanking()
            moora.countRanking()

            session['rankingScore'] = list(zip(moora.getRanking(), moora.getRankScore()))
            session['result'] = moora.getRanking()

    return redirect('/result')


@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
