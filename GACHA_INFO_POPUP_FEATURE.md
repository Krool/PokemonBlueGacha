# Gacha Info Popup Feature

## Overview
A new INFO button has been added to the gacha purchase screen that displays all possible Pokémon outcomes and their exact drop rates for the selected gacha machine.

## Features Implemented

### 1. INFO Button
- **Location**: Positioned to the left of the 1-PULL button on the gacha purchase screen
- **Size**: 100x50 pixels
- **Color**: Blue theme (50, 100, 150) with hover effect
- **Vertically aligned** with the pull buttons for a clean layout

### 2. Drop Rates Popup
When clicked, the INFO button opens a popup displaying:
- **Title**: Shows which machine's rates are being displayed (e.g., "RED MACHINE - DROP RATES")
- **Scrollable List**: All Pokémon available in that machine
- **Information per Pokémon**:
  - Pokémon number (e.g., #001)
  - Pokémon name
  - Exact drop rate percentage (e.g., 0.5432%)
  - Rarity indicator (colored dot)

### 3. Rarity Color Coding
Each Pokémon has a colored dot indicating its rarity:
- **White**: Common
- **Green**: Uncommon
- **Blue**: Rare
- **Purple**: Epic
- **Orange**: Legendary

### 4. Scrolling Support
- Uses mouse wheel to scroll through the list
- Scrollbar appears on the right when content exceeds visible area
- Smooth scrolling experience

### 5. Drop Rate Calculation
The popup accurately calculates drop rates using the two-step gacha system:
1. First, rolls for rarity based on rarity weights
2. Then, rolls for specific Pokémon within that rarity
3. Combined probability shown as a percentage

Formula: `(Rarity Probability) × (Pokémon Probability within Rarity) × 100`

### 6. Error Handling
- Comprehensive error handling to prevent crashes
- Displays "No drop rate data available" if calculation fails
- Debug logging for troubleshooting
- Try-catch blocks around all calculations

## Technical Implementation

### New File: `src/ui/gacha_info_popup.py`
A new UI component class that:
- Accepts the machine name, Pokémon list, rarities dictionary, and font manager
- Calculates all drop rates on initialization
- Handles its own events (scrolling, clicking, closing)
- Renders a semi-transparent overlay with the popup content

### Updated: `src/states/gacha_buy_state.py`
- Added `self.info_popup = None` to track popup state
- Created INFO button with proper positioning
- Implemented `_show_info()` method to create the popup
- Updated `handle_events()` to prioritize popup events when visible
- Updated `update()` and `render()` methods to handle the popup

### Key Methods

#### `_calculate_drop_rates()`
```python
def _calculate_drop_rates(self, pokemon_list, rarities_dict, version):
    # Filters Pokémon available in the version
    # Calculates total rarity weight
    # For each Pokémon:
    #   - Gets its rarity probability
    #   - Calculates probability within rarity
    #   - Combines for final drop rate
    # Returns sorted list of (pokemon, drop_rate) tuples
```

#### Event Flow
1. User clicks INFO button
2. `_show_info()` creates `GachaInfoPopup` instance
3. Popup calculates all drop rates for selected machine
4. Popup renders over the gacha screen
5. User can scroll to see all Pokémon
6. User clicks CLOSE or clicks outside to dismiss

## User Experience Benefits
- **Transparency**: Players can see exact odds for all Pokémon
- **Informed Decisions**: Compare rates across different machines
- **Version Exclusives**: Easily identify which Pokémon are unavailable (0% rate)
- **Rarity Understanding**: Color-coded indicators help identify valuable Pokémon

## Version-Specific Behavior
- Red Machine: Shows only Pokémon available in Red version
- Blue Machine: Shows only Pokémon available in Blue version
- Yellow Machine: Shows all Pokémon with doubled legendary rates
- Version exclusives automatically show 0% rate (filtered out)

## Future Enhancements (Optional)
- Add sorting options (by rarity, by rate, by number)
- Add filtering (show only specific rarities)
- Add search functionality
- Display cumulative percentages
- Show "pity system" information if implemented
- Export rates to CSV file

