from playwright.sync_api import Page, expect
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BASE_URL", "")
email = os.getenv("ADMIN_USER", "")
non_admin_email = os.getenv("NON_ADMIN","")
password = os.getenv("PASSWORD", "")


@pytest.fixture
def get_into_site(page: Page):
    page.goto(BASE)
    yield page

    
    
def test_validate_admin_have_system_options(get_into_site):
    """As an admin I will expect that after login the system menu will be visable"""
    
    page = get_into_site
    
    page.locator("[data-test='input-email']").fill(email)
    page.locator("[data-test='input-password']").fill(password)
    page.get_by_role("button", name="Sign In").click()
    page.locator("[data-test='nav-system']").click()
    
    # expect(page).to_have_title("System – SV Students Recommend")
    expect(page.get_by_role("heading", name="System Management")).to_be_visible()

def test_validate_non_admin_does_not_have_system_options(get_into_site):
    """As an non admin I will expect that after login the system menu will NOT be visable"""
    page = get_into_site

    page.fill("css=#email", non_admin_email)
    page.locator("[data-test='input-password']").fill(password)
    page.click("xpath=//form[@id='loginForm']/button")
    
    expect(page.get_by_role("link", name="System")).not_to_be_visible()