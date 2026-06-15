@pytest.mark.api
def test_NAME_OF_TEST(playwright: Playwright):
    """WHAT this test verifies and WHICH result is expected."""
 
    api = playwright.request.new_context(base_url=BASE)
 
    # 1) Prepare input data (if the endpoint needs any)
    payload = { "KEY": "VALUE" }
 
    # 2) Send the request (GET / POST / PUT / DELETE)
    res = api.METHOD("/YOUR/ENDPOINT", data=payload)
 
    # 3) Assert the status code
    assert res.status == EXPECTED_CODE, f"Failed: {res.text()}"
 
    # 4) (Optional) Assert something about the response body
    body = res.json()
    assert body["FIELD"] == EXPECTED_VALUE
 
    # 5) Clean up
    api.dispose()
