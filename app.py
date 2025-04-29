from flask import Flask, render_template, request, redirect, url_for

import json
import os
import html

app = Flask(__name__)

def load_remedies():
    if os.path.exists('remedies.json'):
        with open('remedies.json', 'r') as file:
            return json.load(file)
    else:
        return []

def save_remedies(remedies):
    with open('remedies.json', 'w') as file:
        json.dump(remedies, file, indent=4)

user_remedies = load_remedies() # Storage for user remedies
def load_remedies():
    if os.path.exists('remedies.json'):
        with open('remedies.json', 'r') as file:
            return json.load(file)
    else:
        return []

def save_remedies(remedies):
    with open('remedies.json', 'w') as file:
        json.dump(remedies, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        remedy = {
            'name': request.form['name'],
            'story': request.form['story'],
            'ritual': request.form['ritual'],
            'symptoms': request.form['symptoms'],
            'cultural': request.form['cultural'],
            'dosage': request.form['dosage']
        }
        user_remedies.append(remedy)
        save_remedies(user_remedies)
        return redirect('/thankyou')  # <-- Redirect to thankyou page
    return render_template('home.html')

@app.route('/remedies')
def remedies():
    return render_template('remedies.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        query = request.form['query'].lower()
        results = [remedy for remedy in user_remedies if query in remedy['symptoms'].lower()]
    return render_template('search.html', results=results)

@app.route('/archive')
def archive():
    return render_template('archive.html', remedies=user_remedies)

if __name__ == '__main__':
    app.run(debug=True)
