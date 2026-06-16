from operator import contains
# from time import sleep

import pytest
from playwright.sync_api import Page, expect


def validate_login_page(page: Page) -> bool:
    try:
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("https://sv-students-recommend.onrender.com/pages/login.html")
        title = page.title()
        assert contains(title.strip(), "Login – SV Students Recommend"), f"Expected title 'Login – SV Students Recommend' but got '{title}'"
        return True
    except AssertionError:
        return False


@pytest.mark.logout
def test_logout(login_as_admin: Page):
    """Test that a user can log out successfully after logging in."""
    page = login_as_admin
    page.wait_for_load_state("networkidle")
    # sleep(9)  # Ensure the page is fully loaded before attempting to log out
    page.locator("[data-test='nav-logout']").click()
    page.wait_for_load_state("networkidle")
    assert validate_login_page(page), "Logout validation failed: URL or title did not match expected login page"