"""
Item data structure
"""

class Item:
    """Represents a game item"""
    
    # Abbreviated name mappings for items that are too long
    ABBREVIATIONS = {
        "Master Ball": "M.Ball",
        "Ultra Ball": "U.Ball",
        "Great Ball": "G.Ball",
        "Poké Ball": "P.Ball",
        "Moon Stone": "MoonStn",
        "Burn Heal": "BrnHeal",
        "Ice Heal": "IceHeal",
        "Awakening": "Awaken",
        "Parlyz Heal": "PrzHeal",
        "Full Restore": "FullRes",
        "Max Potion": "MaxPotn",
        "Hyper Potion": "HyprPtn",
        "Super Potion": "SuprPtn",
        "Escape Rope": "EscRope",
        "Fire Stone": "FireStn",
        "Thunder Stone": "ThndrSt",
        "Water Stone": "WatrStn",
        "Rare Candy": "RrCandy",
        "X Accuracy": "X Accur",
        "Leaf Stone": "LeafStn",
        "Poké Doll": "P.Doll",
        "Full Heal": "FullHel",
        "Max Revive": "MaxRevv",
        "Guard Spec.": "GrdSpec",
        "Super Repel": "SuprRpl",
        "Max Repel": "MaxRepl",
        "Dire Hit": "DireHit",
        "X Attack": "X Attk",
        "X Defend": "X Def",
        "X Special": "X Spec",
        "Fresh Water": "FrshWtr",
        "Soda Pop": "SodaPop",
        "Lemonade": "Lemonad",
    }
    
    def __init__(self, number: str, name: str, index: int, category: str, 
                 value: int, rarity: str, weight: int, icon: str):
        """
        Initialize Item
        
        Args:
            number: Item number (1-79)
            name: Item name
            index: Gen 1 index number
            category: Item category (ball, medicine, etc.)
            value: Item value in Pokédollars
            rarity: Rarity tier
            weight: Drop weight
            icon: Icon filename
        """
        self.number = str(number).zfill(3)  # e.g., "001"
        self.name = name
        self.index = index
        self.category = category
        self.value = value
        self.rarity = rarity
        self.weight = weight
        self.icon = icon
    
    def get_display_name(self, max_length: int = 7) -> str:
        """
        Get display name for item, abbreviated if necessary
        
        Args:
            max_length: Maximum length for display name
            
        Returns:
            Abbreviated name if available and original is too long, otherwise original name
        """
        # Use abbreviation if available
        if self.name in self.ABBREVIATIONS:
            return self.ABBREVIATIONS[self.name]
        
        # If name is short enough, return as-is
        if len(self.name) <= max_length:
            return self.name
        
        # Otherwise truncate with ellipsis
        return self.name[:max_length-1] + "."
    
    def __repr__(self):
        return f"Item({self.number}, {self.name}, {self.rarity})"
    
    def get_icon_path(self) -> str:
        """Get full path to item icon"""
        return f"Assets/Sprites/Items/{self.icon.split('/')[-1]}"

