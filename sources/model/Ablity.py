import enum

class Ablity:
    def __init__(self, name: str, desc: str, tribes: str):
        self.name = name
        self.desc = desc
        self.tribes = tribes
    def __repr__(self):
        return f"name: {self.name} desc: {self.name} tribes: {self.tribes}"