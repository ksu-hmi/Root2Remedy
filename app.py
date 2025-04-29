# Import necessary libraries
from flask import Flask, render_template, request, redirect
import json
import os
import html

# Initialize the Flask app
app = Flask(__name__)

# Helper function to load remedies from a JSON file
def load_remedies():
    if os.path.exists('remedies.json'):
        with open('remedies.json', 'r') as file:
            return json.load(file)
    else:
        return []

# Helper function to save remedies to a JSON file
def save_remedies(remedies):
    with open('remedies.json', 'w') as file:
        json.dump(remedies, file, indent=4)

# Load existing remedies when the app starts
user_remedies = load_remedies()

# Route for the Home Page (User submission form)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Create a new remedy entry from user input
        remedy = {
            'name': html.escape(request.form['name']),
            'story': html.escape(request.form['story']),
            'ritual': html.escape(request.form['ritual']),
            'symptoms': html.escape(request.form['symptoms']),
            'cultural': html.escape(request.form['cultural']),
            'dosage': html.escape(request.form['dosage'])
        }
        # Add remedy to the list and save to JSON file
        user_remedies.append(remedy)
        save_remedies(user_remedies)
        return redirect('/thankyou')
    return render_template('home.html')

# Route for the Archive Page (View all remedies)
@app.route('/archive')
def archive():
    return render_template('archive.html', remedies=user_remedies)

# Route for the Thank You Page (after submission)
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

# Route for the Symptom-Based Search Page
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        query = request.form['query'].lower()
        # Find remedies that match the symptom query
        results = [remedy for remedy in user_remedies if query in remedy['symptoms'].lower()]
    return render_template('search.html', results=results)

# Route for the Disclaimer Page
@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
