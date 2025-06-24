from playwright.async_api import async_playwright

async def scrape_profile(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)
        await page.wait_for_timeout(3000)

        profile = {}

        try:
            profile['name'] = await page.locator('h1').nth(0).inner_text()
        except:
            profile['name'] = ''

        try:
            profile['headline'] = await page.locator('.text-body-medium').nth(0).inner_text()
        except:
            profile['headline'] = ''

        try:
            profile['summary'] = await page.locator('section.pv-about-section').inner_text()
        except:
            profile['summary'] = ''

        await browser.close()
        return profile
