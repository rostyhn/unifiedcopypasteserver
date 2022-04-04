from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# TODO: write tests for clipboards existing
def test_no_clipboards_exist():
    pass

def test_create_insecure_clipboard():
    response = client.post("/api/create_clipboard/test",
                           json={"contents": "supplied contents"})    
    assert response.status_code == 201


def test_create_secure_clipboard():
    response = client.post("/api/create_clipboard/test_secure",
                           json={"contents": "supplied contents",
                                 "passphrase": "super_secret"})    
    assert response.status_code == 201


def test_duplicate_clipboard():
    response = client.post("/api/create_clipboard/test",
                           json={"contents": "supplied contents",
                                 "passphrase": "super_secret"})
    assert response.status_code == 403
    

def test_get_real_insecure_clipboard():
    response = client.post("/api/get_clipboard/test", json={"passphrase": ""})
    assert response.status_code == 200
    assert response.content == b'"supplied contents"'


def test_get_real_insecure_clipboard_with_pass():
    response = client.post("/api/get_clipboard/test",
                          json={"passphrase": "no need"}
                          )
    assert response.status_code == 200
    assert response.content == b'"supplied contents"'

    
def test_get_real_secure_clipboard():
    response = client.post("/api/get_clipboard/test_secure",
                          json={"passphrase": "super_secret"}
                          )
    assert response.status_code == 200
    assert response.content == b'"supplied contents"'

def test_fail_get_real_secure_clipboard():
    response = client.post("/api/get_clipboard/test_secure",
                          json={"passphrase": "wrong_secret"}
                          )
    assert response.status_code == 403

def test_fail_get_fake_secure_clipboard():
    response = client.post("/api/get_clipboard/test_noexist",
                          json={"passphrase": "wrong_secret"}
                          )
    assert response.status_code == 404

def test_change_insecure_clipboard():
   response = client.post("/api/set_clipboard/test",
                          json={"contents": "new_content"}
                          )
   assert response.status_code == 200

def test_get_real_insecure_clipboard_after_change():
    response = client.post("/api/get_clipboard/test",
                           json={"passphrase": ""})
    assert response.status_code == 200
    assert response.content == b'"new_content"'
   
def test_change_secure_clipboard():
    response = client.post("/api/set_clipboard/test_secure",
                           json={"contents": "new_content",
                                 "passphrase": "super_secret"}
                           )
    assert response.status_code == 200


def test_get_secure_clipboard_after_change():
    response = client.post("/api/get_clipboard/test_secure",
                           json={"passphrase": "super_secret"})
    assert response.status_code == 200
    assert response.content == b'"new_content"'


def test_fail_set_secure_clipboard():
    response = client.post("/api/set_clipboard/test_secure",
                           json={"contents": "new_content",
                                 "passphrase": "wrong_secret"}
                           )
    assert response.status_code == 403


def test_kill_insecure_clipboard():
    response = client.post("/api/kill_clipboard/test",
                           json={"passphrase": ""})
    assert response.status_code == 200


def test_fail_get_dead_clipboard():
    response = client.post("/api/get_clipboard/test",
                          json={"passphrase": ""})
    assert response.status_code == 404


def test_fail_kill_secure_clipboard():
    response = client.post("/api/kill_clipboard/test_secure",
                           json={"passphrase": ""})
    assert response.status_code == 403


def test_kill_secure_clipboard():
    response = client.post("/api/kill_clipboard/test_secure",
                           json={"passphrase": "super_secret"})
    assert response.status_code == 200
