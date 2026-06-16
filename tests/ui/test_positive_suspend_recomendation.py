from operator import contains
import os
# from time import sleep

from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page, expect


load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
email = os.getenv("ADMIN_USER", "")
password = os.getenv("ADMIN_PASSWORD", "")


CUSTOM_DEVICES = {
    "iPhone 17": {
        "viewport": {"width": 402, "height": 874},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "default_browser_type": "webkit",
        "user_agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/18.0 Mobile/15E148 Safari/604.1"
        ),
    },
    "Samsung 26": {
        "viewport": {"width": 384, "height": 832},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "default_browser_type": "chromium",
        "user_agent": (
            "Mozilla/5.0 (Linux; Android 15; SM-S931B) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.0.0 Mobile Safari/537.36"
        ),
    },
}


def resolve_device(playwright, device_name):
    """Return a context-args dict for a device name.
    Looks in Playwright's built-in registry first, then our custom dict,
    and treats 'Desktop Chrome' as plain desktop (empty config)."""
    if device_name == "Desktop Chrome":
        return {}
    if device_name in playwright.devices:
        return playwright.devices[device_name]
    if device_name in CUSTOM_DEVICES:
        return CUSTOM_DEVICES[device_name]
    raise ValueError(f"Unknown device: {device_name!r}")

def validate_suspend(page: Page) -> bool:
    try:
        error_msg_locator = page.locator("[data-test=\"error-message\"]")
        expect(error_msg_locator).to_have_text("New recommendations are currently disabled by the administrator.")
        return True
    except AssertionError:
        return False

@pytest.mark.parametrize(
    "device_name",
    ["iPhone 17", "Samsung 26", "Desktop Chrome"],
)
@pytest.mark.system
def test_suspend_recommendation(playwright, browser, device_name):
    """Test that a user can suspend a recommendation successfully."""
    device = resolve_device(playwright, device_name)
    context = browser.new_context(**device)
    page = context.new_page()
    page.goto(BASE)
    page.get_by_label("Email").fill(email)
    page.locator("[data-test='input-password']").fill(password)
    page.get_by_role("button", name="Sign In").click()
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
    