# UI Updates Complete

## Summary
Completed several UI improvements and bug fixes for the Pokemon Blue Gacha prototype.

## Changes Completed

### 1. RECOMMENDED Badge Redesign
**Location**: `src/states/gacha_buy_state.py`

- Moved RECOMMENDED badge from inside button text to a separate bright yellow badge positioned **above** the recommended machine button
- Badge has:
  - Bright yellow background (#FFFF00)
  - Black text for high contrast
  - Border for definition
  - Positioned 30 pixels above the button
  - Width: 160px, Height: 25px
- All machine buttons now consistently display just the machine name without embedded RECOMMENDED text
- Font size is now consistent at 20px for all buttons

### 2. Fixed Missing Pokemon Sprites
**Location**: `data/pokemon_gen1.csv`, `Assets/Sprites/Pokemon/`

Fixed missing images for:
- **#083 Farfetch'd**: Downloaded sprite and updated CSV path to `Assets/Sprites/Pokemon/083_farfetchd.png`
- **#122 Mr. Mime**: Downloaded sprite and updated CSV path to `Assets/Sprites/Pokemon/122_mr-mime.png`

These Pokemon will now display correctly in the Pokedex and during gacha pulls.

### 3. Fixed Insufficient Funds Popup Buttons
**Location**: `src/ui/popup.py`

- **Fixed double text issue**: Removed "+20,000" text from add gold button (was displaying twice)
- **Increased button sizes**: Changed button width from 120px to 220px (100px wider, 50px on each side)
- Add gold button now only shows the currency icon + amount (no duplicate text)
- Both "Add Gold" and "Close" buttons are now 220px wide x 40px tall

### 4. Changed "Inventory" to "Pokédex"
**Location**: `src/states/gacha_outcome_state.py`

- Changed button text from "INVENTORY" to "POKÉDEX" on the outcome screen
- This provides clearer terminology consistent with Pokemon franchise
- Only changed visible UI text, not internal code identifiers

### 5. Info Button Positioning
**Location**: `src/states/inventory_state.py`

- Moved info button 5 pixels left (from `SCREEN_WIDTH - 340` to `SCREEN_WIDTH - 345`)
- Moved reset button 30 pixels right (from `SCREEN_WIDTH - 280` to `SCREEN_WIDTH - 250`)
- This creates exactly 25 pixels of spacing between the two buttons
- Prevents overlap with Pokemon count display

### 6. Stats Popup Height Increase
**Location**: `src/states/inventory_state.py`

- Increased stats popup height from 600px to 650px (50 pixels taller)
- Provides more breathing room for statistics display
- All content remains properly positioned with the new height

## Files Modified
1. `src/states/gacha_buy_state.py` - RECOMMENDED badge redesign
2. `data/pokemon_gen1.csv` - Fixed image paths for #083 and #122
3. `Assets/Sprites/Pokemon/083_farfetchd.png` - NEW: Downloaded sprite
4. `Assets/Sprites/Pokemon/122_mr-mime.png` - NEW: Downloaded sprite
5. `src/ui/popup.py` - Fixed button sizing and double text
6. `src/states/gacha_outcome_state.py` - Changed "INVENTORY" to "POKÉDEX"
7. `src/states/inventory_state.py` - Button positioning and popup sizing

## Testing Recommendations
1. **RECOMMENDED Badge**: Open gacha buy screen and verify the yellow badge appears above the recommended machine
2. **Missing Pokemon**: Check Pokedex for #083 and #122 to confirm sprites appear
3. **Insufficient Funds**: Try to make a pull without enough currency and verify:
   - Button sizes are larger
   - Add gold button shows currency icon + amount only once
4. **Text Changes**: Verify "POKÉDEX" appears on outcome screen button
5. **Button Spacing**: Check inventory screen for proper spacing between Info and Reset buttons
6. **Stats Popup**: Open the info popup and verify it's taller with good content spacing

## Technical Notes
- Pokemon sprite filenames had to match the downloaded file format (lowercase, no special characters)
- The RECOMMENDED badge is rendered in the gacha_buy render() method after buttons are drawn
- Button sizing changes in popup.py affect both single-button and dual-button popups
- Stats popup height is parameterized, making future adjustments easy

