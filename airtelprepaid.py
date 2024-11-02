#import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random  

def driver():
    chrome_options = Options()
    # Use --headless=new for a more stable headless experience if visual output isn't required
    #chrome_options.add_argument("--headless=new")  # Remove or adjust this for visual mode
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def find_mobile_no_inp(driver):
    selectors = [
                "//input[@placeholder='Enter mobile number']",
                "//input[@placeholder='Mobile number']",
                "//input[@placeholder='Phone number']",
                "//input[contains(@placeholder, 'Enter your 10-digit mobile number')]",
            ]

    wait = WebDriverWait(driver, 5)
    
    for xpath in selectors:
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            print(f"Found mobile input field using selector: {xpath}")
            driver.execute_script("arguments[0].style.border='3px solid red'", element)
            time.sleep(1)
            return element
        except TimeoutException:
            continue
            
    raise Exception("Could not find mobile number input field")

def select_upi(driver):
    """
    selecting upi dropdown in the payment page with javascript
    """
    try:
        # Locate the UPI dropdown by its ID
        UPI_dropdown = driver.find_element(By.ID, "accordion-header-2")
        
        # Scroll  and highlight it for visibility
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", UPI_dropdown)
        driver.execute_script("arguments[0].style.border='3px solid green'", UPI_dropdown)
        time.sleep(1)
        
        # Use JavaScript to click the dropdown
        driver.execute_script("arguments[0].click();", UPI_dropdown)
        
        #print("Successfully clicked on the UPI dropdown")
        time.sleep(5)  # Wait to observe the change if necessary
        return True
    
    except Exception as e:
        print(f"Error clicking on the accordion header: {str(e)}")
        return False


def other_upi(driver):
    """
    selecting other upi option  in the payment page with javascript which gives a input box 
    """
    try:
        # Locate the 'Pay via other UPI ID' container by its data-testid
        pay_other_upi = driver.find_element(By.XPATH, "//div[@data-testid='payOtherUpiContainer']")
        
        # Scroll to the element and highlight it for visibility
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pay_other_upi)
        driver.execute_script("arguments[0].style.border='3px solid blue'", pay_other_upi)
        time.sleep(1)
        
        # Use JavaScript to click the element
        driver.execute_script("arguments[0].click();", pay_other_upi)
        
        #print("Successfully clicked on the 'Pay via other UPI ID' option!")
        time.sleep(5)  # Wait to observe the change if necessary
        return True
    
    except Exception as e:
        print(f"Error clicking on 'Pay via other UPI ID': {str(e)}")
        return False


def enter_upi_id(driver, upi_id):
    """
    Locate the input field for UPI ID and enter the given UPI ID.
    """
    try:
        # Find the input field near "Pay via other UPI ID"
        upi_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'UPI ID')]")
        
        # Scroll to the input field and highlight it
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upi_input)
        driver.execute_script("arguments[0].style.border='3px solid green'", upi_input)
        time.sleep(1)
        
        # Clear the input field if any text is present and type the UPI ID
        upi_input.clear()
        upi_input.send_keys(upi_id)
        
        print(f"Successfully entered UPI ID: {upi_id}")
        time.sleep(2)  # Wait to observe the entered UPI ID if necessary
        return True
    
    except Exception as e:
        print(f"Error entering UPI ID: {str(e)}")
        return False


def click_verify_button(driver):
    """
    Find and click on the 'Verify' button after entering the UPI ID.
    """
    try:
        # Locate the Verify button by its unique data-testid attribute
        verify_button = driver.find_element(By.XPATH, "//button[@data-testid='vpaInputSubmit']")
        
        # Scroll to the button if necessary
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", verify_button)
        driver.execute_script("arguments[0].style.border='3px solid blue'", verify_button)
        time.sleep(1)
        
        # Click on the Verify button
        verify_button.click()
        
        print("Successfully clicked the 'Verify' button.")
        time.sleep(2)  # Pause to observe the button click effect
        return True
    
    except Exception as e:
        print(f"Error clicking 'Verify' button: {str(e)}")
        return False


#Airtel 
class Airtel:
    def __init__(self,url):
        self.driver = driver()
        self.url= url

    def get_plans(self,Mobile_No:str):
        print("visiting Airtel platform with mobile no")
        print("*-"*20)
        try:
            self.driver.get(self.url)
            time.sleep(2)

            #finding mobile no input
            input_mobile = find_mobile_no_inp(self.driver)
            print(f"Entering mobile number: {Mobile_No}")
            input_mobile.clear()
            time.sleep(1)

            #entering mobile no 
            for digit in Mobile_No:
                input_mobile.send_keys(digit)
                time.sleep(0.2)
        
            print("Mobile number entered successfully")
            time.sleep(10)
            return

        except Exception as e:
            print(f"Error: {str(e)}")
            raise
    

    def select_rplans(self):
        """
        Click on a random plan card among multiple cards using JavaScript.
        """

        # Find all chevron icons on the page
        Plan_cards = self.driver.find_elements(By.XPATH, "//div[@class='chevron-arrow']")
        
        # Check if any chevron icons are found
        if not Plan_cards:
            print("No cards found.")
            return False
        
        # Select a random chevron icon from the list
        random_card = random.choice(Plan_cards)
        
        # Scroll the selected icon into view and highlight it for visibility
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_card)
        self.driver.execute_script("arguments[0].style.border='3px solid blue'", random_card)
        time.sleep(1)

        # Use JavaScript to click the randomly selected icon
        self.driver.execute_script("arguments[0].click();", random_card)
        
        print("Successfully clicked on a random chevron icon!")
        time.sleep(5)  # Wait to see if the next page loads
        return True


    def start_payment(self,UPIid):
        """
        Starting process for payment with given upi
        """
        #step-1
        select_upi(self.driver)

        #step-2
        other_upi(self.driver)

        #step-3
        enter_upi_id(self.driver,UPIid)

        #step-4
        click_verify_button(self.driver)
        click_verify_button(self.driver)

if __name__ == "__main__":
    url = "https://www.airtel.in/recharge/prepaid/"
    air = Airtel(url)
    air.get_plans("8093819062")

    air.select_rplans()
    UPIID = "7605931480@ybl"
    air.start_payment(UPIID)