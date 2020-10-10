from httpx import get, post

url_base = 'http://127.0.0.1:5000/ongs'


def test_ongs_must_return_status200_when_receive_get():
    request = get(url_base)
    assert request.status_code == 200

ong_valid = {'name': 'Ong Vicente', 'email': 'vicente@gmail.com', 'whatsapp': '12341234', 'location': 'Brazil'}
def test_insert_ong_json_valid_gets_201():
    request = post(url_base, json=ong_valid)
    assert request.status_code == 201