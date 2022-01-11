from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time, datetime
from OpenSeaScripts.AssetOptions import AssetOptions

class OSSBrowser:
    def __init__(self, command_executor_url:str = None, session_id:str = None, headless:bool = False):
        """
        Create a new OSSBrowser instance by opening a new chrome window or reconnecting to an existing session.
        If command_executor_url and session_id are provided, the browser will be reconnected to an existing session.

        Args:
            command_executor_url (str, optional): The command_executor_url of an existing browser session. Defaults to None.
            session_id (str, optional): The session_id of an existing browser session. Defaults to None.
            headless (bool, optional): Wether to operate in headless mode or not. Defaults to False.
        """

        service = Service(ChromeDriverManager().install()) # Install the Chrome driver and create a new Service

        chrome_options = Options() # Create an Options object to configure the browser

        if headless:
            chrome_options.add_argument("--headless") # Add headless argument if headless is True

        if command_executor_url is not None and session_id is not None: # If command_executor_url and session_id are provided, connect to an existing session
            self.driver = webdriver.Remote(command_executor=command_executor_url, desired_capabilities={}) # Connect to an existing session
            self.driver.close()
            self.driver.session_id = session_id
            self.driver.file_detector = UselessFileDetector() # Use a different file_detector for existing sessions
        else: # Otherwise, open a new window
            self.driver = webdriver.Chrome(chrome_options=chrome_options, service=service) # Create a new browser window

        self.driver.get("https://www.opensea.io/") # Go to the OpenSea website

        if not headless:
            self.driver.maximize_window() # Operate in full screen

    def _find_element_timeout(self, by:str, value:str, timeout:float = 7, base_delay:float = 0.1):
        """Find an HTML element, waiting up to timeout seconds for it to appear and delaying base_delay
        seconds before searching. Uses the Selenium By method to search for value.

        Args:
            by (str): The method to search for value. Most likely By.ID or By.CSS_SELECTOR.
            value (str): The value to search for.
            timeout (float, optional): How long to wait before failing. Defaults to 7.
            base_delay (float, optional): How long to wait before the first check. Defaults to 0.1.

        Raises:
            Exception: If the element is not found after timeout seconds.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: The element found.
        """
        time.sleep(base_delay)

        for i in range(timeout):
            try:
                return self.driver.find_element(by, value) # Attempt to find element
            except:
                time.sleep(1) # Wait if not found

        raise Exception("Element not found") # Raise exception if not found after timeout seconds

    def _find_elements_timeout(self, by:str, value:str, timeout:float = 7, base_delay:float = 0.1):
        """Find HTML elements, waiting up to timeout seconds for them to appear and delaying base_delay
        seconds before searching. Uses the Selenium By method to search for value.

        Args:
            by (str): The method to search for value. Most likely By.ID or By.CSS_SELECTOR.
            value (str): The value to search for.
            timeout (float, optional): How long to wait before failing. Defaults to 7.
            base_delay (float, optional): How long to wait before the first check. Defaults to 0.1.

        Raises:
            Exception: If elements are not found after timeout seconds.

        Returns:
            list: The elements found.
        """

        time.sleep(base_delay)

        for i in range(timeout):
            try:
                return self.driver.find_elements(by, value) # Attempt to find elements
            except:
                time.sleep(1) # Wait if not found

        raise Exception("Elements not found") # Raise exception if not found after timeout seconds

    def _find_element_content_timeout(self, by:str, value:str, content_text:str, timeout:float = 7, base_delay:float = 0.1):
        """Find an HTML element with content content_text, waiting up to timeout seconds
        for it to appear and delaying base_delay seconds before searching.
        Uses the Selenium By method to search for value.

        Args:
            by (str): The method to search for value. Most likely By.ID or By.CSS_SELECTOR.
            value (str): The value to search for.
            content_text (str): The content of the element to search for.
            timeout (float, optional): How long to wait before failing. Defaults to 7.
            base_delay (float, optional): How long to wait before the first check. Defaults to 0.1.

        Raises:
            Exception: If the element is not found after timeout seconds.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: The element found.
        """

        time.sleep(base_delay)

        for i in range(timeout):
            try:
                elements = self.driver.find_elements(by, value) # Attempt to find elements

                for element in elements:
                    if element.text == content_text: # Check if element has the correct content
                        return element

                raise Exception("Element not found") # Jump to except if not found
            except:
                time.sleep(1) # Wait if not found

        raise Exception("Element not found") # Raise exception if not found after timeout seconds


    def upload_asset(self, asset_options:AssetOptions, create_link:str = "https://opensea.io/asset/create?enable_supply=true"):
        """
        Upload a given asset to opensea.io.

        Args:
            asset_options (AssetOptions): The asset object to upload.
            create_link (str, optional): The URL to use to upload. Use this for uploading to a collection. Defaults to "https://opensea.io/asset/create?enable_supply=true".

        Raises:
            ValueError: If the asset_options is of the wrong type.
            ValueError: If the asset_options is missing required fields.
            Exception: If the asset upload fails.

        Returns:
            Boolean: False if the asset was not uploaded.
            str: The URL of the asset if it was uploaded.
        """

        try: # Wrap the whole thing in a try/except block to safely return False if errors occur
            if not isinstance(asset_options, AssetOptions):
                raise ValueError("Asset options must be an instance of AssetOptions")

            self.driver.get(create_link) # Go to the create page

            fileUpload = self._find_element_timeout(By.ID, "media")
            self.driver.execute_script('arguments[0].style = ""; arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";', fileUpload)
            fileUpload.send_keys(asset_options.get_asset_path()) # Upload the asset

            if AssetOptions.needs_preview(asset_options.get_asset_path().split(".")[-1]): # Determine if the asset needs a preview (certain file types do on Opensea)
                previewUpload = self._find_element_timeout(By.NAME, "preview")
                self.driver.execute_script('arguments[0].style = ""; arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";', previewUpload)
                preview_path = asset_options.get_preview_path()

                if preview_path == "":
                    raise ValueError("Multimedia files need a preview image")

                previewUpload.send_keys(preview_path) # Upload the preview image

            self._find_element_timeout(By.ID, "name").send_keys(asset_options.get_name()) # Set the name
            self._find_element_timeout(By.ID, "external_link").send_keys(asset_options.get_external_link()) # Set the external link
            self._find_element_timeout(By.ID, "description").send_keys(asset_options.get_description()) # Set the description

            if not len(asset_options.get_properties()) == 0: # If there are properties, set them
                self._find_element_timeout(By.CSS_SELECTOR, "button[aria-label='Add properties'").click()

                for i, property in enumerate(asset_options.get_properties()):
                    self._find_elements_timeout(By.CSS_SELECTOR, "input[placeholder='Character']")[i].send_keys(property["name"])
                    self._find_elements_timeout(By.CSS_SELECTOR, "input[placeholder='Male']")[i].send_keys(property["value"])
                    self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Add more").click()

                self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Save").click()

            if not len(asset_options.get_levels()) == 0: # If there are levels, set them
                self._find_element_timeout(By.CSS_SELECTOR, "button[aria-label='Add levels'").click()

                for i, level in enumerate(asset_options.get_levels()):
                    self._find_elements_timeout(By.CSS_SELECTOR, "input[placeholder='Speed']")[i].send_keys(level["name"])
                    max_field = self._find_elements_timeout(By.CSS_SELECTOR, "input[placeholder='Max']")[i]
                    max_field.send_keys(Keys.CONTROL, "a")
                    max_field.send_keys(level["max"])
                    val_field = self._find_elements_timeout(By.CSS_SELECTOR, "input[placeHolder='Min']")[i]
                    val_field.send_keys(Keys.CONTROL, "a")
                    val_field.send_keys(level["value"])
                    self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Add more").click()

                self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Save").click()

            if not len(asset_options.get_stats()) == 0: # If there are stats, set them
                self._find_element_timeout(By.CSS_SELECTOR, "button[aria-label='Add stats'").click()

                for i, stat in enumerate(asset_options.get_stats()):
                    self._find_elements_timeout(By.CSS_SELECTOR, "input[placeholder='Speed']")[i].send_keys(stat["name"])
                    max_field = self._find_elements_timeout(By.CSS_SELECTOR, "input[placeHolder='Max']")[i]
                    max_field.send_keys(Keys.CONTROL, "a")
                    max_field.send_keys(stat["max"])
                    val_field = self._find_elements_timeout(By.CSS_SELECTOR, "input[placeHolder='Min']")[i]
                    val_field.send_keys(Keys.CONTROL, "a")
                    val_field.send_keys(stat["value"])

                    self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Add more").click()

                self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Save").click()

            if not asset_options.get_unlockable_content() == "": # If there is unlockable content, set it
                content_check = self._find_element_timeout(By.CSS_SELECTOR, "input[id='unlockable-content-toggle']")
                self.driver.execute_script('arguments[0].click();', content_check)
                self._find_element_timeout(By.CSS_SELECTOR, "textarea[placeholder='Enter content (access key, code to redeem, link to a file, etc.)']").send_keys(asset_options.get_unlockable_content())

            if asset_options.get_explicit(): # If the asset is explicit, flip the switch
                explicit_check = self._find_element_timeout(By.CSS_SELECTOR, "input[id='explicit-content-toggle']")
                self.driver.execute_script('arguments[0].click();', explicit_check)

            if asset_options.get_supply() > 1: # If the asset has a supply greater than 1, set it
                supply_field = self._find_element_timeout(By.CSS_SELECTOR, "input[id='supply']")
                supply_field.send_keys(Keys.CONTROL, "a")
                supply_field.send_keys(asset_options.get_supply())

            if asset_options.get_blockchain() == "Polygon": # If the asset is on Polygon, set the blockchain
                chain_input = self._find_element_timeout(By.CSS_SELECTOR, "input[id='chain']")
                chain_input.find_element(By.XPATH, "..").click()
                self._find_element_timeout(By.CSS_SELECTOR, "div[id='tippy-9']").click()

            self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Create").click() # Click the create button

            if self._find_element_content_timeout(By.CSS_SELECTOR, "h4", "You created " + asset.get_name() + "!", timeout=15) is not None: # Check if the asset was created successfully
                asset.set_listed_link(self.driver.current_url)
                return self.driver.current_url
            else:
                raise Exception("Failed to create asset")

        except Exception as e:
            print("Error:", e)
            return False

    def sell_asset(self, asset_link:str, price:float, start_date:datetime = None, end_date:datetime = None):
        """
        Sell an uploaded asset from the given URL.

        Args:
            asset_link (str): The URL of the asset to sell.
            price (float): The price to sell the asset for.
            start_date (datetime, optional): The start date of the sale.
            end_date (datetime, optional): The end date of the sale.

        Returns:
            True if the asset was sold successfully, False otherwise.
        """
        try:
            sell_link = asset_link

            if asset_link.endswith("/"):
                sell_link += "sell"
            elif asset_link.endswith("/sell"):
                pass
            else:
                sell_link += "/sell"

            self.driver.get(sell_link) # Open the asset's sell page in the browser

            self._find_element_timeout(By.CSS_SELECTOR, "input[name='price']").send_keys(str(price)) # Set the price

            if start_date is not None and end_date is not None: # If there are start and end dates, set them
                self._find_element_timeout(By.CSS_SELECTOR, "button[id='duration']").click() # Click the duration button

                date_inputs = self._find_elements_timeout(By.CSS_SELECTOR, "input[type='date']") # Get the date inputs
                start_date_field = date_inputs[0]
                end_date_field = date_inputs[1]

                start_date_field.click() # Enter the start date
                start_date_field.send_keys(str(start_date.month).zfill(2))
                start_date_field.send_keys(str(start_date.day).zfill(2))

                end_date_field.click() # Enter the end date
                end_date_field.send_keys(str(end_date.month).zfill(2))
                end_date_field.send_keys(str(end_date.day).zfill(2))

                start_time_field = self._find_element_timeout(By.CSS_SELECTOR, "input[id='start-time']") # Get the time fields
                end_time_field = self._find_element_timeout(By.CSS_SELECTOR, "input[id='end-time']")

                start_time_field.click() # Enter the start time

                start_hour = start_date.hour # The datetime hour is not how OpenSea interprets the hour, so we need to convert it

                if start_hour == 0: # If the hour is 0, it is 12 AM
                    start_hour = 12
                elif start_hour > 12: # If the hour is greater than 12, it is PM
                    start_hour -= 12

                start_time_field.send_keys(str(start_hour).zfill(2))
                start_time_field.send_keys(str(start_date.minute).zfill(2))

                if start_date.hour < 12: # Enter AM/PM
                    start_time_field.send_keys("a")
                else:
                    start_time_field.send_keys("p")

                end_time_field.click() # Enter the end time

                end_hour = end_date.hour # The datetime hour is not how OpenSea interprets the hour, so we need to convert it

                if end_date.hour == 0: # If the hour is 0, it is 12 AM
                    end_hour = 12
                elif end_date.hour > 12: # If the hour is greater than 12, it is PM
                    end_hour -= 12

                end_time_field.send_keys(str(end_hour).zfill(2))
                end_time_field.send_keys(str(end_date.minute).zfill(2))

                if end_date.hour < 12: # Enter AM/PM
                    end_time_field.send_keys("a")
                else:
                    end_time_field.send_keys("p")

                self._find_element_timeout(By.CSS_SELECTOR, "input[name='price']").click() # Click the price field to escape the duration box

            self._find_element_timeout(By.CSS_SELECTOR, "button[type='submit']").click() # Click the sell button

            before_windows = self.driver.window_handles # Get existing window handles
            main_window = self.driver.current_window_handle # The main window handle

            self._find_element_content_timeout(By.CSS_SELECTOR, "button[type='button']", "Sign").click() # Click the sign button

            sign_window = None # The sign window handle. A new window is opened by MetaMask for signing the transaction
            loop_count = 0

            while sign_window is None and loop_count < 15:
                time.sleep(0.5)
                loop_count += 1

                after_windows = self.driver.window_handles

                for window in after_windows: # Check for a new window handle
                    if window not in before_windows:
                        sign_window = window
                        break

            if sign_window is None:
                raise Exception("Failed to find transaction sign window") # If the sign window was not found, raise an exception

            self.driver.switch_to.window(sign_window) # Focus on the sign window

            self._find_element_timeout(By.CSS_SELECTOR, "button[data-testid='request-signature__sign']").click() # Click the sign button

            self.driver.switch_to.window(main_window) # Focus on the main window

            if self._find_element_content_timeout(By.CSS_SELECTOR, "h4", "Your NFT is listed!", timeout=15) is not None: # Check if the asset was sold successfully
                return True
            else:
                raise Exception("Failed to sell asset")

        except Exception as e:
            print("Error:", e)
            return False

    def get_session_data(self):
        """
        Returns the session data for this OSSBrowser instance. Used for reconnecting instead
        of opening a new browser.

        Returns:
            dict: The session data, containing the command_executor_url and session_id
        """
        return {"command_executor_url": self.driver.command_executor._url, "session_id": self.driver.session_id}

    def close(self):
        """
        Closes the browser.
        """
        self.driver.quit()