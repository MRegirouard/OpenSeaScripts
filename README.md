# OpenSeaScripts
A suite of Python scripts for using OpenSea where API's are limited. OSS uses Selenium to control a Google Chrome window to find, fetch, and interact with HTML elements on OpenSea's website.

## Application
This Python module is intended for uploading and listing for sale many NFT's to OpenSea. Their API does not support uploading, and to avoid manually uploading collections of potentially hundreds of NFT's, this module can be used. I used this to upload my collection of [Monkey Men](https://opensea.io/collection/5000-monkey-men).
<br><br>
This module supports all asset options on OpenSea using the AssetOptions class. Properties, levels, and stats will all be added to your NFT and displayed on the page just like any other NFT.

## Installation
```bash
pip install OpenSeaScripts
```
You will also need Google Chrome.

## Usage
```python3
from OpenSeaScripts.AssetOptions import AssetOptions
from OpenSeaScripts.OSSBrowser import OSSBrowser
import datetime

# Create a new browser. This will open a Chrome window.
browser = OSSBrowser()

# Use the information displayed here to avoid signing in to MetaMask
# each time the program is run:
print("Browser info:", browser.get_session_data())

# Create a new asset object with the file NFT.png, titled "NFT"
my_asset = AssetOptions("NFT.png", "NFT")
my_asset.set_description("An NFT.")
my_asset.set_external_link("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Add attributes to your NFT
my_asset.add_property("Type", "Image")
my_asset.add_property("Color", "Blue")
my_asset.add_level("Number", "1", "4")
my_asset.add_stat("Size", "50", "100")

# Set the asset to upload on the Polygon blockchain
my_asset.set_blockchain("Polygon") # "Ethereum" also works

# You will need to install the MetaMask extension in the browser 
# and connect your wallet to OpenSea before uploading assets.
input("Please sign in to OpenSea using MetaMask. Press Enter when ready... ")

# Perform the uploading process in the browser window
result = browser.upload_asset(my_asset)

# "result" will be False if the upload failed, or the OpenSea URL of the NFT if successful.

if not result:
	print("Upload failed.")
else:
	print("Uploaded asset. URL:", result)

	sell_start = datetime.datetime(2022, 1, 13, 0, 0) # Sell duration start datetime object.
	sell_end   = datetime.datetime(2022, 4, 13, 0, 0) # Sell duration end datetime object.

	# The sell_start must be in the future but within 30 days.
	# The sell_end must be past sell_start, but no more than 6 months later.

	sell_result = browser.sell_asset(result, 1, sell_start, sell_end) # List the NFT for sale using its URL for the price of 1 ETH, and with the start and end sell times above

	if not result:
		print("Sell failed.")
	else:
		print("Asset listed for sale.")
```
### :warning: Sell Duration Limitations
The sell duration settings may not work as expected. OpenSea's date entry method is quite complicated and this was difficult to overcome in the programming. However, it still may not work well so it is recommended you keep an eye on it or at least test it out with some dates. Here are a few things to keep in mind:
- Start dates must be in the future, but no more than 30 days in the future.
- End dates must be past the start date, but no more than 6 months past the start date.
- The Python module does not check the dates you give it at all, but they will fail on OpenSea. The `sell_asset` function will return `False` in this case.
- Sometimes, the date selector gets "stuck" on a previous date entered. It's really inconsistent but changing the date on the calendar below the input fields sometimes helps.
- This may not work for all localities. OpenSea may change the date input order or not in different regions, but this module assumes that OpenSea uses MM/DD/YY as is done in the US.
- This may not work when dates are in a different year than right now. This feature is currently impossible to test as OpenSea doesn't allow edits to year field as it is currently January and the next year is more than the maximum of 6 months away. OpenSeaScripts does not do anything with the year value you give it, but there's a chance OpenSea figures it out automatically.

## Easily Reconnect to Existing Browser Session
Selenium allows you to connect to a previously opened browser session. You can use this to avoid having to sign in to MetaMask each time you run a script to upload NFT's. However, certain things must be done to ensure that the first session stays open.
<br>
I recommend doing this with two different Python scripts. The first will initailize the browser, print the connection info, and then keep the session open. The second will actually connect to the browser and can be restarted without closing the browser session.

### StartBrowser.py
```python3
from OpenSeaScripts.OSSBrowser import OSSBrowser

browser = OSSBrowser()
print("Browser info:", browser.get_session_data()) # Use this info to reconnect

# Keep the browser open for reconnecting
while True:
	pass
```

### ConnectToBrowser.py
```python3
from OpenSeaScripts.OSSBrowser import OSSBrowser

# Browser info from StartBrowser.py
command_executor_url = ""
session_id = ""
browser = OSSBrowser(command_executor_url, session_id)

# Upload / Sell Assets
```

> :warning: I have noticed some issues with opening and then reconnecting to a browser in the Visual Studio Code console. I recommend you run scripts that open browser windows in a different terminal winodw.

## Future Features
- Better error messages
- Documentation
- Example programs
