import os
import time
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
email = os.getenv("ADMIN_USER", "")
password = os.getenv("PASSWORD", "")


@pytest.fixture
def login(page: Page):
    """Test that a user can log in successfully with valid credentials."""
    page.goto(f"{BASE}")
    page.get_by_label("Email").fill(email)
    page.locator("[data-test='input-password']").fill(password)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_load_state("networkidle")
    yield page

    

def validate_login_page(page: Page) -> bool:
    try:
        expect(page).to_have_url("https://sv-students-recommend.onrender.com/pages/login.html")
        expect(page).to_have_title("Login - SV Students Recommend")
        return True
    except AssertionError:
        return False


@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.logout
def test_logout_success(login: Page):
    """Test that a user can log out successfully after logging in."""
    page = login
    page.locator("[data-test='nav-logout']").click()
    assert validate_login_page(page), "Logout validation failed: URL or title did not match expected login page"