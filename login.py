# login.py

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# 🔐 Load credentials from .env
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def save_jobright_cookies(output_file="jobright_cookies.json"):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment for headless login
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.jobright.ai/")
        time.sleep(5)

        # Click "Login" button to open login modal
        try:
            next_button = driver.find_element(By.XPATH, '//*[@id="firstpage"]/header/div/div[2]/span')
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print("⚠️ Could not click login button:", e)

        # Fill email and password
        email_input = driver.find_element(By.XPATH, '//*[@id="basic_email"]')
        email_input.send_keys(EMAIL)
        time.sleep(1)

        password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
        password_input.send_keys(PASSWORD)
        time.sleep(1)

        login_button = driver.find_element(By.XPATH, '//*[@id="basic"]/div[3]/div/div/div/div/button')
        login_button.click()

        print("🔐 Logging in...")
        time.sleep(10)  # Wait for dashboard or jobs page to load

        # Optionally check login success
        if "jobright" in driver.current_url:
            cookies = driver.get_cookies()
            with open(output_file, "w") as f:
                json.dump(cookies, f)
            print(f"✅ Cookies saved to {output_file}")
        else:
            print("⚠️ Login might have failed. Current URL:", driver.current_url)

    except Exception as e:
        print(f"❌ Login error: {e}")

    finally:
        driver.quit()

# Optional: for CLI testing
if __name__ == "__main__":
    save_jobright_cookies()
