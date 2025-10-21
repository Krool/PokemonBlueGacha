# Pokémon Blue Gacha - Implementation Plan

## Technology Stack Decision
**Framework**: Pygame (Python game framework)
- Good for 2D games with sprite management
- Easy audio/image handling
- Simple state management
- Cross-platform

---

## Phase 1: Project Setup & Core Infrastructure

### 1.1 Project Structure Setup
- Create proper directory structure for Python/Pygame project
- Set up virtual environment
- Create requirements.txt with dependencies
- Verify all asset files are in correct locations

### 1.2 Data Loading System
- Create CSV parser classes
- Load pokemon_gen1.csv into data structures
- Load pokemon_types.csv for type colors/icons
- Load rarity_drop_weights.csv for gacha logic
- Create data validation to ensure all files load correctly

### 1.3 Save System
- Design JSON save file structure
- Create SaveManager class
- Implement save/load functionality
- Handle first-time player initialization (0 gold, no Pokémon)

### 1.4 Game State Manager
- Create base GameState class
- Implement state switching mechanism
- Create event handling system
- Set up main game loop

---

## Phase 2: Asset Management System

### 2.1 Image Loading
- Load all 151 Pokémon sprites
- Load type icons (15 types)
- Load UI images (logo, gacha machine)
- Create sprite caching system
- Handle missing images gracefully

### 2.2 Audio System
- Initialize pygame.mixer
- Load background music
- Load roll sound effects (roll1, roll2, roll3, legendary)
- Create audio manager for playing/stopping sounds
- Implement looping background music

### 2.3 Resource Manager
- Create centralized resource manager class
- Provide easy access to images/sounds/data
- Handle resource cleanup

---

## Phase 3: UI Component Library

### 3.1 Basic UI Components
- Button component (with hover/click states)
- Text label component
- Checkbox component
- Scrollable list component
- Progress bar component
- Popup/modal component

### 3.2 Custom UI Components
- Pokémon tile component
  - Image rendering
  - Type icons (stacked vertically)
  - Owned count display
  - Background coloring by type
  - Rarity outline with glow effect
  - "NEW!" badge
- Sort button component (with icon)
- Gold display component

### 3.3 UI Utilities
- Color conversion (hex to RGB)
- Text rendering utilities
- Layout helpers (centering, positioning)
- Glow/shimmer effect shader

---

## Phase 4: Gacha Logic System

### 4.1 Gacha Roll Engine
- Implement two-step weighted random selection
  1. Rarity roll (based on rarity weights)
  2. Pokémon roll (based on individual weights within rarity)
- Create GachaRoller class
- Handle single pull (1 result)
- Handle 10-pull (10 results)

### 4.2 Inventory Manager
- Track owned Pokémon with counts
- Add Pokémon to inventory
- Check if Pokémon is newly acquired
- Get owned count for specific Pokémon
- Reset inventory function

### 4.3 Currency Manager
- Track gold balance
- Deduct gold for pulls
- Add gold (cheat button)
- Check if player can afford pulls

---

## Phase 5: Game States Implementation

### 5.1 Loading State
- Display logo.png
- Animated progress bar
- Auto-transition to Inventory after loading completes
- Start background music

### 5.2 Inventory State
- Display scrollable list of all 151 Pokémon
- Render Pokémon tiles with all details
- Implement sort buttons (#, rarity, count)
- Implement sort order reversal
- Implement "Owned" filter checkbox
- Display "No pokemon owned" when filtered list is empty
- Three action buttons (Gacha, Reset, Quit)
- Handle user interactions

### 5.3 GachaBuy State
- Display gacha machine image
- Show gold balance
- Two roll buttons (1-pull, 10-pull) with costs
- Check if player can afford
- Show "Not enough gold" popup if needed
- Return to Inventory button
- Transition to GachaAnimation on valid purchase

### 5.4 GachaAnimation State
- Perform gacha rolls (store results)
- Animate gacha machine:
  - Shake based on rarity
  - Colorize by rarity
  - Scale intensity/duration by rarity
  - Add rotation for higher rarities
- Play appropriate sound effect
- Allow click-to-skip
- Auto-transition to GachaOutcome after animation

### 5.5 GachaOutcome State
- Display rolled Pokémon in grid (1 or 10)
- Show tiles with "NEW!" badges where appropriate
- Update inventory (add Pokémon)
- Save game after updating inventory
- Two buttons:
  - Roll Again (same type/cost)
  - Return to Inventory
- Handle "not enough gold" popup for Roll Again

---

## Phase 6: Polish & Testing

### 6.1 Visual Polish
- Implement glow/shimmer effects on rarity outlines
- Smooth animations for state transitions
- Button hover effects
- Loading bar animation tweening

### 6.2 Audio Polish
- Smooth music looping
- Volume balancing
- Fade in/out effects

### 6.3 Bug Testing
- Test all user flows
- Test edge cases (0 gold, all Pokémon owned, etc.)
- Test save/load persistence
- Test sort/filter combinations

### 6.4 Performance Optimization
- Optimize rendering for 151 Pokémon tiles
- Implement tile pooling for scrolling
- Cache rendered text
- Minimize redundant calculations

---

## Phase 7: Final Integration

### 7.1 End-to-End Testing
- Play through entire game flow
- Verify all states work correctly
- Test save persistence across launches
- Verify all 151 Pokémon can be obtained

### 7.2 Code Cleanup
- Remove debug code
- Add comments to complex sections
- Organize imports
- Create documentation

### 7.3 Build & Package
- Create standalone executable (if needed)
- Test on clean environment
- Create user instructions

---

## Implementation Order Priority

1. **Phase 1**: Foundation (critical path)
2. **Phase 2**: Assets (needed for UI)
3. **Phase 4**: Gacha Logic (core mechanic)
4. **Phase 3**: UI Components (needed for states)
5. **Phase 5**: Game States (assembly)
6. **Phase 6**: Polish (final touches)
7. **Phase 7**: Testing & Packaging

---

## Next Steps

After reviewing this high-level plan, we'll drill down into detailed sub-steps for each phase, including:
- Specific class designs
- Method signatures
- Data structures
- Code organization
- File naming conventions

**Ready to detail out each phase?**

