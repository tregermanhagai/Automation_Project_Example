import os
import time
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")

_registered_user = {}


@pytest.mark.api
def test_register_new_user(playwright: Playwright):
    api = playwright.request.new_context(base_url=BASE)
    email = f"test_{int(time.time())}@example.com"
    password = "abcd12"
    res = api.post("/auth/register", data={
        "name": "Test Student", "email": email, "password": password})
    assert res.status in (200, 201), f"Register failed: {res.text()}"
    _registered_user["email"] = email
    _registered_user["password"] = password
    api.dispose()


@pytest.mark.api
def test_delete_own_account(playwright: Playwright):
    assert _registered_user, "No registered user found — run test_register_new_user first"

    api = playwright.request.new_context(base_url=BASE)

    login_res = api.post("/auth/login", data={
        "email": _registered_user["email"],
        "password": _registered_user["password"],
    })
    assert login_res.status == 200, f"Login failed: {login_res.text()}"

    body = login_res.json()
    token = body.get("access_token")
    assert token, f"No token found in login response: {body}"

    delete_res = api.delete("/api/profile/me", headers={"authorization": f"Bearer {token}"})
    assert delete_res.status == 204, f"Delete failed: {delete_res.text()}"

    api.dispose()
