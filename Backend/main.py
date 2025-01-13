import pandas as pd
from bs4 import BeautifulSoup
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

# Step 1: Navigate to the main page
driver.get(START_URL)

current_page = 1

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
            for i in range(281):
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
                current_page += 1
        else:
            print("Couldn't find two SVG elements.")
    else:
        print("No <ul> element found.")

except Exception as e:
    print(f"Error: {e}")


# Wait for the page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/schemes']"))
)

data = []
not_found = []  # To store schemes where eligibility is not found

# Main loop for pagination
while True:
    # Get the page source and parse with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Step 2: Extract scheme sections
    sections = soup.select("a[href^='/schemes']")
    num_sections = len(sections)  # Count the number of sections
    print(f"Extracted {num_sections} sections from this page.")
    l = []
    for i in sections:
        if len(i.get_text(strip=True)) > 0:
            l.append(i)
    sections = l
    for section in sections:
        time.sleep(0.3)
        try:
            # Get the section name and URL
            section_name = section.get_text(strip=True)

            try:
                section_href = section["href"]  # Extract the href from the BeautifulSoup element
                print(f"Clicking on the scheme: {section_name}")
                print(section)

                # Locate the element using the href
                selenium_section = driver.find_element(By.CSS_SELECTOR, f"a[href='{section_href}']")

                # Scroll and attempt to click in a loop
                for __ in range(3):
                    clicked = False
                    time.sleep(0.2)
                    driver.execute_script("window.scrollTo(0, 0);")
                    driver.execute_script("window.scrollTo(0, 0);")
                    driver.execute_script("window.scrollTo(0, 0);")

                    for _ in range(5):  # Try scrolling and clicking up to 5 times
                        try:
                            driver.execute_script("arguments[0].scrollIntoView();",
                                                  selenium_section)  # Scroll into view
                            WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='{section_href}']")))
                            selenium_section.click()  # Attempt to click
                            clicked = True
                            print("Clicked")
                            break  # Exit the loop if clicked successfully
                        except Exception as inner_e:
                            print(f"Retrying click for section {section_name}")
                            # Scroll to the top of the page

                            time.sleep(0.3)  # Add a small delay before retrying

                    if not clicked:
                        raise Exception(f"Unable to click on the section: {section_name}")
                    else:
                        break

            except Exception as e:
                print(f"Error processing section {section_name}: {e}")
                df = pd.DataFrame(data)
                df.to_csv("myscheme_data5.csv", index=False)
                print("Data saved to myscheme_data.csv")

                # Save not found data to a separate CSV
                not_found_df = pd.DataFrame(not_found)
                not_found_df.to_csv("eligibility_not_found5.csv", index=False)
                print("Data saved to eligibility_not_found.csv")

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "eligibility"))
            )

            # Get the page source and parse with BeautifulSoup
            section_html = driver.page_source
            section_soup = BeautifulSoup(section_html, "html.parser")

            # Step 4: Extract the eligibility section
            eligibility_container = section_soup.find("div", id="eligibility")
            if not eligibility_container:
                print(f"Eligibility container not found for: {section_name}")
                not_found.append({"Scheme Name": section_name, "URL": driver.current_url})
                driver.execute_script("window.history.back();")
                continue

            # Extract eligibility criteria
            markdown_options = eligibility_container.find_all("ol")
            eligibility_criteria = []

            for ol in markdown_options:
                for li in ol.find_all("li"):
                    eligibility_criteria.append(li.get_text(strip=True))

            notes = eligibility_container.find_all("div", class_="mb-2")
            for note in notes:
                note_text = note.get_text(strip=True)
                if note_text:
                    eligibility_criteria.append(note_text)

            if eligibility_criteria:
                data.append(
                    {"Scheme Name": section_name, "Eligibility": eligibility_criteria, "URL": driver.current_url})
            else:
                print(f"No eligibility criteria found for: {section_name}")
                not_found.append({"Scheme Name": section_name, "URL": driver.current_url})

        except Exception as e:
            print(f"Error processing section {section_name}: {e}")

        # Go back to the previous page
        driver.execute_script("window.history.back();")

        # Wait for the main page to reload
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/schemes']"))
        )
        time.sleep(0.3)

    try:
        time.sleep(0.2)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ul.list-none.flex.flex-wrap.items-center.justify-center")))
        time.sleep(0.2)
        ul = driver.find_elements(
            By.CSS_SELECTOR,
            "ul.list-none.flex.flex-wrap.items-center.justify-center"
        )
        current_page += 1
        if ul:
            time.sleep(0.2)
            li_elements = ul[0].find_elements(By.TAG_NAME, "li")  # Find all <li> elements inside the <ul>
            found = False  # To track if the correct page number is found

            for li in li_elements:
                try:
                    page_text = li.text.strip()  # Get the text of the <li> element
                    if page_text == str(current_page):  # Check if it matches the current page number
                        print(f"Found the <li> element for page {current_page}. Clicking on it...")
                        for k in range(5):
                            try:
                                driver.execute_script("arguments[0].scrollIntoView();", li)  # Scroll the element into view
                                time.sleep(1)
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(li))  # Wait until clickable
                                time.sleep(1)
                                ActionChains(driver).move_to_element(li).click().perform()  # Click on the element
                                found = True
                                time.sleep(1)  # Small delay to ensure the page loads properly
                                break
                            except:
                                print("retrying clicking on page")
                                time.sleep(1)
                            # Scroll to the top of the page
                        driver.execute_script("window.scrollTo(0, 0);")

                except Exception as e:
                    print(f"Error processing <li> element: {e}")

            if not found:
                print(f"No <li> element found for page {current_page}.")
                break
        else:
            print("No <ul> element found.")

        time.sleep(2)
    except Exception as e:
        print(f"Error: {e}")

# Step 7: Close the browser
driver.quit()

# Step 8: Save data to CSV
df = pd.DataFrame(data)
df.to_csv("myscheme_data5.csv", index=False)
print("Data saved to myscheme_data.csv")

# Save not found data to a separate CSV
not_found_df = pd.DataFrame(not_found)
not_found_df.to_csv("eligibility_not_found5.csv", index=False)
print("Data saved to eligibility_not_found.csv")
