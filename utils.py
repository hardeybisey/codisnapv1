from playwright.sync_api import sync_playwright

def take_screenshot_from_url(url, sesstion_data):
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()
        browser_context = browser.new_context(device_scale_factor=2)
        browser_context.add_cookies([sesstion_data])
        page = browser_context.new_page()
        page.goto(url)
        screenshot_bytes = page.locator(".code").screenshot()
        browser.close()
        return screenshot_bytes