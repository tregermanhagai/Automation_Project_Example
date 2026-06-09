from playwright.sync_api import Page, expect

def test_validate_admin_have_system_options(page: Page):
    """As an admin I will expect that after login the system menu will be visable"""
    
    page.goto("https://sv-students-recommend.onrender.com/")
    page.locator("[data-test='input-email']").fill("hagai@svcollege.co.il")
    page.locator("[data-test='input-password']").fill("test1234")
    page.get_by_role("button", name="Sign In").click()
    page.locator("[data-test='nav-system']").click()
    
    expect(page).to_have_title("System – SV Students Recommend")

   