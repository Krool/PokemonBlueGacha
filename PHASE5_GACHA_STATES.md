# Phase 5: Gacha Animation & Outcome States

## Overview
Implement the exciting gacha pull animation and results display to complete the core gameplay loop.

---

## 5.1 GachaAnimation State

### **Purpose**
Show an animated gacha machine shake/effect based on the rarity of the rolled Pokemon, building anticipation before revealing results.

### **Flow**
1. Receives: `version` (Red/Blue/Yellow), `pull_count` (1 or 10), `results` (list of Pokemon)
2. Performs animation based on highest rarity in results
3. Plays sound effect
4. Transitions to GachaOutcome when complete

### **Implementation Details**

#### **Animation System**
```python
class GachaAnimationState(GameState):
    def enter(self, version, pull_count, results):
        self.version = version
        self.pull_count = pull_count
        self.results = results  # List of Pokemon objects
        
        # Determine animation intensity from highest rarity
        self.highest_rarity = self._get_highest_rarity(results)
        self.animation_duration = self._get_duration(self.highest_rarity)
        self.shake_intensity = self._get_intensity(self.highest_rarity)
        
        # Play sound
        self._play_sound(self.highest_rarity)
        
        self.elapsed_time = 0
        self.skipped = False
```

#### **Rarity-Based Animation Parameters**

| Rarity | Duration | Shake Intensity | Rotation | Color Overlay |
|--------|----------|-----------------|----------|---------------|
| Common | 0.5s | Low (±5px) | None | White tint |
| Uncommon | 0.8s | Medium (±10px) | None | Green tint |
| Rare | 1.2s | High (±15px) | Small (±5°) | Blue tint |
| Epic | 1.6s | Very High (±20px) | Medium (±10°) | Purple tint |
| Legendary | 2.0s | Extreme (±30px) | Large (±15°) | Orange glow |

#### **Animation Functions**
```python
def _shake_gacha_machine(self, time_ratio):
    """Calculate shake offset based on time"""
    # Sine wave for smooth shake
    shake_x = sin(time_ratio * 20) * self.shake_intensity
    shake_y = cos(time_ratio * 15) * self.shake_intensity * 0.5
    return shake_x, shake_y

def _rotate_gacha_machine(self, time_ratio):
    """Calculate rotation angle"""
    if self.highest_rarity in ['Rare', 'Epic', 'Legendary']:
        rotation = sin(time_ratio * 10) * rotation_amount
        return rotation
    return 0

def _get_color_overlay(self):
    """Get color tint based on rarity"""
    rarity = self.highest_rarity
    rarity_obj = resource_manager.get_rarity(rarity)
    return rarity_obj.get_color_rgb()
```

#### **Rendering**
```python
def render(self):
    screen.fill(COLOR_BLACK)
    
    # Calculate animation progress
    time_ratio = min(elapsed_time / animation_duration, 1.0)
    
    # Get gacha machine image
    machine_img = get_machine_image(self.version)
    
    # Apply effects
    shake_x, shake_y = _shake_gacha_machine(time_ratio)
    rotation = _rotate_gacha_machine(time_ratio)
    color_tint = _get_color_overlay()
    
    # Apply color tint
    tinted_img = apply_color_tint(machine_img, color_tint, time_ratio)
    
    # Apply rotation (if needed)
    if rotation != 0:
        rotated_img = pygame.transform.rotate(tinted_img, rotation)
    else:
        rotated_img = tinted_img
    
    # Draw at shaken position
    pos = (center_x + shake_x, center_y + shake_y)
    screen.blit(rotated_img, rotated_img.get_rect(center=pos))
    
    # Draw "Click to skip" text
    if not near_end:
        render_text("Click to skip", ...)
```

#### **Sound Selection**
```python
def _play_sound(self, rarity):
    if rarity == 'Legendary':
        audio_manager.play_sfx('legendary')
    else:
        # Random from roll1, roll2, roll3
        roll_sound = random.choice(['roll1', 'roll2', 'roll3'])
        audio_manager.play_sfx(roll_sound)
```

#### **Skip Functionality**
```python
def handle_events(self, events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.skipped = True
            self._transition_to_outcome()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.skipped = True
                self._transition_to_outcome()
```

---

## 5.2 GachaOutcome State

### **Purpose**
Display the results of the gacha pull in a grid, update inventory, and allow player to roll again or return to inventory.

### **Flow**
1. Receives: `version`, `pull_count`, `results` (list of Pokemon)
2. Adds all Pokemon to inventory
3. Marks first-time catches as "NEW"
4. Displays results in grid
5. Provides "Roll Again" and "Back to Inventory" buttons

