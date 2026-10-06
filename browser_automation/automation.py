from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # 1. Open website
    page.goto("http://127.0.0.1:8080")

    print("Website opened successfully")

    # 2. Add product to cart
    page.click("#add-to-cart")

    print("Product added to cart")

    page.screenshot(
        path="browser_automation/screenshots/cart.png"
    )

    # 3. Click checkout
    page.click("#checkout")

    print("Checkout page opened")

    page.screenshot(
        path="browser_automation/screenshots/checkout.png"
    )

    # 4. Enter customer details
    page.fill("#name", "Vishwas")

    page.fill("#email", "vishwas@example.com")

    print("Customer details entered")

    # 5. Place order
    page.click("#place-order")

    print("Order placed successfully")

    page.screenshot(
        path="browser_automation/screenshots/success.png"
    )

    browser.close()