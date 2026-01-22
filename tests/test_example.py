def test_example(browser, base_url):
    browser.get(base_url)
    assert "Marketplace" in browser.title