### **Implementation Details**

#### **Grid Layout**

**Single Pull (1 Pokemon)**:
```
┌──────────────────────────────────┐
│                                  │
│        [Large Pokemon Tile]      │
│                                  │
│   [Roll Again]  [To Inventory]   │
└──────────────────────────────────┘
```

**10-Pull (10 Pokemon)**:
```
┌──────────────────────────────────┐
│  [Tile] [Tile] [Tile] [Tile]    │
│  [Tile] [Tile] [Tile] [Tile]    │
│  [Tile] [Tile]                   │
│                                  │
│   [Roll Again]  [To Inventory]   │
└──────────────────────────────────┘
```

#### **Pokemon Tile Component**
```python
class PokemonTile:
    def __init__(self, pokemon, count=1, is_new=False, size="medium"):
        self.pokemon = pokemon
        self.count = count
        self.is_new = is_new
        self.size = size  # "small", "medium", "large"
    
    def render(self, surface, x, y):
        # Get size constants
        tile_size = TILE_SIZES[self.size]
        
        # Draw background (type color)
        bg_color = get_type_color(pokemon.type1)
        pygame.draw.rect(surface, bg_color, (x, y, tile_size, tile_size))
        
        # Draw rarity outline with glow
        rarity_color = get_rarity_color(pokemon.rarity)
        pygame.draw.rect(surface, rarity_color, 
                        (x, y, tile_size, tile_size), 3)
        
        # Draw Pokemon sprite (centered)
        sprite = resource_manager.get_pokemon_sprite(pokemon.number)
        sprite_rect = sprite.get_rect(center=(x + tile_size//2, y + tile_size//2))
        surface.blit(sprite, sprite_rect)
        
        # Draw type icons (top left, stacked vertically)
        type_y = y + 5
        for poke_type in [pokemon.type1, pokemon.type2]:
            if poke_type:
                type_icon = resource_manager.get_type_icon(poke_type)
                surface.blit(type_icon, (x + 5, type_y))
                type_y += type_icon.get_height() + 2
        
        # Draw count (bottom right)
        if self.count > 0:
            count_text = f"x{self.count}"
            text_surf = font_manager.render_text(count_text, 16, COLOR_WHITE)
            surface.blit(text_surf, (x + tile_size - 30, y + tile_size - 20))
        
        # Draw "NEW!" badge
        if self.is_new:
            badge_surf = font_manager.render_text("NEW!", 14, (255, 255, 0))
            surface.blit(badge_surf, (x + 5, y + tile_size - 20))
```

#### **Outcome State Class**
```python
class GachaOutcomeState(GameState):
    def enter(self, version, pull_count, results):
        self.version = version
        self.pull_count = pull_count
        self.results = results  # List of Pokemon objects
        
        # Update inventory and track NEW pokemon
        self.new_pokemon = []
        for pokemon in results:
            was_new = game_data.add_pokemon(pokemon.number)
            if was_new:
                self.new_pokemon.append(pokemon)
        
        # Save game
        game_data.save()
        
        # Create tiles
        self._create_tiles()
        
        # Create buttons
        machine = resource_manager.get_gacha_machine(version)
        cost = machine.cost_single if pull_count == 1 else machine.cost_10pull
        
        self.roll_again_button = Button(...)
        self.back_button = Button(...)
    
    def _create_tiles(self):
        """Create Pokemon tiles for display"""
        self.tiles = []
        
        if self.pull_count == 1:
            # Single large tile
            pokemon = self.results[0]
            is_new = pokemon in self.new_pokemon
            tile = PokemonTile(pokemon, 1, is_new, size="large")
            self.tiles.append(tile)
        else:
            # 10 small tiles in grid
            for pokemon in self.results:
                is_new = pokemon in self.new_pokemon
                tile = PokemonTile(pokemon, 1, is_new, size="small")
                self.tiles.append(tile)
```

#### **Grid Positioning**
```python
def _calculate_tile_positions(self):
    """Calculate positions for tiles in grid"""
    if self.pull_count == 1:
        # Center single tile
        x = SCREEN_WIDTH // 2 - TILE_LARGE // 2
        y = 200
        return [(x, y)]
    else:
        # 4 columns, 3 rows
        positions = []
        cols = 4
        rows = 3
        tile_size = TILE_SMALL
        spacing = 20
        
        grid_width = (cols * tile_size) + ((cols - 1) * spacing)
        start_x = (SCREEN_WIDTH - grid_width) // 2
        start_y = 150
        
        for i in range(10):
            row = i // cols
            col = i % cols
            x = start_x + (col * (tile_size + spacing))
            y = start_y + (row * (tile_size + spacing))
            positions.append((x, y))
        
        return positions
```

