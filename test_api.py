import requests

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    print(f"[health] status={r.status_code}, body={r.json()}")

def test_register():
    r = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={
            "username": "testuser",
            "password": "TestPass123",
            "email": "test@example.com",
            "full_name": "Test User"
        }
    )
    print(f"[register] status={r.status_code}, body={r.json()}")
    return r.json()

def test_login():
    r = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "TestPass123"
        }
    )
    print(f"[login] status={r.status_code}, body={r.json()}")
    return r.json()

if __name__ == "__main__":
    print("Testing API...")
    test_health()
    test_register()
    test_login()
