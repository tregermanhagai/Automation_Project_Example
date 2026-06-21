import os
import time
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright

from tests.api.test_api_sanity import test_add_recommendation

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
STUDENT_EMAIL = os.getenv("STUDENT_USER")
STUDENT_PASSWORD = os.getenv("STUDENT_PASSWORD")

_data_user = {}


@pytest.fixture
def auth_token(playwright: Playwright) -> str:
    """Log in as a student, store the Bearer token in _data_user, and return it."""
    api = playwright.request.new_context(base_url=BASE)
    res = api.post("/auth/login", data={
        "email": STUDENT_EMAIL,
        "password": STUDENT_PASSWORD,
    })
    assert res.status == 200, f"Login failed: {res.text()}"
    token = res.json().get("access_token")
    assert token, "No access_token in login response"
    _data_user["token"] = token
    api.dispose()
    return token


@pytest.fixture
def add_recommendation(playwright: Playwright, auth_token: str):
    """Verify that an authenticated user can add a recommendation with all fields via POST /api/recommendations.
    Expects a 201 response."""

    api = playwright.request.new_context(base_url=BASE)

    res = api.post(
        "/api/recommendations",
        headers={"authorization": f"Bearer {auth_token}"},
        multipart={
            "name": "Class 20 - Test Reommendations",
            "category": "Book",
            "description": "A classic book on software craftsmanship.",
            "recommender_name": "API Tester",
            "website_link": "https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/",
        },
    )

    assert res.status == 201, f"Add recommendation failed: {res.text()}"

    body = res.json()
    assert "id" in body, "Missing 'id' in response"
    assert body["name"] == "Class 20 - Test Reommendations"
    assert body["category"] == "Book"
    _data_user["rec_id"] = body["id"]
    
    return body["id"]

    api.dispose()


@pytest.mark.api_sanity_negative
def test_delete_recommendation_negative_no_token(playwright: Playwright, auth_token: str, add_recommendation: str):
    """Verify that an authenticated user cannot delete a recommendation without a token via DELETE /api/recommendations/{rec_id}.
    Expects a 401 response. Depends on add_recommendation having run first."""
    assert "rec_id" in _data_user, "No rec_id found — run add_recommendation first"

    api = playwright.request.new_context(base_url=BASE)

    rec_id = add_recommendation
    res = api.delete(
        f"/api/recommendations/{rec_id}",
        headers={"authorization": f"Bearer 123456789"},  # Invalid token
    )

    assert res.status == 401, f"Delete recommendation should have failed with 401, but got: {res.status}"
    assert res.json().get("detail") == "Invalid or expired token. Please log in again.", f"Delete recommendation should have failed with 'Invalid token', but got: {res.json().get('detail')}"

    api.dispose()


@pytest.mark.api_sanity
def test_delete_recommendation(playwright: Playwright, auth_token: str):
    """Verify that an authenticated user can delete a recommendation via DELETE /api/recommendations/{rec_id}.
    Expects a 204 response. Depends on test_add_recommendation having run first."""
    assert "rec_id" in _data_user, "No rec_id found — run test_add_recommendation first"

    api = playwright.request.new_context(base_url=BASE)

    rec_id = _data_user["rec_id"]
    res = api.delete(
        f"/api/recommendations/{rec_id}",
        headers={"authorization": f"Bearer {auth_token}"},
    )

    assert res.status == 204, f"Delete recommendation failed: {res.text()}"

    api.dispose()

