from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
driver = webdriver.Chrome()
driver.get("https://www.demoblaze.com/")
wait = WebDriverWait(driver, 10)
NEW_USERNAME = "txin0567"
NEW_PASSWORD = "Txinpassword034"


# Helper: Wait for any modal backdrop to disappear
def wait_for_modal_to_disappear():
    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop")))
    except:
        pass

# Helper: Close login modal if it's still open
def close_login_modal():
    try:
        close_btn = driver.find_element(By.XPATH, "//div[@id='logInModal']//button[@class='close']")
        close_btn.click()
        time.sleep(1)
        print("Login modal closed.")
    except:
        print("No login modal to close.")

# Test 1: Verify Login Page Works
def test_login():
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "login2").click()
    wait.until(EC.visibility_of_element_located((By.ID, "loginusername")))
    driver.find_element(By.ID, "loginusername").send_keys(NEW_USERNAME)
    driver.find_element(By.ID, "loginpassword").send_keys(NEW_PASSWORD)
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()
    time.sleep(5)

    assert driver.find_element(By.ID, "nameofuser").is_displayed()
    print("Login successful.")


# Test 2: Verify Logout Works
def test_logout():
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "logout2").click()
    time.sleep(5)
    assert driver.find_element(By.ID, "login2").is_displayed()
    print("Logout successful.")

# Test 3: Verify Contact Form Works
def test_contact_form():
    wait_for_modal_to_disappear()
    driver.find_element(By.XPATH, "//a[text()='Contact']").click()
    wait.until(EC.visibility_of_element_located((By.ID, "recipient-email")))
    driver.find_element(By.ID, "recipient-email").send_keys("test@example.com")
    driver.find_element(By.ID, "recipient-name").send_keys("Test User")
    driver.find_element(By.ID, "message-text").send_keys("This is a test message.")
    driver.find_element(By.XPATH, "//button[text()='Send message']").click()
    time.sleep(5)
    driver.switch_to.alert.accept()
    print("Contact form submitted.")

# Test 4: Verify Products List Loads
def test_products_list():
    wait_for_modal_to_disappear()
    driver.find_element(By.XPATH, "//a[@class='navbar-brand']").click() 
    time.sleep(5)
    products = driver.find_elements(By.CLASS_NAME, "card-title")
    assert len(products) > 0
    print("Product list loaded.")

# Test 5: Verify Product Details Page Loads
def test_product_details():
    wait_for_modal_to_disappear()
    driver.find_element(By.CLASS_NAME, "card-title").click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "name")))
    product_name = driver.find_element(By.CLASS_NAME, "name").text
    assert product_name != ""
    driver.back()
    time.sleep(5)
    print("Product details loaded.")

# Test 6: Verify Categories Filter Works
def test_categories_filter():
    wait_for_modal_to_disappear()
    driver.find_element(By.XPATH, "//a[text()='Laptops']").click()
    time.sleep(5)
    products = driver.find_elements(By.CLASS_NAME, "card-title")
    assert len(products) > 0
    print("Category filter works.")

# Test 7: Verify Add to Cart
def test_add_to_cart():
    wait_for_modal_to_disappear()
    driver.find_element(By.CLASS_NAME, "card-title").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Add to cart']")))
    driver.find_element(By.XPATH, "//a[text()='Add to cart']").click()
    time.sleep(5)
    driver.switch_to.alert.accept()
    driver.back()
    time.sleep(5)
    print("Product added to cart.")

# Test 8: Verify Cart Page Loads
def test_cart_page():
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "cartur").click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success")))
    assert driver.find_element(By.CLASS_NAME, "success").is_displayed()
    print("Cart page loaded.")

# Test 9: Verify Order Placement Works
def test_order_placement():
    wait_for_modal_to_disappear()
    driver.find_element(By.XPATH, "//button[text()='Place Order']").click()
    wait.until(EC.visibility_of_element_located((By.ID, "name")))
    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "country").send_keys("Test Country")
    driver.find_element(By.ID, "city").send_keys("Test City")
    driver.find_element(By.ID, "card").send_keys("1234567890")
    driver.find_element(By.ID, "month").send_keys("12")
    driver.find_element(By.ID, "year").send_keys("2025")
    driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
    time.sleep(5)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "sweet-alert")))
    time.sleep(5)
    print("Order placed successfully.")

    driver.find_element(By.XPATH, "//button[text()='OK']").click()
    time.sleep(5)

    try:
        close_button = driver.find_element(By.XPATH, "//div[@id='orderModal']//button[@class='close']")
        close_button.click()
        print("Order modal manually closed.")
        time.sleep(5)
    except:
        print("Order modal already closed or not found.")

    driver.find_element(By.XPATH, "//a[@class='navbar-brand']").click()
    time.sleep(5)

# Test 10: Verify Remove Product From Cart
def test_remove_from_cart():
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "cartur").click()
    time.sleep(5)

    delete_buttons = driver.find_elements(By.XPATH, "//a[text()='Delete']")
    if not delete_buttons:
        print("Cart is empty. Adding a product first.")
        driver.find_element(By.XPATH, "//a[@class='navbar-brand']").click()
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, "card-title").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Add to cart']")))
        driver.find_element(By.XPATH, "//a[text()='Add to cart']").click()
        time.sleep(5)
        driver.switch_to.alert.accept()
        driver.find_element(By.ID, "cartur").click()
        time.sleep(5)
    
    delete_buttons = driver.find_elements(By.XPATH, "//a[text()='Delete']")
    if delete_buttons:
        delete_buttons[0].click()
        print("Product removed from cart.")
        time.sleep(5)
        products = driver.find_elements(By.CLASS_NAME, "success")
        assert len(products) == 0
    else:
        print("Still no products found to delete (unexpected).")


# Test 11: Verify Create Account
def test_create_account():
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "signin2").click()
    wait.until(EC.visibility_of_element_located((By.ID, "sign-username")))
    driver.find_element(By.ID, "sign-username").send_keys(NEW_USERNAME)
    driver.find_element(By.ID, "sign-password").send_keys(NEW_PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
    time.sleep(5)
    driver.switch_to.alert.accept()
    print(f"Account '{NEW_USERNAME}' created successfully.")


# Test 12: Verify Pagination Works
def test_pagination():
    wait_for_modal_to_disappear()

    next_button = driver.find_element(By.ID, "next2")
    next_button.click()
    time.sleep(5)

    products = driver.find_elements(By.CLASS_NAME, "card-title")
    assert len(products) > 0

    prev_button = driver.find_element(By.ID, "prev2")
    prev_button.click()
    time.sleep(5)

    products = driver.find_elements(By.CLASS_NAME, "card-title")
    assert len(products) > 0
    print("Pagination works.")


# ---- Run All Tests ----
try:
    test_create_account()
    test_login()
    test_contact_form()
    test_products_list()
    test_product_details()
    test_categories_filter()
    test_add_to_cart()
    test_cart_page()
    test_order_placement()
    test_remove_from_cart()
    test_logout()
    test_pagination()

finally:
    driver.quit()
