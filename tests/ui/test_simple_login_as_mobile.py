import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
email = os.getenv("ADMIN_USER", "")
password = os.getenv("PASSWORD", "")


# Custom device descriptors for models not in Playwright's registry.
# These are config dicts — same shape as playwright.devices entries.
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

@pytest.mark.ui
@pytest.mark.mobile
@pytest.mark.parametrize(
    "device_name",
    ["iPhone 17", "Samsung 26", "Desktop Chrome"],
)
def test_login_responsive(playwright, browser, device_name):
    device = resolve_device(playwright, device_name)
    context = browser.new_context(**device)
    page = context.new_page()
    page.goto(BASE)
    page.get_by_label("Email").fill(email)
    page.locator("[data-test='input-password']").fill(password)
    page.get_by_role("button", name="Sign In").click()
    expect(page).to_have_url(f"{BASE}/pages/home.html", timeout=15000)
    context.close()