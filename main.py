from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Define email and password (replace with your credentials)
email = "Yoru Username"
password = "Your Password"

# Configure Chrome options
chrome_options = Options()
# Optional 
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path='/usr/local/bin/chromedriver')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def login():
    """
    Log in to Instagram
    """
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver.get("https://www.instagram.com/")

    try:
        # Wait for the username field to appear, then input the username
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="username" and @aria-label="Phone number, username, or email"]'))
            )
            
        email_element = driver.find_element(By.XPATH, '//input[@name="username" and @aria-label="Phone number, username, or email"]')
        # Clears any pre-existing text to ensure
        email_element.clear()

        email_element.send_keys(email + Keys.TAB)

        # Wait for the password field to appear, then input the password
        password_element = driver.find_element(By.XPATH, '//input[@name="password" and @aria-label="Password"]')
        # Clears any pre-existing text to ensure 
        password_element.clear()

        password_element.send_keys(password + Keys.ENTER)

        print("Login successful!")

    except Exception as e:
        print(f'Login Failed: {e}...')

    return None

def navigate_saved():
    """
    Navigates to the Saved posts section.
    """
    try:
        # Wait for the "More" link to appear, then click it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "More"))
        )
        link = driver.find_element(By.LINK_TEXT, "More")
        link.click()
        print("Navigated to 'More'")

        # Wait for the "Saved" link to appear, then click it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Saved"))
        )

        link = driver.find_element(By.LINK_TEXT, "Saved")
        link.click()
        print("Navigated to saved")

        # Wait for the "All posts" link to appear, then click it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "All posts"))
        )
        link = driver.find_element(By.LINK_TEXT, "All posts")
        link.click()
        print("Navigated to all posts.")

    except Exception as e:
        print(f"Failed to navigate to {e}.")

def unsave_post():
    """
    Unsaves posts.
    Option to unsave post depending on 
    post category by analyzing hasthags.
    """
    # Navigates to first saved post
    try:
        # Wait for the first saved post to appear and click on it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_aagw"))
        )
        saved_post = driver.find_element(By.CLASS_NAME, "_aagw")
        print("Navigating to first saved post.")
        saved_post.click()
        
        # Locate and click the "Unsave/remove" button
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Remove')]"))
        )
        remove_button = driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Remove')]")
        print("Unsaving Post")
        driver.execute_script("arguments[0].scrollIntoView();", remove_button)
        time.sleep(3)  # Add delay to ensure visibility and stability
        remove_button.click()
        print("Sucessfully unsaved post.")
    
    except Exception as e:
        # Print error and capture a screenshot for debugging
        print(f"Error unsaving post: {e}")
        driver.save_screenshot("error_unsave_post.png")

    # Nagivates to the next post
    try:
        # Wait for the "Next" button to appear and click on it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(@aria-label, 'Next')]"))
        )
        next_button = driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Next')]")

        next_button.click()
        print("Sucessfully navigated to next post")
        
        # Locate and click the "Unsave/remove" button again
        remove_button = driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Remove')]")
        print("Unsaving Post")
        driver.execute_script("arguments[0].scrollIntoView();", remove_button)
        time.sleep(2)  # Add delay to ensure visibility and stability
        remove_button.click()
        print("Sucessfully unsaved post.")
    except Exception as e:
        print(f"Error navigating to next post.")

def filter_by(target_hashtags):
    """
    Checks the hashtags of a post and returns True if the post contains
    any of the target hashtags. Otherwise, returns False.
    """
    try:
        # Wait for the parent element containing hashtags to load
        parent_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1._aaco._aacu._aacx._aad7._aade"))
        )

        # Find all hashtags within the parent element
        hashtags = parent_element.find_elements(By.CSS_SELECTOR, "a[href*='/explore/tags/']")

        # Extract text of all hashtags
        post_hashtags = [tag.text for tag in hashtags]

        # Checks if any target hashtag is present in the post's hashtags
        for hashtag in target_hashtags:
            if hashtag in post_hashtags:
                print(f"Target hashtag '{hashtag}' found. Skipping post.")
                return True  

        print("No target hashtags found in post.")
        return False  

    except Exception as e:
        print(f"Error in filtering hashtags: {e}")
        return False 

if __name__ == "__main__":
    login()
    navigate_saved()
    # Define target hashtags to skip posts
    target_hashtags = ["#example1", "#example2", "#example3"]

    # Loop to process saved posts
    while True:
        try:
            # Check if post should be skipped
            if filter_by(target_hashtags):
                # If a target hashtag is found, navigate to the next post
                try:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(@aria-label, 'Next')]"))
                    )
                    next_button = driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Next')]")
                    next_button.click()
                    print("Skipped post with target hashtags. Navigated to next.")
                except Exception as e:
                    print(f"Error navigating to next post after skipping: {e}")
            else:
                # If no target hashtags are found, unsave the post
                unsave_post()
        except KeyboardInterrupt:
            print("Program exited manually.")
            break  
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break