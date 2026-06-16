import os
import time
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright

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


@pytest.mark.api
def test_register_new_user(playwright: Playwright):
    
    """Verify that a new user can successfully register via the /auth/register endpoint.
    Expects  201 response and stores the credentials for use in subsequent tests."""
    
    api = playwright.request.new_context(base_url=BASE)
    email = f"test_{int(time.time())}@example.com"
    password = "abcd12"
    
    res = api.post("/auth/register", data={
        "name": "Test Student", "email": email, "password": password})
    
    assert res.status == 201, f"Register failed: {res.text()}"
    _data_user["email"] = email
    _data_user["password"] = password
    api.dispose()


@pytest.mark.api
def test_delete_own_account(playwright: Playwright):
    """Verify that a logged-in user can delete their own account via DELETE /api/profile/me.
    Logs in with previously registered credentials, obtains a Bearer token, and expects a 204 response."""
    assert _data_user, "No registered user found — run test_register_new_user first"

    api = playwright.request.new_context(base_url=BASE)

    login_res = api.post("/auth/login", data={
        "email": _data_user["email"],
        "password": _data_user["password"],
    })
    assert login_res.status == 200, f"Login failed: {login_res.text()}"

    body = login_res.json()
    token = body.get("access_token")
    assert token, f"No token found in login response: {body}"

    delete_res = api.delete("/api/profile/me", headers={"authorization": f"Bearer {token}"})
    assert delete_res.status == 204, f"Delete failed: {delete_res.text()}"

    api.dispose()


@pytest.mark.api
def test_get_recommendations(playwright: Playwright):
    """Verify that the /api/recommendations endpoint returns a 200 status code and a valid response body."""

    api = playwright.request.new_context(base_url=BASE)

    res = api.get("/api/recommendations", params={"category": "Book", "page": 1, "limit": 10})

    assert res.status == 200, f"Failed: {res.text()}"

    body = res.json()
    assert isinstance(body, list), f"Expected a list, got: {type(body)}"
    assert len(body) > 0, "Expected at least one recommendation"

    first = body[0]
    assert "id" in first, "Missing 'id' field"
    assert "name" in first, "Missing 'name' field"
    assert "category" in first, "Missing 'category' field"
    assert "recommender_name" in first, "Missing 'recommender_name' field"
    assert "comment_count" in first, "Missing 'comment_count' field"
    assert all(item["category"] == "Book" for item in body), "Not all results have category 'Book'"

    api.dispose()


@pytest.mark.api_sanity
def test_add_recommendation(playwright: Playwright, auth_token: str):
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

    api.dispose()



@pytest.mark.api_sanity
def test_add_comment(playwright: Playwright, auth_token: str):
    """Verify that an authenticated user can add a comment to a recommendation via POST /api/recommendations/{rec_id}/comments.
    Expects a 201 response. Depends on test_add_recommendation having run first."""
    

    api = playwright.request.new_context(base_url=BASE)

    rec_id = _data_user["rec_id"]
    res = api.post(
        f"/api/recommendations/{rec_id}/comments",
        headers={"authorization": f"Bearer {auth_token}"},
        data={
            "rating": 5,
            "comment": "This is a test comment."
        },
    )
    body = res.json()
    print(f"Add comment response: {body}")
    assert res.status == 201, f"Add comment failed: {res.text()}"
    assert body["commenter_name"] == "Hagai Tregerman"
    api.dispose()








# @pytest.mark.api_sanity
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

