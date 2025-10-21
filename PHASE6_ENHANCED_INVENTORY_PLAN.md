# Phase 6: Enhanced Inventory State - Implementation Plan

## Overview
Transform the basic inventory screen into a full Pokédex viewer with sorting, filtering, and a beautiful grid display of all 151 Pokémon!

---

## 🎯 Goals

### **Current Inventory State:**
- Shows only: Gold balance and owned count (79/151)
- Press Space to open gacha
- Press ESC to quit

### **Target Enhanced Inventory:**
- **Full 151 Pokémon Grid** (scrollable)
- **Sort Options** (Pokédex #, Rarity, Count)
- **Filter Options** ("Owned Only" checkbox)
- **Pokemon Tiles** showing:
  - Sprite (grayed if not owned)
  - Name
  - Types
  - Rarity border
  - Owned count badge (x3, x5, etc.)
- **Header** with gold, progress, and buttons

---

## 📋 Detailed Implementation Steps

### **Step 1: UI Layout Design**

```
┌─────────────────────────────────────────────────────┐
│  POKÉDEX                    [💰] 15,000   79/151    │
│  ┌────┐ ┌────┐ ┌────┐        [OPEN GACHA] [RESET]  │
│  │ # ▼│ │RAR▼│ │CNT▼│   [✓] Owned Only             │
│  └────┘ └────┘ └────┘                               │
├─────────────────────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ 001 │ │ 002 │ │ 003 │ │ 004 │ │ 005 │ │ 006 │  │ 
│  │Bulb │ │Ivys │ │Venu │ │Char │ │Char │ │Char │  │
│  │saur │ │ aur │ │saur │ │mand.│ │mele.│ │izard│  │
│  │ x2  │ │ --- │ │ x1  │ │ --- │ │ x1  │ │ --- │  │ <- Scrollable
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │    Grid
│  ... (more rows, 6 per row)                         │
│  ... scrolls down to 151                            │
└─────────────────────────────────────────────────────┘
Press ESC to quit
```

### **Step 2: Create Scrollable Grid Component**

**File**: `src/ui/scrollable_grid.py`

Features:
- Renders Pokemon tiles in a grid
- Handles mouse wheel scrolling
- Calculates visible rows
- Smooth scroll offset

### **Step 3: Create Sort Button Component**

**File**: `src/ui/sort_button.py`

Features:
- Shows label (e.g., "# ▼")
- Three states: None, Ascending (▲), Descending (▼)
- Click to cycle through states
- Visual indication of active sort

### **Step 4: Create Checkbox Component**

**File**: `src/ui/checkbox.py` (already planned, now implement it)

Features:
- Label text ("Owned Only")
- Checked/unchecked visual
- Click to toggle
- Callback on change

### **Step 5: Enhance PokemonTile for Inventory**

Update `src/ui/pokemon_tile.py`:
- Support "grayed out" mode for unowned Pokemon
- Show "???" for unowned names (optional)
- Handle empty/missing sprite gracefully

### **Step 6: Rewrite InventoryState**

**File**: `src/states/inventory_state.py`

New features:
- Initialize all UI components (sort buttons, checkbox, grid, buttons)
- Implement sorting logic (by #, rarity, count)
- Implement filtering logic (owned only)
- Handle scrolling
- Render full layout

---

## 🎨 Visual Specifications

### **Pokemon Tile (Inventory Mode)**
- **Size**: 100x120 pixels
- **Owned**: Full color, rarity border, count badge (if > 1)
- **Not Owned**: Grayed out (50% opacity), dashed border, no count

### **Grid Layout**
- **Columns**: 6 tiles per row
- **Spacing**: 10px horizontal, 10px vertical
- **Scrollable Area**: 480px tall (4 rows visible at once)
- **Total Rows**: 26 rows (151 Pokemon ÷ 6 = 25.16 → 26)

### **Sort Buttons**
- **Size**: 60x40 pixels each
- **States**: 
  - Inactive: Gray background
  - Ascending: Green with ▲
  - Descending: Green with ▼
- **Options**:
  - "#" - Pokédex number
  - "RAR" - Rarity (Common → Legendary)
  - "CNT" - Owned count (most → least)

### **Checkbox**
- **Size**: 20x20 box + label
- **Checked**: Green checkmark
- **Unchecked**: Empty box

---

## 📝 Implementation Order

1. ✅ **Create Checkbox Component** (`src/ui/checkbox.py`)
2. ✅ **Create Sort Button Component** (`src/ui/sort_button.py`)
3. ✅ **Create Scrollable Grid Component** (`src/ui/scrollable_grid.py`)
4. ✅ **Update PokemonTile** for grayed-out mode
5. ✅ **Rewrite InventoryState** with full layout
6. ✅ **Test and Polish** scrolling, sorting, filtering

---

## 🔧 Technical Details

### **Sorting Logic**

```python
def _sort_pokemon(self, pokemon_list, sort_by, ascending):
    """Sort Pokemon based on criteria"""
    if sort_by == "number":
        return sorted(pokemon_list, key=lambda p: p.get_pokedex_num(), reverse=not ascending)
    elif sort_by == "rarity":
        rarity_order = {"Common": 0, "Uncommon": 1, "Rare": 2, "Epic": 3, "Legendary": 4}
        return sorted(pokemon_list, key=lambda p: rarity_order.get(p.rarity, 0), reverse=not ascending)
    elif sort_by == "count":
        return sorted(pokemon_list, key=lambda p: self.game_data.pokemon_owned.get(p.number, 0), reverse=not ascending)
    return pokemon_list
```

### **Filtering Logic**

```python
def _filter_pokemon(self, pokemon_list, owned_only):
    """Filter Pokemon based on criteria"""
    if owned_only:
        return [p for p in pokemon_list if self.game_data.has_pokemon(p.number)]
    return pokemon_list
```

### **Scrolling Logic**

```python
# In handle_events
if event.type == pygame.MOUSEWHEEL:
    self.scroll_offset -= event.y * 30  # 30 pixels per scroll
    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
```

---

## 🎯 Success Criteria

When Phase 6 is complete:
- ✅ Can see all 151 Pokemon in a scrollable grid
- ✅ Can sort by #, rarity, or count (ascending/descending)
- ✅ Can filter to show only owned Pokemon
- ✅ Unowned Pokemon appear grayed out
- ✅ Owned Pokemon show count badges
- ✅ Smooth mouse wheel scrolling
- ✅ Can open gacha from inventory
- ✅ Visual polish and responsiveness

---

## 📊 Estimated Components

### **New Files (3)**
1. `src/ui/checkbox.py` (~80 lines)
2. `src/ui/sort_button.py` (~120 lines)
3. `src/ui/scrollable_grid.py` (~150 lines)

### **Modified Files (2)**
4. `src/ui/pokemon_tile.py` - Add grayed-out mode (~30 lines added)
5. `src/states/inventory_state.py` - Complete rewrite (~400 lines)

### **Total New Code**: ~780 lines

---

## ⏱️ Time Estimate

- Checkbox component: 10 minutes
- Sort button component: 15 minutes
- Scrollable grid component: 20 minutes
- Update PokemonTile: 10 minutes
- Rewrite InventoryState: 30 minutes
- Testing and polish: 15 minutes

**Total**: ~1.5 hours of implementation

---

## 🚀 Let's Begin!

Ready to transform the inventory into a beautiful Pokédex viewer! 

Shall we start with Step 1 (Checkbox component)?

