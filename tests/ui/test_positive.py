import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
email = os.getenv("ADMIN_USER", "")
password = os.getenv("PASSWORD", "")


@pytest.mark.ui
def test_login_success(page: Page):
    page.goto(f"{BASE}")
    page.get_by_label("Email").fill(email)
    page.locator("[data-test='input-password']").fill(password)
    page.get_by_role("button", name="Sign In").click()
    expect(page).to_have_url(f"{BASE}/pages/home.html", timeout=15000)
    expect(page.locator("[data-test='nav-system']")).to_be_visible()
    expect(page.get_by_role("link", name="Logout")).to_be_visible()