class AssetOptions:
    preview_extensions = ["mp4", "webm", "mp3", "wav", "ogg", "glb", "gltf"]

    def __init__(self, asset_path, name):
        self.asset_path = asset_path
        self.preview_path = ""
        self.name = name
        self.external_link = ""
        self.description = ""
        self.properties = []
        self.levels = []
        self.stats = []
        self.unlockable_content = ""
        self.explicit = False
        self.supply = 1
        self.blockchain = "Ethereum"
        self.listed_link = ""

    def needs_preview(file_extension):
        return file_extension.lower() in AssetOptions.preview_extensions

    def set_asset_path(self, asset_path):
        if asset_path == "" or not isinstance(asset_path, str):
            raise ValueError("Asset path must be a non-empty string")
        else:
            self.asset_path = asset_path

        return self

    def get_asset_path(self):
        return self.asset_path

    def set_preview_path(self, preview_path):
        if preview_path == "" or not isinstance(preview_path, str):
            raise ValueError("Preview path must be a non-empty string")
        else:
            self.preview_path = preview_path

        return self

    def get_preview_path(self):
        return self.preview_path

    def set_name(self, name):
        if name == "" or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        else:
            self.name = name

        return self

    def get_name(self):
        return self.name

    def set_external_link(self, external_link):
        if not isinstance(external_link, str):
            raise ValueError("External link must be a string")
        else:
            self.external_link = external_link

        return self

    def get_external_link(self):
        return self.external_link

    def set_description(self, description):
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        else:
            self.description = description

        return self

    def get_description(self):
        return self.description

    def add_property(self, name, value):
        if name == "" or not isinstance(name, str) or value == "" or not isinstance(value, str):
            raise ValueError("Property name and value must be non-empty strings")
        else:
            self.properties.append({"name": name, "value": value})
        
        return self

    def get_properties(self):
        return self.properties

    def add_level(self, name, value, max_value):
        if name == "" or not isinstance(name, str) or value == "" or not isinstance(value, str) or max_value == "" or not isinstance(max_value, str):
            raise ValueError("Property name and value must be non-empty strings")
        else:
            self.levels.append({"name": name, "value": value, "max": max_value})

        return self

    def get_levels(self):
        return self.levels

    def add_stat(self, name, value, max_value):
        if name == "" or not isinstance(name, str) or value == "" or not isinstance(value, str) or max_value == "" or not isinstance(max_value, str):
            raise ValueError("Property name and value must be non-empty strings")
        else:
            self.stats.append({"name": name, "value": value, "max": max_value})

        return self

    def get_stats(self):
        return self.stats

    def set_unlockable_content(self, unlockable_content):
        if not isinstance(unlockable_content, str):
            raise ValueError("Unlockable content must be a string")
        else:
            self.unlockable_content = unlockable_content

        return self

    def get_unlockable_content(self):
        return self.unlockable_content

    def set_explicit(self, explicit):
        if not isinstance(explicit, bool):
            raise ValueError("Explicit must be a boolean")
        else:
            self.explicit = explicit

        return self

    def get_explicit(self):
        return self.explicit

    def set_supply(self, supply):
        if not isinstance(supply, int):
            raise ValueError("Supply must be an integer")
        else:
            self.supply = supply

        return self

    def get_supply(self):
        return self.supply

    def set_blockchain(self, blockchain):
        if not isinstance(blockchain, str):
            raise ValueError("Blockchain must be a string")
        else:
            if blockchain[0].lower() == "e" or blockchain[0].lower() == "":
                self.blockchain = "Ethereum"
            else:
                self.blockchain = "Polygon"

        return self

    def get_blockchain(self):
        return self.blockchain

    def set_listed_link(self, listed_link):
        self.listed_link = listed_link
        return self
    
    def get_listed_link(self):
        return self.listed_link