#### **Render Method**
```python
def render(self):
    screen.fill(COLOR_BLACK)
    
    # Title
    title = "GACHA RESULTS!"
    title_surf = font_manager.render_text(title, 48, COLOR_WHITE, is_title=True)
    screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, 80)))
    
    # Render all tiles
    positions = self._calculate_tile_positions()
    for tile, pos in zip(self.tiles, positions):
        tile.render(screen, pos[0], pos[1])
    
    # Render buttons
    roll_again_button.render(screen)
    
    # Show cost below roll again button
    machine = resource_manager.get_gacha_machine(self.version)
    cost = machine.cost_single if pull_count == 1 else machine.cost_10pull
    CurrencyDisplay.render_centered(
        screen,
        roll_again_button.rect.centerx,
        roll_again_button.rect.bottom + 15,
        cost,
        resource_manager.pokedollar_icon,
        font_manager,
        font_size=18,
        icon_size=18
    )
    
    back_button.render(screen)
```

#### **Roll Again Functionality**
```python
def _roll_again(self):
    """Perform another pull with same settings"""
    machine = resource_manager.get_gacha_machine(self.version)
    cost = machine.cost_single if self.pull_count == 1 else machine.cost_10pull
    
    if game_data.gold >= cost:
        game_data.gold -= cost
        game_data.save()
        
        # Perform gacha rolls
        results = gacha_system.roll_ten(self.version) if self.pull_count == 10 \
                  else [gacha_system.roll_single(self.version)]
        
        # Go to animation
        state_manager.change_state('gacha_animation', 
                                  version=self.version,
                                  pull_count=self.pull_count,
                                  results=results)
    else:
        # Show "not enough gold" popup
        self._show_insufficient_funds_popup()
```

---

## 5.3 Integration with GachaBuy State

### **Update Pull Methods**
```python
# In GachaBuyState
def _single_pull(self):
    machine = self.machines[self.selected_machine]
    
    if self.game_data.gold >= machine.cost_single:
        self.game_data.gold -= machine.cost_single
        self.game_data.save()
        
        # Perform gacha roll
        result = self.gacha_system.roll_single(self.selected_machine)
        
        # Transition to animation
        self.state_manager.change_state('gacha_animation',
                                       version=self.selected_machine,
                                       pull_count=1,
                                       results=[result])
    else:
        print("Not enough gold!")
        # TODO: Show popup

def _ten_pull(self):
    machine = self.machines[self.selected_machine]
    
    if self.game_data.gold >= machine.cost_10pull:
        self.game_data.gold -= machine.cost_10pull
        self.game_data.save()
        
        # Perform gacha rolls
        results = self.gacha_system.roll_ten(self.selected_machine)
        
        # Transition to animation
        self.state_manager.change_state('gacha_animation',
                                       version=self.selected_machine,
                                       pull_count=10,
                                       results=results)
    else:
        print("Not enough gold!")
        # TODO: Show popup
```

---

## Implementation Checklist

### GachaAnimation State
- [ ] Create `src/states/gacha_animation_state.py`
- [ ] Implement shake animation with sine waves
- [ ] Implement rotation for higher rarities
- [ ] Implement color tinting based on rarity
- [ ] Add sound effect playback
- [ ] Add skip functionality (click/space)
- [ ] Test all rarity levels

### GachaOutcome State
- [ ] Create `src/states/gacha_outcome_state.py`
- [ ] Create `src/ui/pokemon_tile.py` component
- [ ] Implement grid layout for 1 and 10 pulls
- [ ] Add Pokemon to inventory
- [ ] Track and display "NEW!" badges
- [ ] Implement "Roll Again" button
- [ ] Implement "Back to Inventory" button
- [ ] Test with duplicates (e.g., 3 Pidgey)

### Integration
- [ ] Update `main.py` to register new states
- [ ] Pass `gacha_system` to states
- [ ] Update GachaBuy to transition to animation
- [ ] Test full flow: Buy → Animation → Outcome → Inventory

### Polish
- [ ] Add glow effect to rarity outlines
- [ ] Smooth animation interpolation
- [ ] Particle effects for legendary (optional)
- [ ] Screen shake for legendary reveal (optional)

---

## Next Steps After This Phase

1. **Inventory State Enhancement** - Full Pokemon grid with sorting/filtering
2. **Popup System** - "Not enough gold" modal
3. **Final Polish** - Animations, effects, transitions
4. **Testing** - Complete gameplay loop verification

---

**Ready to implement GachaAnimation and GachaOutcome states!**

