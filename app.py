from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store remedies submitted by users
user_remedies = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/remedies')
def remedies():
    return render_template('remedies.html')


@app.route('/archive', methods=['GET', 'POST'])
def archive():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_remedies.append({'name': name, 'description': description})
        return redirect(url_for('archive'))
    return render_template('archive.html', remedies=user_remedies)

if __name__ == '__main__':
    app.run(debug=True)
    