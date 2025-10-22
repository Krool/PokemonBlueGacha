"""
Inventory/Pokédex State - Shows all 151 Pokemon with sorting and filtering
"""
import pygame
from states.base_state import GameState
from config import COLOR_WHITE, COLOR_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, IS_WEB
from ui.button import Button
from ui.checkbox import Checkbox
from ui.sort_button import SortButton, SortOrder
from ui.scrollable_grid import ScrollableGrid
from ui.currency_display import CurrencyDisplay
from ui.stats_popup import StatsPopup
from utils.gacha_stats import GachaStats


class InventoryState(GameState):
    """State for viewing Pokemon collection"""
    
    def __init__(self, state_manager, game_data, resource_manager, audio_manager, font_manager=None, gacha_system=None):
        super().__init__(state_manager, game_data, resource_manager, audio_manager, font_manager, gacha_system)
        
        # Sort and filter state
        self.current_sort = "number"  # "number", "rarity", "count"
        self.sort_ascending = True
        self.show_owned_only = False
        
        # UI Components
        self.open_gacha_button = None
        self.reset_button = None
        self.info_button = None
        self.mute_button = None
        self.owned_only_checkbox = None
        self.sort_buttons = {}
        self.scrollable_grid = None
        self.currency_rect = None  # Clickable currency area
        self.title_rect = None  # Clickable title area for music randomization
        self.stats_popup = None  # Stats popup
        
        # Currency click hold tracking
        self.currency_held = False
        self.currency_hold_timer = 0.0
        self.currency_add_interval = 0.1  # Add gold every 0.1 seconds while held
        
        # Initialize UI
        self._create_ui_components()
    
    def _create_ui_components(self):
        """Create all UI components"""
        # Open Gacha button (top center)
        button_width = 200
        self.open_gacha_button = Button(
            (SCREEN_WIDTH - button_width) // 2, 15,
            button_width, 45,
            "OPEN GACHA",
            self.font_manager,
            font_size=22,
            use_title_font=True,
            bg_color=(0, 100, 200),
            hover_color=(0, 150, 255),
            callback=self._open_gacha,
            audio_manager=self.audio_manager
        )
        
        # Calculate button positions to center INFO between MUTE and RESET
        mute_width = 110
        info_width = 85
        reset_width = 110
        button_spacing = 15
        
        # Total width of all three buttons plus spacing
        total_width = mute_width + info_width + reset_width + button_spacing * 2
        
        # Start position (align to right)
        start_x = SCREEN_WIDTH - total_width - 20
        
        # Mute button (leftmost) - moved down to avoid Pokemon count overlap
        # Hidden on web (no background music on web)
        buttons_y = 95
        if not IS_WEB:
            mute_text = "UNMUTE" if self.game_data.music_muted else "MUTE"
            self.mute_button = Button(
                start_x, buttons_y,
                mute_width, 35,
                mute_text,
                self.font_manager,
                font_size=16,
                bg_color=(100, 100, 100),
                hover_color=(130, 130, 130),
                callback=self._toggle_mute,
                audio_manager=self.audio_manager
            )
        
        # Info button (centered between mute and reset)
        self.info_button = Button(
            start_x + mute_width + button_spacing, buttons_y,
            info_width, 35,
            "INFO",
            self.font_manager,
            font_size=16,
            bg_color=(50, 100, 150),
            hover_color=(70, 130, 180),
            callback=self._show_stats,
            audio_manager=self.audio_manager
        )
        
        # Reset button (rightmost)
        self.reset_button = Button(
            start_x + mute_width + button_spacing + info_width + button_spacing, buttons_y,
            reset_width, 35,
            "RESET",
            self.font_manager,
            font_size=18,
            bg_color=(150, 0, 0),
            hover_color=(200, 0, 0),
            callback=self._reset_collection,
            audio_manager=self.audio_manager
        )
        
        # Sort buttons (below title)
        sort_y = 80
        self.sort_buttons = {
            "number": SortButton(
                20, sort_y, 70, 40, "NUM",
                self.font_manager, font_size=18,
                callback=lambda order: self._on_sort_clicked("number", order),
                audio_manager=self.audio_manager
            ),
            "rarity": SortButton(
                100, sort_y, 70, 40, "RAR",
                self.font_manager, font_size=18,
                callback=lambda order: self._on_sort_clicked("rarity", order),
                audio_manager=self.audio_manager
            ),
            "count": SortButton(
                180, sort_y, 70, 40, "AMT",
                self.font_manager, font_size=18,
                callback=lambda order: self._on_sort_clicked("count", order),
                audio_manager=self.audio_manager
            )
        }
        
        # Set initial sort (by number, ascending)
        self.sort_buttons["number"].set_sort_order(SortOrder.ASCENDING)
        
        # Owned Only checkbox
        self.owned_only_checkbox = Checkbox(
            270, sort_y + 10, 20, "Owned",
            self.font_manager, font_size=18,
            checked=False,
            callback=self._on_filter_changed,
            audio_manager=self.audio_manager
        )
        
        # Scrollable grid (main display area)
        grid_y = 135
        grid_height = SCREEN_HEIGHT - grid_y - 50
        self.scrollable_grid = ScrollableGrid(
            x=20,
            y=grid_y,
            width=SCREEN_WIDTH - 40,
            height=grid_height,
            tile_width=100,
            tile_height=120,
            columns=11,
            spacing_x=10,
            spacing_y=10
        )
    
    def enter(self, **kwargs):
        """Enter inventory state"""
        print("Entered InventoryState")
        print(f"Gold: {self.game_data.gold}")
        print(f"Pokemon owned: {self.game_data.get_total_owned_count()}/151")
        
        # Start or stop music based on mute state
        if self.game_data.music_muted:
            self.audio_manager.stop_music()
        else:
            # Start playing background music when entering Pokédex
            self.audio_manager.play_random_background_music()
        
        # Update mute button text (desktop only)
        if self.mute_button:
            self.mute_button.text = "UNMUTE" if self.game_data.music_muted else "MUTE"
        
        # Refresh the grid with current sort/filter
        self._refresh_grid()
    
    def exit(self):
        """Exit inventory state"""
        print("Exited InventoryState")
    
    def _refresh_grid(self):
        """Refresh the Pokemon grid with current sort/filter settings"""
        # Start with all Pokemon
        pokemon_list = self.resource_manager.pokemon_list.copy()
        
        # Apply filter
        if self.show_owned_only:
            pokemon_list = [p for p in pokemon_list if self.game_data.has_pokemon(p.number)]
        
        # Apply sort
        pokemon_list = self._sort_pokemon(pokemon_list)
        
        # Update grid
        self.scrollable_grid.set_pokemon_list(
            pokemon_list,
            self.resource_manager,
            self.font_manager,
            self.game_data
        )
    
    def _sort_pokemon(self, pokemon_list):
        """Sort Pokemon list based on current settings"""
        if self.current_sort == "number":
            return sorted(pokemon_list, key=lambda p: p.get_pokedex_num(), reverse=not self.sort_ascending)
        elif self.current_sort == "rarity":
            rarity_order = {"Common": 0, "Uncommon": 1, "Rare": 2, "Epic": 3, "Legendary": 4}
            return sorted(pokemon_list, key=lambda p: rarity_order.get(p.rarity, 0), reverse=not self.sort_ascending)
        elif self.current_sort == "count":
            return sorted(pokemon_list, key=lambda p: self.game_data.pokemon_owned.get(p.number, 0), reverse=not self.sort_ascending)
        return pokemon_list
    
    def _on_sort_clicked(self, sort_type: str, order: SortOrder):
        """Handle sort button click"""
        # Reset other sort buttons
        for key, button in self.sort_buttons.items():
            if key != sort_type:
                button.reset()
        
        # Update sort settings
        # Always stay on the same sort type, just toggle asc/desc
        self.current_sort = sort_type
        if order == SortOrder.NONE:
            # If goes to NONE, switch back to ascending
            self.sort_ascending = True
            self.sort_buttons[sort_type].set_sort_order(SortOrder.ASCENDING)
        else:
            self.sort_ascending = (order == SortOrder.ASCENDING)
        
        # Refresh grid
        self._refresh_grid()
    
    def _on_filter_changed(self, checked: bool):
        """Handle owned only checkbox change"""
        self.show_owned_only = checked
        self._refresh_grid()
    
    def _open_gacha(self):
        """Open gacha screen"""
        self.state_manager.change_state('gacha_buy')
    
    def _toggle_mute(self):
        """Toggle music mute"""
        self.game_data.music_muted = not self.game_data.music_muted
        self.game_data.save()
        
        if self.game_data.music_muted:
            self.audio_manager.stop_music()
            if self.mute_button:
                self.mute_button.text = "UNMUTE"
            print("Music muted")
        else:
            # Play random background music
            self.audio_manager.play_random_background_music()
            if self.mute_button:
                self.mute_button.text = "MUTE"
            print("Music unmuted")
    
    def _reset_collection(self):
        """Reset all owned Pokemon (for testing)"""
        self.game_data.reset_inventory()
        self.game_data.save()
        self._refresh_grid()
    
    def _show_stats(self):
        """Show gacha statistics popup"""
        # Calculate stats
        total_pulls = self.game_data.get_total_pulls()
        
        # Get pulls by version
        red_pulls = self.game_data.get_pulls_by_version("Red")
        blue_pulls = self.game_data.get_pulls_by_version("Blue")
        yellow_pulls = self.game_data.get_pulls_by_version("Yellow")
        
        # Calculate expected remaining pulls
        red_expected = GachaStats.calculate_expected_pulls_for_version(
            self.resource_manager.pokemon_list,
            self.resource_manager.rarities_dict,
            "Red",
            self.game_data.pokemon_owned
        )
        
        blue_expected = GachaStats.calculate_expected_pulls_for_version(
            self.resource_manager.pokemon_list,
            self.resource_manager.rarities_dict,
            "Blue",
            self.game_data.pokemon_owned
        )
        
        yellow_expected = GachaStats.calculate_expected_pulls_for_version(
            self.resource_manager.pokemon_list,
            self.resource_manager.rarities_dict,
            "Yellow",
            self.game_data.pokemon_owned
        )
        
        # Calculate total expected from scratch (returns sum)
        total_expected = GachaStats.calculate_expected_pulls_from_scratch(
            self.resource_manager.pokemon_list,
            self.resource_manager.rarities_dict
        )
        
        # Calculate optimal strategy cost
        machines = {
            "Red": self.resource_manager.get_gacha_machine("Red"),
            "Blue": self.resource_manager.get_gacha_machine("Blue"),
            "Yellow": self.resource_manager.get_gacha_machine("Yellow")
        }
        optimal_cost = GachaStats.calculate_optimal_strategy_cost(
            self.resource_manager.pokemon_list,
            self.resource_manager.rarities_dict,
            machines
        )
        
        # Create popup (100 pixels taller than original 550)
        self.stats_popup = StatsPopup(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            700,
            700,  # Made taller to fit optimal cost
            total_pulls,
            red_pulls, red_expected,
            blue_pulls, blue_expected,
            yellow_pulls, yellow_expected,
            total_expected,
            optimal_cost,
            self.font_manager,
            game_data=self.game_data,  # Pass game_data for setting gold
            callback=None,  # Don't use callback, we handle cleanup in handle_events
            audio_manager=self.audio_manager
        )
    
    def handle_events(self, events):
        """Handle input events"""
        # Enable audio on any user interaction (for web browser autoplay policy)
        for event in events:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                # Don't auto-start music if muted
                allow_music = not self.game_data.music_muted
                self.audio_manager.enable_audio_after_interaction(allow_music_start=allow_music)
                break
        
        # Handle stats popup first if showing
        if self.stats_popup is not None:
            if self.stats_popup.is_showing():
                for event in events:
                    self.stats_popup.handle_event(event)
                # Check again after event handling (popup might have closed itself)
                if self.stats_popup is not None and not self.stats_popup.is_showing():
                    self.stats_popup = None
                return
            else:
                # Popup is not showing, clean it up
                self.stats_popup = None
        
        # Update UI components
        self.open_gacha_button.update()
        if self.mute_button:
            self.mute_button.update()
        self.reset_button.update()
        self.info_button.update()
        self.owned_only_checkbox.update()
        for button in self.sort_buttons.values():
            button.update()
        
        for event in events:
            # Pass to UI components
            self.open_gacha_button.handle_event(event)
            if self.mute_button:
                self.mute_button.handle_event(event)
            self.reset_button.handle_event(event)
            self.info_button.handle_event(event)
            self.owned_only_checkbox.handle_event(event)
            for button in self.sort_buttons.values():
                button.handle_event(event)
            
            # Pass scroll events to grid
            self.scrollable_grid.handle_event(event)
            
            # Check for title click (randomize music)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.title_rect and self.title_rect.collidepoint(event.pos):
                    # Randomize background music if not muted
                    if not self.game_data.music_muted:
                        self.audio_manager.play_random_background_music()
                    continue
            
            # Check for currency click start
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.currency_rect and self.currency_rect.collidepoint(event.pos):
                    self.currency_held = True
                    self.currency_hold_timer = 0.0
                    # Add immediately on first click
                    self.game_data.gold += 10000
                    self.game_data.save()
                    print(f"Added 10000 gold! Total: {self.game_data.gold}")
                    continue
            
            # Check for currency click release
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.currency_held = False
            
            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._open_gacha()
                elif not IS_WEB and event.key == pygame.K_ESCAPE:
                    # Quit game (desktop only)
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def update(self, dt):
        """Update state"""
        self.scrollable_grid.update(dt)
        
        # Handle currency hold - add gold continuously while held
        if self.currency_held:
            self.currency_hold_timer += dt
            if self.currency_hold_timer >= self.currency_add_interval:
                self.currency_hold_timer = 0.0
                self.game_data.gold += 10000
                self.game_data.save()
                print(f"Added 10000 gold (hold)! Total: {self.game_data.gold}")
    
    def render(self):
        """Render inventory"""
        self.screen.fill(COLOR_BLACK)
        
        # Draw title (clickable to randomize music)
        if self.font_manager:
            title = "POKÉDEX"
            title_surface = self.font_manager.render_text(title, 48, COLOR_WHITE, is_title=True)
            title_x = 20
            title_y = 15
            self.screen.blit(title_surface, (title_x, title_y))
            
            # Store clickable rect for title
            self.title_rect = title_surface.get_rect(topleft=(title_x, title_y))
            
            # Draw progress (gold color when collection is complete) - positioned right next to title
            owned_count = self.game_data.get_total_owned_count()
            total_count = len(self.resource_manager.pokemon_list)
            progress_text = f"{owned_count}/{total_count}"
            
            # Use gold color if collection is complete
            progress_color = (255, 215, 0) if owned_count >= total_count else COLOR_WHITE
            progress_surface = self.font_manager.render_text(progress_text, 32, progress_color, is_title=True)
            
            # Position to the right of the title with spacing
            progress_x = title_x + title_surface.get_width() + 20
            progress_y = title_y + 20  # Align vertically with title (slightly lower to baseline-align better)
            self.screen.blit(progress_surface, (progress_x, progress_y))
        
        # Draw currency (top right, with dark gray background container)
        currency_x = SCREEN_WIDTH - 20
        currency_y = 20
        
        # Calculate currency dimensions for background
        icon_size = 28
        padding = 12
        if self.font_manager:
            amount_str = f"{self.game_data.gold:,}"
            text_surface = self.font_manager.render_text(amount_str, 28, COLOR_WHITE)
            total_width = icon_size + 5 + text_surface.get_width()
            
            # Store currency rect for click detection (no background)
            self.currency_rect = pygame.Rect(
                currency_x - total_width, currency_y - icon_size // 2,
                total_width, icon_size
            )
        
        CurrencyDisplay.render(
            self.screen,
            currency_x,
            currency_y,
            self.game_data.gold,
            self.resource_manager.pokedollar_icon,
            self.font_manager,
            font_size=28,
            color=COLOR_WHITE,
            icon_size=28,
            align="right"
        )
        
        # Draw buttons
        self.open_gacha_button.render(self.screen)
        if self.mute_button:
            self.mute_button.render(self.screen)
        self.reset_button.render(self.screen)
        self.info_button.render(self.screen)
        
        # Draw sort buttons
        for button in self.sort_buttons.values():
            button.render(self.screen)
        
        # Draw checkbox
        self.owned_only_checkbox.render(self.screen)
        
        # Draw scrollable grid
        self.scrollable_grid.render(self.screen)
        
        # Draw instructions at bottom (hide if stats popup is open)
        if self.font_manager and not (self.stats_popup is not None and self.stats_popup.is_showing()):
            instructions = "Mouse Wheel: Scroll | Space: Open Gacha | ESC: Quit"
            inst_surface = self.font_manager.render_text(instructions, 16, (150, 150, 150))
            inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
            self.screen.blit(inst_surface, inst_rect)
        
        # Draw stats popup if showing (render on top)
        if self.stats_popup is not None and self.stats_popup.is_showing():
            self.stats_popup.render(self.screen)
