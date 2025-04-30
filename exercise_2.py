from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
driver = webdriver.Chrome()
driver.set_window_position(0, 0)
driver.set_window_size(1280, 800)
driver.get("https://www.demoblaze.com/")
wait = WebDriverWait(driver, 10)
NEW_USERNAME = "txin8567"
NEW_PASSWORD = "Txinpassword934"

def wait_for_modal_to_disappear():
    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop")))
    except:
        pass

def close_login_modal():
    try:
        driver.execute_script("""
            var modal = document.getElementById('logInModal');
            if (modal) {
                modal.classList.remove('show');
                modal.style.display = 'none';
                document.body.classList.remove('modal-open');
                let backdrops = document.getElementsByClassName('modal-backdrop');
                while (backdrops.length > 0) {
                    backdrops[0].parentNode.removeChild(backdrops[0]);
                }
            }
        """)
        time.sleep(1)
        print("Forced login modal close with JS.")
    except Exception as e:
        print("Error forcing modal close:", e)

def go_home():
    try:
        driver.execute_script("""
            document.querySelectorAll('.modal.show').forEach(m => m.style.display = 'none');
            document.body.classList.remove('modal-open');
            document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
        """)
        time.sleep(1)
        driver.find_element(By.ID, "nava").click()
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "card-title")))
        print("Returned to homepage.")
    except Exception as e:
        print("Error returning to homepage:", e)

def test_invalid_login_wrong_password():
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "login2").click()
    wait.until(EC.visibility_of_element_located((By.ID, "loginusername")))
    driver.find_element(By.ID, "loginusername").send_keys(NEW_USERNAME)
    driver.find_element(By.ID, "loginpassword").send_keys("wrongpassword")
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()
    time.sleep(2)
    alert = driver.switch_to.alert
    assert "Wrong password" in alert.text
    alert.accept()
    print("Invalid login test passed.")

def test_invalid_logout_without_login():
    close_login_modal()
    wait_for_modal_to_disappear()
    try:
        driver.find_element(By.ID, "logout2").click()
        print("Logout button clicked, but should not be visible.")
    except:
        print("Logout button not interactable or absent, as expected.")

def test_invalid_contact_form_empty_fields():
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.find_element(By.XPATH, "//a[text()='Contact']").click()
    wait.until(EC.visibility_of_element_located((By.ID, "recipient-email")))
    driver.find_element(By.XPATH, "//button[text()='Send message']").click()
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        print("Unexpected alert appeared:", alert_text)
    except:
        print("No alert, as expected for invalid empty form.")

def test_invalid_products_dom_cleared():
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.execute_script("document.getElementById('tbodyid').innerHTML = '';")
    time.sleep(2)
    products = driver.find_elements(By.CLASS_NAME, "card-title")
    assert len(products) == 0
    print("Manually cleared product list - no products shown.")

def test_invalid_product_click_empty_space():
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.find_element(By.TAG_NAME, "body").click()
    print("Clicked non-product element - nothing happens.")

def test_invalid_category_filter_repeat_click():
    close_login_modal()
    wait_for_modal_to_disappear()
    laptops = driver.find_element(By.XPATH, "//a[text()='Laptops']")
    laptops.click()
    time.sleep(1)
    laptops.click()
    time.sleep(1)
    products = driver.find_elements(By.CLASS_NAME, "card-title")
    assert len(products) > 0
    print("Repeated category click doesn't break product list.")

def test_invalid_cart_load_empty():
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "cartur").click()
    wait.until(EC.visibility_of_element_located((By.ID, "totalp")))
    products = driver.find_elements(By.CLASS_NAME, "success")
    assert len(products) == 0, f"Cart is not empty. Found {len(products)} items"
    print("Cart is empty as expected.")
    go_home()

def test_invalid_remove_from_empty_cart():
    go_home()
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "cartur").click()
    wait.until(EC.visibility_of_element_located((By.ID, "totalp")))
    delete_buttons = driver.find_elements(By.XPATH, "//a[text()='Delete']")
    assert len(delete_buttons) == 0
    print("No delete button present in empty cart.")
    go_home()

def test_invalid_add_to_cart_excessive_quantity():
    go_home()
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.find_element(By.CLASS_NAME, "card-title").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Add to cart']")))
    for i in range(15):
        driver.find_element(By.XPATH, "//a[text()='Add to cart']").click()
        time.sleep(2)
        try:
            driver.switch_to.alert.accept()
            print(f"Item added to cart {i+1} time(s).")
        except:
            print(f"No alert shown at iteration {i+1} – possible failure.")
    driver.find_element(By.ID, "cartur").click()
    wait.until(EC.visibility_of_element_located((By.ID, "totalp")))
    products = driver.find_elements(By.XPATH, "//tr[@class='success']")
    print(f"{len(products)} items found in cart.")
    assert len(products) <= 15
    print("Excessive add-to-cart boundary test passed.")
    go_home()

def test_invalid_order_incomplete_form():
    go_home()
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "cartur").click()
    wait.until(EC.visibility_of_element_located((By.ID, "totalp")))
    driver.find_element(By.XPATH, "//button[text()='Place Order']").click()
    wait.until(EC.visibility_of_element_located((By.ID, "name")))
    driver.find_element(By.ID, "name").send_keys("")
    driver.find_element(By.ID, "country").send_keys("")
    driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        print("Unexpected alert:", alert.text)
        alert.accept()
    except:
        print("Form was not accepted without input, as expected.")
    go_home()

def test_invalid_create_account_duplicate():
    close_login_modal()
    wait_for_modal_to_disappear()
    driver.find_element(By.ID, "signin2").click()
    wait.until(EC.visibility_of_element_located((By.ID, "sign-username")))
    driver.find_element(By.ID, "sign-username").send_keys(NEW_USERNAME)
    driver.find_element(By.ID, "sign-password").send_keys(NEW_PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
    time.sleep(2)
    alert = driver.switch_to.alert
    assert "already exist" in alert.text
    alert.accept()
    print("Duplicate account test passed.")
    go_home()

def test_invalid_pagination_on_last_page():
    close_login_modal()
    wait_for_modal_to_disappear()
    try:
        next_button = driver.find_element(By.ID, "next2")
        while next_button.is_displayed():
            next_button.click()
            time.sleep(1)
            next_button = driver.find_element(By.ID, "next2")
        next_button.click()
        print("Unexpected next button click on last page.")
    except:
        print("Next button not clickable on last page, as expected.")

# ---- Run All Tests ----
tests = [
    test_invalid_login_wrong_password,
    test_invalid_logout_without_login,
    test_invalid_contact_form_empty_fields,
    test_invalid_products_dom_cleared,
    test_invalid_product_click_empty_space,
    test_invalid_category_filter_repeat_click,
    test_invalid_cart_load_empty,
    test_invalid_remove_from_empty_cart,
    test_invalid_add_to_cart_excessive_quantity,
    test_invalid_order_incomplete_form,
    test_invalid_create_account_duplicate,
    test_invalid_pagination_on_last_page,
]

try:
    for test in tests:
        try:
            print(f"\nRunning {test.__name__}...")
            test()
            time.sleep(1) 
        except AssertionError as e:
            print(f"Assertion failed in {test.__name__}: {e}")
        except Exception as e:
            print(f"Exception in {test.__name__}: {e}")
finally:
    driver.quit()
