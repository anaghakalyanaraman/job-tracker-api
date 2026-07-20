from conftest import client


#1 test_health
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status" : "ok"}

#2 test_register_user
def test_register_user():
    response = client.post("/auth/register", json = {"name": "Anagha","email":"anagha@gmail.com", "password":"password123"})
    assert response.status_code == 200
    assert response.json()["email"] == "anagha@gmail.com"

#3 test_register_duplicate_email
def test_register_duplicate_email():
    response = client.post("/auth/register", json={"name": "Anagha","email":"anagha@gmail.com", "password":"password123"})
    assert response.status_code == 409

#4 test_login_success
def test_login_success():
    response = client.post("/auth/login", data = {"username":"anagha@gmail.com", "password":"password123"})
    assert response.status_code == 200
    assert response.json()["access_token"] 

#5 test_login_wrong_password
def test_login_wrong_password():
    response = client.post("/auth/login", data = {"username":"anagha@gmail.com", "password":"password321"})
    assert response.status_code == 401

#6 test_get_users_me
def test_get_users_me():
    response = client.post("/auth/register", json={"name": "Banagha","email":"banagha@gmail.com", "password":"password123"})
    login_response = client.post("/auth/login", data = {"username":"banagha@gmail.com", "password":"password123"})
    token = login_response.json()["access_token"]
    response = client.get("/users/me", headers= {"Authorization" : f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "banagha@gmail.com"
    
#7 test_get_users_me_no_token
def test_get_users_me_no_token():
    response = client.get("/users/me")
    assert response.status_code == 401

#8 test_get_user_not_found
def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404