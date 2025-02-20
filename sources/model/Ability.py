class CrawlingDTO:
    def __init__(self, name: str, desc: str, tribes: str):
        self.name = name
        self.desc = desc
        self.tribes = tribes
    
    def __repr__(self):
        return f"name: {self.name} desc: {self.desc} tribes: {self.tribes}"
    

class Ability:
    def __init__(self, name: str, description: str, tribes: str, tip: str = "", category: str = "", image: str = "", new: bool = False):
        self.name = name
        self.description = description
        self.tribes = tribes
        self.tip = tip
        self.category = category
        self.image = image
        self.new = new

    def __repr__(self):
        return f"name: {self.name}"