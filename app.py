import os
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow

from flask_sqlalchemy import SQLAlchemy
import json

##FEITO UTILIZANDO FLASK_SQLALCHEMY
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
    __tablename__ = 'ongs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    whatsapp = db.Column(db.String(100))
    location = db.Column(db.String(100))
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'),nullable=False)

    def __repr__(self):
        return f'Ong(id={self.id}, name={self.name}, email={self.email}, incident_id={self.incident_id})'

class OngSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OngModel

class IncidentModel(db.Model):
    __tablename__ = 'incidents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    value = db.Column(db.Integer)
    ong = db.relationship('OngModel', backref='incidents', uselist=False)

    def __repr__(self):
        return f'Incident(title={self.title}, value={self.value})'

class IncidentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IncidentModel

# init Schema
ong_schema = OngSchema()
ongs_schema = OngSchema(many=True)
incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)


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

    incidentDefault = IncidentModel(title='teste', description='descricaao', value='20', ong=ong)

    db.session.add(ong)
    db.session.add(incidentDefault)
    db.session.commit()
    print('ONG saved successfully!')
    print(ong)
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
