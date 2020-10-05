from flask import Flask, request, jsonify
import json

app = Flask(__name__)

mock = [
    {
        "id": 1,
        "name": "Mercy Corps",
        "e-mail": "mercy@gmail.com",
        "whatsapp": "12345678", 
        "location": "Brazil"
    },
    {
        "id": 2,
        "name": "Cure Violence",
        "e-mail": "cure@gmail.com",
        "whatsapp": "89345678", 
        "location": "USA"
    },
    {
        "id": 3,
        "name": "CARE International",
        "e-mail": "care@gmail.com",
        "whatsapp": "54345678", 
        "location": "Brazil"
    },
    {
        "id": 4,
        "name": "Ceres",
        "e-mail": "ceres@gmail.com",
        "whatsapp": "99945678", 
        "location": "Canada"
    }
]

@app.route('/hellojson')
def hellojson():
    return jsonify({
        'nome': 'ze do gas',
        'e-mail': 'ze@gmail.com'
    })

@app.route('/ongs')
def list_all_ong():
    return jsonify(mock)

@app.route('/ongs/<string:location>')
def ong_by_location(location):
    list_ong_by_location = [ong for ong in mock if ong['location'].lower() == location.lower()]
    return jsonify(list_ong_by_location)

@app.route('/ongs/<int:id>')
def ong_by_id(id):
    for ong in mock:
        if ong['id'] == id:
            return jsonify(ong), 200
    return jsonify({'error': 'ONG not found'}), 404

@app.route('/ongs', methods = ['POST'])
def save_ong():
    ong = request.get_json()

    mock.append(ong)
    print('ONG saved successfully!')
    return jsonify(ong), 201

@app.route('/ongs/<int:id>', methods =['PUT'])
def alter_ong(id):
    for ong in mock:
        if ong['id'] == id:
            altered_ong = request.get_json();
            altered_ong['id'] = id

            mock.remove(ong)
            mock.append(altered_ong)

            return jsonify(altered_ong), 200
    return jsonify({'error': 'ONG not found'}), 404

@app.route('/ongs/<int:id>', methods =['DELETE'])
def delete_ong(id):
    for ong in mock:
        if ong['id'] == id:
            mock.remove(ong)
            return ({'success': 'ONG deleted successfully'})
    return jsonify({'error': 'ONG not found'}), 404


app.run(debug=True)