from operator import contains

import pytest
from playwright.sync_api import Page, expect


def validate_login_page(page: Page) -> bool:
    try:
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("https://sv-students-recommend.onrender.com/pages/login.html")
        titel = page.title()
        assert contains(titel.strip(), "Login – SV Students Recommend"), f"Expected title 'Login – SV Students Recommend' but got '{titel}'"
        return True
    except AssertionError:
        return False


@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.logout
def test_logout(login_as_student: Page):
    """Test that a user can log out successfully after logging in."""
    page = login_as_student
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='nav-logout']").click()
    page.wait_for_load_state("networkidle")
    assert validate_login_page(page), "Logout validation failed: URL or title did not match expected login page"