
import re
from playwright.sync_api import Page, expect
import pytest


@pytest.fixture(scope="function")
def login_as_admin(page: Page):
    page.goto("https://sv-students-recommend.onrender.com/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Login"))
    
    page.locator("[data-test='input-email']").fill("hagai@svcollege.co.il")
    page.locator("[data-test='input-password']").fill("test1234")
    page.get_by_role("button", name="Sign In").click()
    
    expect(page).to_have_url(re.compile("home.html"), timeout=5000)
    expect(page.locator("[data-test='nav-system']")).to_be_visible()
    yield page
    

def test_admin_login(login_as_admin):
    page = login_as_admin
    
    page.get_by_role("img", name="The Shawshank Redemption 2").click()
    expect(page.locator("[data-test=\"btn-delete-recommendation\"]")).to_be_visible()
    page.locator("[data-test=\"btn-delete-recommendation\"]").click()
    page.locator("[data-test=\"btn-cancel-delete\"]").click()

