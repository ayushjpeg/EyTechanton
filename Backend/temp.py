from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()

BASE_URL = "https://www.myscheme.gov.in"
START_URL = f"{BASE_URL}/search"

# Open the base URL
driver.get(START_URL)

try:
    # Wait for the pagination container to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list-none.flex.flex-wrap.items-center.justify-center")))

    # Find the <ul> element
    ul = driver.find_elements(
        By.CSS_SELECTOR,
        "ul.list-none.flex.flex-wrap.items-center.justify-center"
    )

    if ul:
        # Find all the <svg> elements inside the <ul> (both arrows)
        svg_elements = ul[0].find_elements(By.TAG_NAME, "svg")

        # Check if there are two <svg> elements
        if len(svg_elements) > 1:
            print(f"Found {len(svg_elements)} SVG elements. Clicking the second one...")

            # Click the second <svg> 296 times with a 2-second delay
            for i in range(50):
                print(f"Clicking on the next button, iteration {i + 1}")

                # Scroll the element into view and wait for it to be clickable
                driver.execute_script("arguments[0].scrollIntoView();", svg_elements[1])
                time.sleep(0.5)
                # Wait until the element is clickable
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(svg_elements[1]))
                time.sleep(0.5)
                # Use ActionChains to click on the second <svg>
                ActionChains(driver).move_to_element(svg_elements[1]).click().perform()

                # Wait for 2 seconds between clicks
                time.sleep(1)
        else:
            print("Couldn't find two SVG elements.")
    else:
        print("No <ul> element found.")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()