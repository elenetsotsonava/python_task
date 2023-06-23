from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import random


app = Flask(__name__)
app.secret_key = "adfadf adfadf33adf"

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

class Animal(db.Model):
    __tablename__ = 'animal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    animal_type = db.Column(db.String(100))


def get_animal_data(name):
    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
    response = requests.get(
        api_url, headers={"X-Api-Key": "CK7M7pL0Wa5Ppbeaqc2MzA==Ypcid2s6zSFWmY1T"})
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random_animal')
def animals():
    animal_names = ['Sloth', 'Tiger', 'Hawk', 'Finch', 'Swan',
                    'Dingo', 'Gull', 'Puma', 'Toad', 'Moth', 'Bison']

    random_animal = random.choice(animal_names)

    animal_data = get_animal_data(random_animal)

    print(animal_data[0])

    return render_template('random_animal.html', animal=animal_data[0])

@app.route('/search_animal', methods=["GET", "POST"])
def search_animal():
    if request.method == 'POST':
        query = request.form.get('search_query')

        return redirect(url_for('search_results', query=query))
    else:
        return render_template('search_animal.html')


@app.route('/search_results')
def search_results():
    query = request.args.get('query')
    data = get_animal_data(query)

    print(f"Animal data {data}")

    if data is None or len(data) == 0:
        flash('No results found for the search query: {}'.format(query))
        return redirect(url_for('search_animal'))
    else:
        return render_template('search_results.html', animal=data[0])


@app.route('/animal_types')
def animal_types():
    types = db.session.query(Animal.animal_type).distinct().all()
    return render_template('animal_types.html', types=types)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
