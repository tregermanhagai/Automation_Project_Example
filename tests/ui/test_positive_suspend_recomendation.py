from operator import contains
# from time import sleep

import pytest
from playwright.sync_api import Page, expect


def validate_suspend(page: Page) -> bool:
    try:
        error_msg_locator = page.locator("[data-test=\"error-message\"]")
        expect(error_msg_locator).to_have_text("New recommendations are currently disabled by the administrator.")
        return True
    except AssertionError:
        return False


@pytest.mark.system
def test_suspend_recommendation(login_as_admin: Page):
    """Test that a user can suspend a recommendation successfully."""
    page = login_as_admin
    page.locator("[data-test=\"nav-system\"]").click()
    page.locator("[data-test=\"btn-toggle-recommendations\"]").click()
    page.locator("[data-test=\"nav-home\"]").click()
    page.locator("[data-test=\"nav-signup-recommendations\"]").click()
    page.locator("[data-test=\"input-recommendation-name\"]").click()
    page.locator("[data-test=\"input-recommendation-name\"]").fill("good movie")
    page.locator("[data-test=\"btn-submit-recommendation\"]").click()
    assert validate_suspend(page), "Suspend admin system actin was not working as expected"
    page.locator("[data-test=\"nav-system\"]").click()
    page.locator("[data-test=\"btn-toggle-recommendations\"]").click()
    