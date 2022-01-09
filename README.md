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
	sell_result = browser.sell_asset(result, 1) # List the NFT for sale using its URL for the price of 1 ETH.

	if not result:
		print("Sell failed.")
	else:
		print("Asset listed for sale.")
```

## Future Features
- Better error messages
- Documentation
- Example programs
