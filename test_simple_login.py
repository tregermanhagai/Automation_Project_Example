def test_simple_login(page):
    page.goto("https://practicetestautomation.com/practice-test-login/")
    page.fill("#username", "student")
    page.fill("#password", "Password123")
    page.click("#submit")
    assert page.locator(".post-title").text_content() == "Logged In Successfully"
    assert page.locator("div.post-content strong").text_content() == "Congratulations student. You successfully logged in!"
