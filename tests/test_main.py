import sys
import os
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app  

client = TestClient(app) 

def test_read_sheep():
    response = client.get("/sheep/1")  
    assert response.status_code == 200  
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_read_nonexistent_sheep():
    response = client.get("/sheep/999")  
    assert response.status_code == 404  
    assert response.json() == {"detail": "Sheep not found"} 

def test_add_sheep():
    new_sheep_data = {
        "id": 7,
        "name": "Dolly",
        "breed": "Southdown",
        "sex": "ewe"
    }
    response = client.post("/sheep/", json=new_sheep_data)
    assert response.status_code == 201
    assert response.json() == new_sheep_data

    response = client.get("/sheep/7")
    assert response.status_code == 200
    assert response.json() == new_sheep_data

def test_update_sheep():
    updated_sheep_data = {
        "id": 1,
        "name": "Spice Updated",
        "breed": "Gotland",
        "sex": "ewe"
    }
    response = client.put("/sheep/1", json=updated_sheep_data)
    assert response.status_code == 200
    assert response.json() == updated_sheep_data

def test_delete_sheep():
    response = client.delete("/sheep/1") 
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice Updated",
        "breed": "Gotland",
        "sex": "ewe"
    }

    response = client.get("/sheep/1")
    assert response.status_code == 404

def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  
    assert len(response.json()) > 0  
