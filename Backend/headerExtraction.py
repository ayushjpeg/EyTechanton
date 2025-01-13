import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def extract_benefits(input_csv, output_csv):
    # Load the input CSV file
    input_data = pd.read_csv(input_csv)

    # Check if the output file exists
    if os.path.exists(output_csv):
        # Load existing output file to avoid re-processing
        existing_data = pd.read_csv(output_csv)
        processed_urls = set(existing_data["URL"].tolist())
    else:
        # Initialize an empty output file
        processed_urls = set()
        pd.DataFrame(columns=["Scheme Name", "URL", "Benefits"]).to_csv(output_csv, index=False)

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH

    # Process each URL
    for index, row in input_data.iterrows():
        time.sleep(6)  # To avoid hitting rate limits
        scheme_name = row["Scheme Name"]
        url = row["URL"]

        # Skip URLs already processed
        if url in processed_urls:
            print(f"Skipping already processed URL: {url}")
            continue

        try:
            # Visit the URL
            print(f"Visiting: {url}")
            driver.get(url)

            # Wait for the Benefits section to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "benefits"))
            )

            # Extract the benefits content
            benefits_element = driver.find_element(By.ID, "benefits")
            benefits_text = benefits_element.text.strip()

            # Append the data directly to the CSV
            with open(output_csv, mode='a', newline='', encoding='utf-8') as f:
                f.write(f'"{scheme_name}","{url}","{benefits_text}"\n')

            print(f"Extracted and saved benefits for: {scheme_name}")

        except Exception as e:
            print(f"Error processing {url}: {e}")

    # Close the WebDriver
    driver.quit()
    print(f"Process complete. Updated benefits saved to {output_csv}")


# Example usage
if __name__ == "__main__":
    input_csv = "eligibilityData.csv"  # Input file with Scheme Name and URL columns
    output_csv = "benefits.csv"       # Output file for extracted benefits
    extract_benefits(input_csv, output_csv)
