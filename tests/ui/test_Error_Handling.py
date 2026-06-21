import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")

def validate_error_msg_for_too_short_password_in_registration(page: Page) -> bool:
    try:
        page.wait_for_load_state("networkidle")
        error_message = page.locator("[data-test=\"error-message\"]")
        expect(error_message).to_have_text("Password should be at least 6 characters.")
        assert error_message.inner_text() == "Password should be at least 6 characters.", f"Expected error message to be 'Password should be at least 6 characters.', but got '{error_message.inner_text()}'."
        return True
    except AssertionError:
        return False

@pytest.mark.ui
@pytest.mark.error_handling
def test_error_msg_displayed_for_invalid_password_in_registration(page: Page):
    """SRS 3.1.2a: Test that an error message is displayed for an invalid password during registration."""
    page.goto(f"{BASE}")
    page.locator("[data-test=\"link-register\"]").click()
    page.locator("[data-test=\"input-name\"]").fill("test")
    page.locator("[data-test=\"input-email\"]").fill("test12@testsvcollege.co.il")
    page.locator("[data-test=\"input-password\"]").fill("test")
    page.locator("[data-test=\"btn-register\"]").click()
    assert validate_error_msg_for_too_short_password_in_registration(page), "Incorrect Error message when expecting error message: \"Password should be at least 6 characters.\""

    