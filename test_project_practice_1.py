from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BASE_URL", "")
email = os.getenv("ADMIN_USER", "")
password = os.getenv("PASSWORD", "")


def test_validate_admin_have_system_options(page: Page):
    """As an admin I will expect that after login the system menu will be visable"""
    
    page.goto(BASE)
    page.locator("[data-test='input-email']").fill(email)
    page.locator("[data-test='input-password']").fill(password)
    page.get_by_role("button", name="Sign In").click()
    page.locator("[data-test='nav-system']").click()
    
    # expect(page).to_have_title("System – SV Students Recommend")
    expect(page.get_by_role("heading", name="System Management")).to_be_visible

   