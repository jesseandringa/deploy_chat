import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


# Function to initialize WebDriver for each thread
def initialize_webdriver():
    pass
    # Configure WebDriver options
    # chrome_options = ChromeOptions()
    # chrome_options.add_argument("--headless")  # Example: Run headless Chrome

    # Create WebDriver instance
    # service = ChromeService(executable_path=chrome_driver_path)
    # driver = webdriver.Chrome()

    # Store WebDriver instance in thread-local storage
    # thread_local.driver = driver  # Store driver in thread-local storage


# Function to perform actions using WebDriver and return result
def perform_actions(yes):
    print(yes)
    # print(thread_local)
    # driver = thread_local.driver
    driver = webdriver.Chrome()
    try:
        # Example actions
        driver.get("https://nike.com")
        links = driver.find_elements(By.TAG_NAME, "a")

        time.sleep(5)  # Simulate some activity

        # Return a result (can be any data type)
        return links[0]

    finally:
        driver.quit()


# Thread-local storage
# thread_local = threading.local()  # Initialize thread-local storage

# Create threads
# threads = []
# for _ in range(5):  # Example: Create 5 threads
#     thread = threading.Thread(target=initialize_webdriver)
#     threads.append(thread)
#     thread.start()

# # Wait for all threads to complete initialization
# for thread in threads:
#     thread.join()

# Perform actions in each thread and collect results
threads = []
results = []
yes = 0
for _ in range(5):  # Example: Perform actions in 5 threads
    thread = threading.Thread(target=lambda: results.append(perform_actions(yes)))
    threads.append(thread)
    thread.start()


# Wait for all threads to complete actions
for thread in threads:
    thread.join()

# Print results
print(results)
