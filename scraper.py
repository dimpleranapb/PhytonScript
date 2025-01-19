import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options to connect to the running browser
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the running Chrome instance

# Set up Chrome driver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print("Starting the script and connecting to the open browser...")

# Counter for total account numbers collected
total_account_numbers = 0

try:
    print("Waiting for the page to load and find top 20 links...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ds-dex-table-row.ds-dex-table-row-top')))
    print("Page loaded successfully.")
    
    # Collect top 20 coin page URLs
    top_20_links = driver.find_elements(By.CLASS_NAME, 'ds-dex-table-row.ds-dex-table-row-top')
    coin_page_urls = [link.get_attribute('href') for link in top_20_links[:20]]  # Limit to the first 20 coins
    print(f"Collected {len(coin_page_urls)} coin page URLs.")
    
    if not coin_page_urls:
        print("No coin links found. Exiting script.")
        driver.quit()
        exit()

    # Prepare CSV file for saving account numbers
    with open('top_traders_account_numbers.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Account Number'])  # Write CSV header

        # Process each coin page
        for coin_page_url in coin_page_urls:
            try:
                print(f"Processing coin page: {coin_page_url}")
                retries = 3  # Number of retries for each coin page

                while retries > 0:
                    try:
                        # Load the coin page
                        driver.get(coin_page_url)

                        # Wait for the "Top Traders" tab to be clickable
                        print("Waiting for the 'Top Traders' tab to become clickable...")
                        top_traders_tab = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[text()="Top Traders"]'))
                        )
                        print("Clicking on 'Top Traders' tab...")
                        top_traders_tab.click()

                        # Add a delay for the "Top Traders" tab to load fully
                        print("Waiting for 'Top Traders' tab content to load (explicit delay)...")
                        time.sleep(5)  # Delay of 5 seconds

                        # Wait for wallet links to appear
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "solscan.io/account/")]'))
                        )

                        # Extract wallet links
                        print("Extracting wallet links...")
                        wallet_links = driver.find_elements(By.XPATH, '//div[@class="custom-1nvxwu0"]//a[contains(@href, "solscan.io/account/")]')

                        # If no wallet links are found, retry by reloading the page
                        if not wallet_links:
                            print("No wallet links found. Reloading the page and retrying...")
                            retries -= 1
                            continue  # Reload the page and retry

                        # Limit to top 100 traders
                        wallet_links = wallet_links[:100]  # Ensure only top 100 are processed
                        print(f"Found {len(wallet_links)} wallet links (limited to top 100).")

                        # Extract and save account numbers (part after 'account/')
                        account_numbers = [link.get_attribute('href').split('account/')[1] for link in wallet_links]
                        total_account_numbers += len(account_numbers)  # Update the total count
                        for account_number in account_numbers:
                            writer.writerow([account_number])

                        print(f"Finished processing {coin_page_url}.")
                        break  # Exit retry loop after success

                    except Exception as e:
                        print(f"Error occurred: {e}. Retrying... (Remaining retries: {retries - 1})")
                        retries -= 1
                        if retries == 0:
                            print(f"Failed to process {coin_page_url} after multiple retries.")
                            break

            except Exception as e:
                print(f"Error processing {coin_page_url}: {e}")
                continue

finally:
    # Close the driver
    print("Closing the browser...")
    driver.quit()
    print(f"Browser closed. Total account numbers collected: {total_account_numbers}")
