import os
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow

from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ \
                os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init DB
db = SQLAlchemy(app)

# init Marshmallow
ma = Marshmallow(app)


class OngModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    whatsapp = db.Column(db.String(100))
    location = db.Column(db.String(100))

    def __init__(self, name, email, whatsapp, location):
        self.name = name
        self.email = email
        self.whatsapp = whatsapp
        self.location = location


class OngSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OngModel


# init Schema

ong_schema = OngSchema()
ongs_schema = OngSchema(many=True)


@app.route('/hellojson')
def hellojson():
    return jsonify({
        'nome': 'ze do gas',
        'email': 'ze@gmail.com'
    })

@app.route('/ongs')
def list_all_ong():
    all_ongs = OngModel.query.all()
    return jsonify(ongs_schema.dump(all_ongs))

@app.route('/ongs/<string:location>')
def ong_by_location(location):
    ongs_by_location = OngModel.query.filter_by(location=location).all()
    return jsonify(ongs_schema.dump(ongs_by_location))
    

@app.route('/ongs/<int:id>')
def ong_by_id(id):
    ong = OngModel.query.get(id)
    return ong_schema.jsonify(ong)

@app.route('/ongs', methods = ['POST'])
def save_ong():
    name = request.json.get('name', '')
    email = request.json.get('email', '')
    whatsapp = request.json.get('whatsapp', '')
    location = request.json.get('location', '')

    ong = OngModel(name=name, email=email, whatsapp=whatsapp, location=location)

    db.session.add(ong)
    db.session.commit()
    print('ONG saved successfully!')
    return ong_schema.jsonify(ong), 201
    

@app.route('/ongs/<int:id>', methods =['PUT'])
def alter_ong(id):
    ong = OngModel.query.get(id)

    name = request.json.get('name', '')
    email = request.json.get('email', '')
    whatsapp = request.json.get('whatsapp', '')
    location = request.json.get('location', '')

    ong.name = name
    ong.email = email
    ong.whatsapp = whatsapp
    ong.location = location

    db.session.add(ong)
    db.session.commit()

    print('ONG altered successfully!')
    return ong_schema.jsonify(ong)

@app.route('/ongs/<int:id>', methods =['DELETE'])
def delete_ong(id):
    ong = OngModel.query.get(id)

    db.session.delete(ong)
    db.session.commit()
    return ({'success': 'ONG deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True)
