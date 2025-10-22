"""
CSV loading utilities with error handling
"""
import csv
import os
from typing import List, Dict
from .pokemon_data import Pokemon
from .type_data import PokemonType
from .rarity_data import Rarity
from .gacha_machine_data import GachaMachine
from .item_data import Item


class CSVLoadError(Exception):
    """Custom exception for CSV loading errors"""
    pass


class CSVLoader:
    """Loads game data from CSV files"""
    
    @staticmethod
    def load_pokemon(filepath: str) -> List[Pokemon]:
        """
        Load all Pokémon from CSV
        
        Args:
            filepath: Path to pokemon CSV file
            
        Returns:
            List of Pokemon objects
            
        Raises:
            CSVLoadError: If file not found or data invalid
        """
        if not os.path.exists(filepath):
            raise CSVLoadError(f"Pokemon CSV not found: {filepath}")
        
        pokemon_list = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                expected_headers = ['Number', 'Name', 'Type1', 'Type2', 'Rarity', 'Red_Weight', 'Blue_Weight', 'Yellow_Weight', 'Image']
                if not all(header in reader.fieldnames for header in expected_headers):
                    raise CSVLoadError(f"Pokemon CSV missing required headers. Expected: {expected_headers}")
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                    try:
                        pokemon = Pokemon(
                            number=row['Number'].strip(),
                            name=row['Name'].strip(),
                            type1=row['Type1'].strip(),
                            type2=row['Type2'].strip() if row['Type2'].strip() else None,
                            rarity=row['Rarity'].strip(),
                            red_weight=int(row['Red_Weight']),
                            blue_weight=int(row['Blue_Weight']),
                            yellow_weight=int(row['Yellow_Weight']),
                            image_path=row['Image'].strip()
                        )
                        pokemon_list.append(pokemon)
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid row {row_num} in {filepath}: {e}")
                        continue
                        
        except Exception as e:
            raise CSVLoadError(f"Error reading Pokemon CSV: {e}")
        
        if len(pokemon_list) == 0:
            raise CSVLoadError("No valid Pokemon data loaded")
        
        print(f"✓ Loaded {len(pokemon_list)} Pokémon")
        return pokemon_list
    
    @staticmethod
    def load_types(filepath: str) -> Dict[str, PokemonType]:
        """
        Load all types from CSV
        
        Args:
            filepath: Path to types CSV file
            
        Returns:
            Dictionary of PokemonType objects keyed by type name
            
        Raises:
            CSVLoadError: If file not found or data invalid
        """
        if not os.path.exists(filepath):
            raise CSVLoadError(f"Types CSV not found: {filepath}")
        
        types_dict = {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                expected_headers = ['Type', 'Image', 'Color']
                if not all(header in reader.fieldnames for header in expected_headers):
                    raise CSVLoadError(f"Types CSV missing required headers. Expected: {expected_headers}")
                
                for row in reader:
                    try:
                        poke_type = PokemonType(
                            name=row['Type'].strip(),
                            image_path=row['Image'].strip(),
                            color_hex=row['Color'].strip()
                        )
                        types_dict[poke_type.name] = poke_type
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid type row: {e}")
                        continue
                        
        except Exception as e:
            raise CSVLoadError(f"Error reading Types CSV: {e}")
        
        if len(types_dict) == 0:
            raise CSVLoadError("No valid type data loaded")
        
        print(f"✓ Loaded {len(types_dict)} types")
        return types_dict
    
    @staticmethod
    def load_rarities(filepath: str) -> Dict[str, Rarity]:
        """
        Load all rarities from CSV
        
        Args:
            filepath: Path to rarities CSV file
            
        Returns:
            Dictionary of Rarity objects keyed by rarity name
            
        Raises:
            CSVLoadError: If file not found or data invalid
        """
        if not os.path.exists(filepath):
            raise CSVLoadError(f"Rarities CSV not found: {filepath}")
        
        rarities_dict = {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                expected_headers = ['Rarity', 'Red_Weight', 'Blue_Weight', 'Yellow_Weight', 'Items_Weight', 'Color']
                if not all(header in reader.fieldnames for header in expected_headers):
                    raise CSVLoadError(f"Rarities CSV missing required headers. Expected: {expected_headers}")
                
                for row in reader:
                    try:
                        rarity = Rarity(
                            name=row['Rarity'].strip(),
                            red_weight=int(row['Red_Weight']),
                            blue_weight=int(row['Blue_Weight']),
                            yellow_weight=int(row['Yellow_Weight']),
                            items_weight=int(row['Items_Weight']),
                            color_hex=row['Color'].strip()
                        )
                        rarities_dict[rarity.name] = rarity
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid rarity row: {e}")
                        continue
                        
        except Exception as e:
            raise CSVLoadError(f"Error reading Rarities CSV: {e}")
        
        if len(rarities_dict) == 0:
            raise CSVLoadError("No valid rarity data loaded")
        
        print(f"✓ Loaded {len(rarities_dict)} rarities")
        return rarities_dict
    
    @staticmethod
    def validate_data_integrity(pokemon_list: List[Pokemon], types_dict: Dict[str, PokemonType], 
                                rarities_dict: Dict[str, Rarity]) -> bool:
        """
        Validate that all references in data are valid
        
        Args:
            pokemon_list: List of loaded Pokemon
            types_dict: Dictionary of loaded types
            rarities_dict: Dictionary of loaded rarities
            
        Returns:
            True if all data is valid, raises CSVLoadError otherwise
        """
        issues = []
        
        # Check all Pokemon have valid types
        for pokemon in pokemon_list:
            if pokemon.type1 not in types_dict:
                issues.append(f"{pokemon.name} has invalid Type1: {pokemon.type1}")
            if pokemon.type2 and pokemon.type2 not in types_dict:
                issues.append(f"{pokemon.name} has invalid Type2: {pokemon.type2}")
            if pokemon.rarity not in rarities_dict:
                issues.append(f"{pokemon.name} has invalid rarity: {pokemon.rarity}")
        
        if issues:
            error_msg = "Data integrity issues found:\n" + "\n".join(issues)
            raise CSVLoadError(error_msg)
        
        print("✓ Data integrity validated")
        return True
    
    @staticmethod
    def load_gacha_machines(filepath: str) -> Dict[str, GachaMachine]:
        """
        Load all gacha machines from CSV
        
        Args:
            filepath: Path to gacha machines CSV file
            
        Returns:
            Dictionary of GachaMachine objects keyed by version name
            
        Raises:
            CSVLoadError: If file not found or data invalid
        """
        if not os.path.exists(filepath):
            raise CSVLoadError(f"Gacha machines CSV not found: {filepath}")
        
        machines_dict = {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                expected_headers = ['Name', 'Version', 'Cost_Single', 'Cost_10Pull', 'Description']
                if not all(header in reader.fieldnames for header in expected_headers):
                    raise CSVLoadError(f"Gacha machines CSV missing required headers. Expected: {expected_headers}")
                
                for row in reader:
                    try:
                        machine = GachaMachine(
                            name=row['Name'].strip(),
                            version=row['Version'].strip(),
                            cost_single=int(row['Cost_Single']),
                            cost_10pull=int(row['Cost_10Pull']),
                            description=row['Description'].strip()
                        )
                        machines_dict[machine.version] = machine
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid gacha machine row: {e}")
                        continue
                        
        except Exception as e:
            raise CSVLoadError(f"Error reading Gacha machines CSV: {e}")
        
        if len(machines_dict) == 0:
            raise CSVLoadError("No valid gacha machine data loaded")
        
        print(f"✓ Loaded {len(machines_dict)} gacha machines")
        return machines_dict
    
    @staticmethod
    def load_items(filepath: str) -> List[Item]:
        """
        Load all items from CSV
        
        Args:
            filepath: Path to items CSV file
            
        Returns:
            List of Item objects
            
        Raises:
            CSVLoadError: If file not found or data invalid
        """
        if not os.path.exists(filepath):
            raise CSVLoadError(f"Items CSV not found: {filepath}")
        
        items_list = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                expected_headers = ['Number', 'Name', 'Index', 'Category', 'Value', 'Rarity', 'Weight', 'Icon']
                if not all(header in reader.fieldnames for header in expected_headers):
                    raise CSVLoadError(f"Items CSV missing required headers. Expected: {expected_headers}")
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        item = Item(
                            number=row['Number'].strip(),
                            name=row['Name'].strip(),
                            index=int(row['Index']),
                            category=row['Category'].strip(),
                            value=int(row['Value']),
                            rarity=row['Rarity'].strip(),
                            weight=int(row['Weight']),
                            icon=row['Icon'].strip()
                        )
                        items_list.append(item)
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid row {row_num} in {filepath}: {e}")
                        continue
        
        except Exception as e:
            raise CSVLoadError(f"Error reading Items CSV: {e}")
        
        if len(items_list) == 0:
            raise CSVLoadError("No valid items data loaded")
        
        print(f"✓ Loaded {len(items_list)} items")
        return items_list

