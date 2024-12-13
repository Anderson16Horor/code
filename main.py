import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

# Function to generate a random password
def generate_password(length=12):
    # Ensure the length is sufficient for all required character types
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    # Define character categories
    digits = string.digits
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    special = "!%*"

    # Guarantee one character from each category
    password = [
        random.choice(digits),       # One digit
        random.choice(lower),        # One lowercase letter
        random.choice(upper),        # One uppercase letter
        random.choice(special)       # One special character
    ]

    # Fill the remaining characters randomly from all categories
    all_chars = digits + lower + upper + special
    password += [random.choice(all_chars) for _ in range(length - 4)]

    # Shuffle the password for randomness
    random.shuffle(password)
    return ''.join(password)

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# List to store mailbox data
mailbox_data = []

try:
    # Authorization
    driver.get("https://cp.beget.com/mail/10492791")
    username = "eeeeee13ev82"  # Enter your username
    password = "555555555"  # Enter your password

    # Enter username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login"))
    )
    username_field.clear()
    username_field.send_keys(username)

    # Enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.clear()
    password_field.send_keys(password)

    # Click the "Login" button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[st='button-login-submit']"))
    )
    login_button.click()

    # Wait for the mailbox creation page to load
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "email-name")))

    # Number of mailboxes to create
    num_mailboxes = 800

    for i in range(num_mailboxes):
        print(f"Creating mailbox #{i + 1}...")

        # Generate mailbox name and password
        mailbox_name = fake.first_name().lower() + fake.last_name().lower()
        mailbox_password = generate_password()

        # Locate fields for mailbox name and password
        mailbox_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "email-name"))
        )
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        # Clear and input data
        mailbox_field.clear()
        mailbox_field.send_keys(mailbox_name)

        password_field.clear()
        password_field.send_keys(mailbox_password)

        # Pause for 5 seconds
        time.sleep(5)

        # Click the "Create" button
        create_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Создать']"))
        )
        create_button.click()

        # Verify mailbox creation (optional, based on available success indicators)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'success-message-class')]"))
            )
            print(f"Mailbox {mailbox_name} created successfully.")
        except Exception as e:
            print(f"Error verifying mailbox creation: {e}")

        # Ensure fields are ready for the next input
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "email-name"))
        )
        mailbox_field.clear()

        # Save data to the list
        mailbox_data.append({"Mailbox Name": mailbox_name, "Password": mailbox_password})

    # Save mailbox data to an Excel file
    df = pd.DataFrame(mailbox_data)
    df.to_excel("created_mailboxes.xlsx", index=False)
    print("All data saved to 'created_mailboxes.xlsx'.")

finally:
    # Close the browser
    driver.quit()
