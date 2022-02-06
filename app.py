"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, flash, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret_cupcake'
app.debug = False
# toolbar = DebugToolbarExtension(app)

# to turn off the Debug Toolbar redirects explicitly just uncomment the line below:
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


#################### cupcakes routes #############################

@app.route('/')
def root():
    '''Display homepage'''

    return render_template('index.html')


@app.route('/api/cupcakes')
def list_cupcakes():
    '''Returns JSON with all the cupcakes'''

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(cupcake_id):
    '''Return JSON for a cupcake based on it's id'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Create a new cupcake and return JSON of the created cupcake.'''

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()), 201)



@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''Update cupcake from database, then return updated data.'''

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    '''Delete a specific cupcake based on it's id and display a message in JSON.'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Cupcake Deleted')











