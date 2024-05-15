# tests/test_address_book.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_address():
    response = client.post(
        "/addresses/",
        json={
            "resident_name": "John Doe",
            "house_number": "123",
            "street_number": "Main St",
            "city": "Anytown",
            "state": "State",
            "country": "Country",
            "zipcode": "12345",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    )
    assert response.status_code == 200
    assert response.json()["resident_name"] == "John Doe"
